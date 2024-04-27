# Transparent Camera Project

A brief description of the project should go here.

Each folder in this project contains a README.md detailing the contents of the folder as well as instructions on how to use the files in the folder if needed.

# Contents
- 3D Models:  This folder contains the files used to design and print the camera frame.
- Camera Software:  This folder contains the software used to capture images for the training and testing of the transparent camera.
- Eye Tracking Software:  This folder contains the eye tracking software used in this project.
- Pix2PixHD:  This folder contains the modified pix2pixHD model that was used in this project.
- Utilities:  This folder contains utility scripts that have helped the project progress but are not necessary to the project.

# Move this to the Pix2PixHD folder
4.) Pix2PixHD Use in the Transparent Camera  

    A.) Training of the Transparent Camera Model 
    
        1.) Create a folder "name of your choice" under datasets and in that folder create two folders called "train_A" and "train_B" 
            and load ground truth images in "test_B" and side camera images in "test_A" that the model has not been exposed to.  
            
        2.) Run the following command with the updated directories and a number after --niter for how many epochs you would like to run
        python train.py --label_nc 0 --no_instance --name "name of your choice" --dataroot './datasets/"name of your choice"' --niter #epochs


    B.) Testing of the Transparent Camera Model  
        1.) To test with this model, place the "latest_net_D.pth" and "latest_net_G.pth" models in a folder "name of your choice" under the checkpoints folder   
            located in the pix2pixHD code folder.  
        2.) Create a new folder named "whatever you want" with "test_A" and "test_B" folders within and load ground truth images in "test_B" and side camera images in "test_A" that the  
            model has not been exposed to. 

        3.) Test by running python test.py --label_nc 0 --no_instance --name tst_img --dataroot   
        './"your directory to pix2pixHD"/datasets/"whatever you want"' --checkpoints_dir '/"your directory to pix2pixHD"/checkpoints/"name of your choice"'  
