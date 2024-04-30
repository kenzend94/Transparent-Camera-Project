# Forked pix2pixHD Repository

This repository is a fork of the original [NVIDIA pix2pixHD](https://github.com/NVIDIA/pix2pixHD) designed to enhance compatibility with Python 3.11. 

# Setup Instructions
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

## Modifications
### Python 3.11 Compatibility
- Updated the codebase to be compatible with Python 3.11