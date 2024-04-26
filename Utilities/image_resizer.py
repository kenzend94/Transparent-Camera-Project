'''
image_resizer.py

This python script takes a directory of images and resizes them to a desired size.

It is customizable and allows the user to change settings as needed.

Author:  Kenneth Gordon
Date:  April 19, 2024
'''

import cv2
import os

# Global configuration variables
input_image_directory = "C:/Users/kgord/Downloads/environment2/Side"
output_image_directory = "C:/Users/kgord/Downloads/downscaled_environment2/Side"
x_resize = 1152
y_resize = 648

'''
resize_image()

Resizes the input image to the desired dimensions.
'''
def resize_image(image_name, x, y):
    image = cv2.imread(f"{input_image_directory}/{image_name}")
    resized_image = cv2.resize(image, (x, y), )
    cv2.imwrite(f"{output_image_directory}/{image_name}", resized_image)
    pass

if __name__ == "__main__":
    print(f"Resizing images in \"{input_image_directory}\"")
    for image in os.listdir(input_image_directory):
        if (image.endswith(".jpg")):
            print(f"Resizing {image}...")
            resize_image(image, x_resize, y_resize)
    print("Done!")