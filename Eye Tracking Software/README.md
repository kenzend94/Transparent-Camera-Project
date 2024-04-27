# Transparent Camera Project - Eye Tracking Software

This folder contains the software necessary to run the eye tracker on either a webcam or images stored on the computer's hard disk.

In order for this software to properly work, you must install opencv-python, dlib, and numpy.

You must also download a model file for face tracking.  These files can be downloaded from:  https://github.com/davisking/dlib-models.  You should use either one of the 68 face landmarks files, but the model68_GTX.dat seems to work best.

# Contents
- eye_tracker.py:  The Python script used to run the eye tracking software on images stored on the computer's hard disk.
- live_eye_tracker.py:  The Python script used to run the eye tracking software using the computer's webcam.