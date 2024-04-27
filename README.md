Transparent Camera  
1.) 3D Models  

    A.) Folder contains files used to design and print the camera frame  
    
2.) Camera Software  

    A.) Folder contains software used to capture images for training and testing of the transparent camera. To run this camera, refer to README.MD in the Camera  
        Software folder.

    
3.) Eye Tracking Software   

4.) Pix2PixHD Use in the Transparent Camera  

    A.) Training of the Transparent Camera Model  
    - Training with Ground Truth and Side Camera Datasets  



    B.) Testing of the Transparent Camera Model  
        1.) To train with this model, place the "latest_net_D.pth" and "latest_net_G.pth" models in a folder "name of your choice" under the checkpoints folder   
            located in the pix2pixHD code folder.  
        2.) Create a "test_A" and "test_B" folder in the datasets and load ground truth images in "test_B" and side camera images in "test_A" that the  
            model has not been exposed to. 

        3.) Test by running python test.py --label_nc 0 --no_instance --name tst_img --dataroot   
        C:\"your directory to pix2pixHD"\datasets\tst_img --checkpoints_dir C:\"your directory to pix2pixHD"\checkpoints\"name of your choice"  
