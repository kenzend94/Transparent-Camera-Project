'''
camera.py

This script contains all of the code necessary to run the transparent camera.

Authors:  Kenneth Gordon, Khoi Ngyuen, and Thomas Warren
Date: 4/26/24
'''

# Necessary imports
import subprocess
from picamera2 import Picamera2, Preview
from time import sleep
import libcamera
import os
import xml.etree.ElementTree as ET
from datetime import datetime

# Global config
settings_filename = 'settings.xml' # currently uses the settings.xml present on the desktop!
counter_value = 0 # Initialize counter_value

# Define the name of the saved data (ie: subject name)
# This should be moved to our settings.xml file eventually
IMAGE_ID = "replace_me"

# Create a flag to toggle the camera's preview
# This should also be moved to settings.xml eventually
ENABLE_PREVIEW = True

# Define how many photos we want to take from the camera
NUMBER_OF_CAPTURES = 10

'''
create_settings_xml()

This function creates a setting.xml file with an initial counter value at the settings_filename global variable.
'''
def create_settings_xml(counter_value, filename = settings_filename):
    root = ET.Element('Settings')
    counter = ET.SubElement(root, 'Counter')
    counter.text = str(counter_value)
    tree = ET.ElementTree(root)
    tree.write(filename)

'''
read_settings_xml()

This function reads the counter value from settings.xml and stores it in the counter_value global variable.
'''
def read_settings_xml(filename=settings_filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    counter_value = int(root.find('Counter').text)
    return counter_value

'''
make_archive()

Function that takes the photos stored in the Front and Side folders and zips them.

The zipped archive is then moved to the camera's website path to be downloaded.
'''
def make_archive(IMAGE_ID):
    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct path for 'Side' and 'Front' folder
    side_dir = os.path.join(current_dir, 'Side')
    front_dir = os.path.join(current_dir, 'Front')

    # Create dir for 'Side' and 'Front' if they do not exist
    os.makedirs(side_dir, exist_ok=True)
    os.makedirs(front_dir, exist_ok=True)

    # Get today's date in the format MM-DD-YYYY
    today_date = datetime.now().strftime("%m-%d-%Y")

    # Construct the archive name using IMAGE_ID and today's date
    archive_name = f"{IMAGE_ID}-{today_date}.zip"

    # Navigate to the directory where 'Front' and 'Side' folders are located
    os.chdir(current_dir)

    # Use subprocess to run the zip command
    try:
        subprocess.check_call(['zip', '-r', archive_name, 'Front', 'Side'])
        print(f"Done archiving the images into {archive_name}!")
        
        # Construct the full path of the zip file
        zip_file_path = os.path.join(current_dir, archive_name)
        
        # Construct the destination path
        destination_path = "/var/www/html/download/"
        
        # Use subprocess to run the sudo cp command
        subprocess.check_call(['sudo', 'cp', zip_file_path, destination_path])
        print(f"Successfully copied {archive_name} to {destination_path}")
        
    except subprocess.CalledProcessError as e:
        print("Failed to create or copy archive: ", e)

'''
main()

Function that takes photos using the transparent camera.
'''
def main():
    # Check if settings.xml exist
    if not os.path.exists(settings_filename):
        create_settings_xml(counter_value)  # Create settings.xml with counter starting at 0
        print("\nThere is no existing settings.xml, create settings.xml...\n")
    else:
        counter_value = read_settings_xml(settings_filename)  # Read the current counter value
        print(f"\nFound settings.xml, the counter value right now is {counter_value}\n")

    # Make sure that the subject's name has been modified
    if IMAGE_ID == "replace_me":
        print("Please enter a valid image id!")
        return

    # Get the current directory
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Construct path for 'Side' and 'Front' folder
    side_dir = os.path.join(current_dir, 'Side')
    front_dir = os.path.join(current_dir, 'Front')

    # Create dir for 'Side' and 'Front' if they do not exist
    os.makedirs(side_dir, exist_ok=True)
    os.makedirs(front_dir, exist_ok=True)

    # Assign the cameras
    picam0 = Picamera2(0)
    picam1 = Picamera2(1)

    if (ENABLE_PREVIEW):
        picam0.start_preview(Preview.QTGL)
        picam1.start_preview(Preview.QTGL)

        # Configure the front camera such that preview images are rotated 180 degrees in the preview
        front_camera_config = Picamera2.create_preview_configuration(picam1)
        front_camera_config["transform"] = libcamera.Transform(hflip=1, vflip=1)
        picam1.configure(front_camera_config)

        # Start the cameras
        picam0.start()
        picam1.start()

        # Preview the output
        sleep(5)

        # Stop the cameras
        picam0.stop()
        picam1.stop()
        picam0.stop_preview()
        picam1.stop_preview()

    # Configure the front camera such that captured images are rotated 180 degress
    front_camera_config = Picamera2.create_still_configuration(picam1)
    front_camera_config["transform"] = libcamera.Transform(hflip=1, vflip=1)
    picam1.configure(front_camera_config)

    # Start the cameras
    picam0.start()
    picam1.start()

    # Capture the data
    for ii in range(counter_value, counter_value + NUMBER_OF_CAPTURES):
        # Save file into Front and Side folder
        side_file_path = os.path.join(side_dir, f'{IMAGE_ID}_side_{ii}.jpg')
        front_file_path = os.path.join(front_dir, f'{IMAGE_ID}_front_{ii}.jpg')
        picam0.capture_file(side_file_path)
        picam1.capture_file(front_file_path)
        print(f"Done capturing image {ii}")
        sleep(0.25)

    # Update the counter value in settings.xml
    create_settings_xml(ii + 1)

    # Stop both of the cameras
    picam0.stop()
    picam1.stop()

    # Make an archive of the images and upload it to the camera's website
    make_archive(IMAGE_ID)

if __name__ == "__main__":
    main()