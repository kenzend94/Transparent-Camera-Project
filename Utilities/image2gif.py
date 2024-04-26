'''
png2gif.py

This python script takes images stored within a specified folder and converts them into a gif.

It is highly customizable and allows the user to change settings as needed.

Author:  Kenneth Gordon
Date:  March 18, 2024
'''

from PIL import Image
from natsort import natsorted # Used to sort the png files in order after they are fetched by glob
import glob

# Global configuration variables
frame_folder = "C:/Users/Kenneth/Desktop/ECE5960/Training Results/UNet"
frame_file_type = ".png"
gif_location = "C:/Users/Kenneth/Desktop/ECE5960/Training Results"
gif_name = "face_training"
gif_duration = 200

'''
make_gif()

Creates a gif from the images contained in the frame folder.
'''
def make_gif():
    # Create an array of the frames from the frame folder.
    # Sort them so that frames appear in the correct order in the gif.
    frames = [Image.open(image) for image in natsorted(glob.glob(f"{frame_folder}/*{frame_file_type}"))]

    # Get the first frame and create a gif from it.
    frame_one = frames[0]
    frame_one.save(f"{gif_location}/{gif_name}.gif", format="GIF", append_images=frames, save_all=True, duration=gif_duration, loop=0)
    
    # If there are no issues, return true to let the user know a gif was successfully made
    return True

if __name__ == "__main__":
    print("Making Gif...")
    if (make_gif()):
        print("Done!")