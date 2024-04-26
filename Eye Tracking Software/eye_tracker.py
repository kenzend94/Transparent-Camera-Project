'''
eye_tracker.py

This python script uses a pre-trained face detection model to find and detect the location of eyes from an input image(s).

The original code was written by Vardan Argwal and was adapted for ECE5960/ECE6960 by Kenneth Gordon.

Model files can be downloaded from:  https://github.com/davisking/dlib-models
You should use the model68_GTX.dat file.

Authors: Vardan Argwal, Kenneth Gordon, Khoi Nguyen, and Thomas Warren
Date: March 18, 2024
Source:  https://towardsdatascience.com/real-time-eye-tracking-using-opencv-and-dlib-b504ca724ac6
'''

import cv2         # For image processing
import dlib        # For loading the face recognition model
import numpy as np # For general purpose number work
import sys         # For argument loading
import os          # For working with paths

# Controls whether or not eye outlines are shown on the image
ENABLE_EYE_OUTLINES = True

# The location of the model file
MODEL_PATH = os.path.join(os.getcwd(), 'model\\model68_GTX.dat')

# The location of the input images
INPUT_LOCATION = os.path.join(os.getcwd(), 'images\\raw')

# The location to save images
SAVE_LOCATION = os.path.join(os.getcwd(), 'images\\processed')

# The threshold value to apply to the mask
THRESHOLD = 78

# Threshold Notes:
# 78 seems to work best of Kenneth
# 35 seems to work best for Khoi
# ?? seems to work best for Thomas 

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
run_eye_detector()

Runs the eye_detector on a single image given by input_file_name.

input_file_name - the image to run the eye detector on
'''
def run_eye_detector(input_file_name):
     # Initialize the face detector and predictor model from dlib
    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(MODEL_PATH)

    # These coordinates correspond to the eye coordinates given by the predictor model.
    left_eye = [36, 37, 38, 39, 40, 41]
    right_eye = [42, 43, 44, 45, 46, 47]

    # Read from the input parameter
    img = cv2.imread(os.path.join(INPUT_LOCATION, input_file_name + '.jpg'))
    threshold = img.copy()

    # Prepare the eye tracker
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
        # kernel = np.ones((9, 9), np.uint8)
        # mask = cv2.dilate(mask, kernel, 5)

        # Segment out the eyes in the mask
        eyes = cv2.bitwise_and(img, img, mask=mask)
        mask = (eyes == [0, 0, 0]).all(axis=2)
        eyes[mask] = [255, 255, 255]
        mid = (shape[42][0] + shape[39][0]) // 2
        eyes_gray = cv2.cvtColor(eyes, cv2.COLOR_BGR2GRAY)

        # Thresholding is used to create to binary nature of the mask
        # Change the threshold value depending on the value of the slider
        threshold = THRESHOLD
        _, threshold = cv2.threshold(eyes_gray, threshold, 255, cv2.THRESH_BINARY)
        # threshold = cv2.erode(threshold, None, iterations=2)
        # threshold = cv2.dilate(threshold, None, iterations=4) # Reduces the size of the mask
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

    # Save the true image with eye detections and facial landmarks along with the mask
    cv2.imwrite(os.path.join(SAVE_LOCATION, input_file_name + '.jpg'), img)
    cv2.imwrite(os.path.join(SAVE_LOCATION, input_file_name + '-mask.jpg'), threshold)

'''
main()

Driver function for the eye detector.

Should have at least one argument specifying whether to run in 'directory' mode or not.

'directory' mode applies the eye_detector script to the entire input directory.
'single' mode applies the eye_detector script to a specified file within the input directory.
'''
def main():
    # Check that the number of arguments is correct
    if (len(sys.argv) < 2):
         print("Error!  There should have at least one argument specifying whether or not to run the script in 'directory' mode!")
         return

    if (sys.argv[1] == "True"): # Directory Mode
        for file in os.listdir(INPUT_LOCATION):
            if (file.endswith('.jpg')):
                print('Processing \"' + file + '\"...')
                run_eye_detector(file.split('.')[0])
    elif(len(sys.argv) == 3): # Single Mode
        if (not sys.argv[2].endswith('.jpg')):
            print('Processing \"' + sys.argv[2] + "\"...")
            run_eye_detector(sys.argv[2])
        else:
            print("Error!  Please make sure that your filename doesn't end with an extension!")
            return
    else: # Argument error
        print("Error!  You have indicated that you want the script to run in 'single' mode but didn't specify an input filename!")
        return

    print('Done!')

if __name__ == "__main__":
    main()