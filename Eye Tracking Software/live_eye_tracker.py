'''
live_eye_tracker.py

This python script uses a pre-trained face detection model to find and track the location of eyes from the user's webcam.

The original code was written by Vardan Argwal and was adapted for ECE5960/ECE6960 by Kenneth Gordon.

Model files can be downloaded from:  https://github.com/davisking/dlib-models
You should use either one of the 68 face landmarks files, but the model68_GTX.dat seems to work best.

Authors: Vardan Argwal, Kenneth Gordon, Khoi Nguyen, and Thomas Warren
Date: March 18, 2024
Source:  https://towardsdatascience.com/real-time-eye-tracking-using-opencv-and-dlib-b504ca724ac6
'''

import cv2         # For image processing
import dlib        # For loading the face recognition model
import numpy as np # For general purpose number work

# Controls whether or not eye outlines are shown on the image
ENABLE_EYE_OUTLINES = True

# The location of the model file
MODEL_PATH = r"insert_the_path_to_your_model_here"

'''
shape_to_np()

Converts a shape predictor into a set of (x, y) coordinates

shape - the shape predictor
dtype - the type of input data
'''
def shape_to_np(shape, dtype="int"):
	# Initialize the list of (x, y)-coordinates
	coords = np.zeros((68, 2), dtype=dtype)
     
	# Loop over the 68 facial landmarks in the model and convert them to a 2-tuple of (x, y)-coordinates
	for i in range(0, 68):
		coords[i] = (shape.part(i).x, shape.part(i).y)
          
	# Return the list of (x, y)-coordinates
	return coords

'''
eye_on_mask()

Finds an eye (left or right depending on side) on the given mask.

shape - the shape predictor
mask - the image mask
side - the side of the face to detect the eye from
'''
def eye_on_mask(shape, mask, side):
    points = [shape[i] for i in side]
    points = np.array(points, dtype=np.int32)
    mask = cv2.fillConvexPoly(mask, points, 255)
    return mask

'''
contouring()

Utilizing contouring, this function draws red circles in the center of detected eyeballs.

threshold - the calculated image threshold
mid - the midpoint between the eys
img - the image to draw to
right - whether or not the contour is on the right side of the face
'''
def contouring(threshold, mid, img, right=False):
    cnts, _ = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    try:
        cnt = max(cnts, key = cv2.contourArea)
        M = cv2.moments(cnt)
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        if right:
            cx += mid
        cv2.circle(img, (cx, cy), 4, (0, 255, 0), 2)
    except:
        pass

'''
main()

Driver function for the live eye tracker
'''
def main():
    # Initialize the face detector and predictor model from dlib
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(MODEL_PATH)

    # These coordinates correspond to the eye coordinates given by the predictor model.
    left_eye = [36, 37, 38, 39, 40, 41]
    right_eye = [42, 43, 44, 45, 46, 47]

    # Get video from the webcam
    # Should this be changed to take a raw image input instead of a webcam stream for the transparent camera
    webcam_capture = cv2.VideoCapture(0)
    ret, img = webcam_capture.read()
    threshold = img.copy()

    # Create a window to display the threshold on
    cv2.namedWindow("Eye Tracker: Threshold")
    kernel = np.ones((9, 9), np.uint8)

    # Put a slider for the user to customize their threshold level
    cv2.createTrackbar("Threshold", "Eye Tracker: Threshold", 0, 255, lambda arg: None)

    while(True):
        # Read from the webcam (ret needs to be there even though it isn't used)
        ret, img = webcam_capture.read()
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        rects = detector(gray, 1)
        for rect in rects:
            shape = predictor(gray, rect)
            shape = shape_to_np(shape)

            # Create the eye mask
            mask = np.zeros(img.shape[:2], dtype=np.uint8)
            mask = eye_on_mask(shape, mask, left_eye)
            mask = eye_on_mask(shape, mask, right_eye)

            # Expand the eyes in the mask
            mask = cv2.dilate(mask, kernel, 5)

            # Segment out the eyes in the mask
            eyes = cv2.bitwise_and(img, img, mask=mask)
            mask = (eyes == [0, 0, 0]).all(axis=2)
            eyes[mask] = [255, 255, 255]
            mid = (shape[42][0] + shape[39][0]) // 2
            eyes_gray = cv2.cvtColor(eyes, cv2.COLOR_BGR2GRAY)

            # Thresholding is used to create the binary nature of the mask
            # Change the threshold value depending on the value of the slider
            threshold = cv2.getTrackbarPos("Threshold", "Eye Tracker: Threshold")
            _, threshold = cv2.threshold(eyes_gray, threshold, 255, cv2.THRESH_BINARY)
            # threshold = cv2.erode(threshold, None, iterations=2)
            # threshold = cv2.dilate(threshold, None, iterations=4)
            # threshold = cv2.medianBlur(threshold, 3)

            # Invert the threshold so that contouring works as intended
            threshold = cv2.bitwise_not(threshold)

            # Draw red circles in the center of the detected eyes
            contouring(threshold[:, 0:mid], mid, img)
            contouring(threshold[:, mid:], mid, img, True)

            # Display detected eye outlines if enabled
            if (ENABLE_EYE_OUTLINES):
                for (x, y) in shape[36:48]:
                    cv2.circle(img, (x, y), 2, (255, 255, 0), -1)
        
        # Show the true image with eye detections and facial landmarks
        cv2.imshow("Eye Tracker: Image", img)
        cv2.imshow("Eye Tracker: Threshold", threshold)

        # Quit the loop by pressing 'q'
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        
    # Release acquired resources
    webcam_capture.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()