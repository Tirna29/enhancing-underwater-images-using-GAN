# Download the dataset
1. Download link: https://drive.google.com/drive/folders/1Hp2zCq-jEztuPtsMmSDGNXvCZeIDKOfh
   
# Steps to execute the code
1. Install all the libraries in the requirements.txt. 

2. Our dataset is under EUVP/Paired. We preprocess the combined dataset by running the data_split.py
   file under the preprocess folder. For example, We can run the following command:
   python data_split.py -d "path/to/dataset" -p 

3. Then, we train our model using train.py which consists of the code for running the code using GPUs and CPUs. We need to specify the path where the model 
   will be saved, the dataset, the number of epochs, batch size, the number of data loading workers, and the learning rate. If we do not specify 
   the architecture, the model will be trained on v1 architecture. For example, we can run the following command for running the train.py file:
   python train.py --save-path "/path/to/save/model" -d "/path/to/dataset -a "v1" --epochs 40 --lr 1e-4 -b 16 -j 8

4. To generate the enhanced images using the trained model, we need to execute the infer.py file. We need to specify
   the path where the generated images will be saved, the path to the test dataset, Inp, which consists of poor-quality images, 
   the path to the trained generator model, batch size, and the number of data loading workers. Here is an example:
   python infer.py --save-path "/path/to/save/generated/images" -d "/path/to/EUVP/test_samples/Inp" -m "/path/to/generator" -b 16 -j 8

5. Once we have the generated images, we can evaluate the model using the evaluation metrics - SSIM, PSNR, and UIQM. These are present 
   in the evaluation folder. To capture the UIQM metrics, we run the measure_uiqm.py and specify the path to the generated images. 
   For example, we can run the following command:
   python measure_uiqm.py --data "/path/to/EUVP/generated/images"

6. To calculate the SSIM and PSNR metrics, we execute measure_ssim_psnr.py on the test dataset, GTr, consisting of the ground truth 
   images. We also need to specify the path to the generated images. Here is an example command:
   python measure_ssim_psnr.py --image-data "/path/to/EUVP/generated/images" --label-data "/path/to/EUVP/test_samples/GTr"
   
#Reference
@article{article,
author = {Islam, Md Jahidul and Xia, Youya and Sattar, Junaed},
year = {2020},
month = {02},
pages = {1-1},
title = {Fast Underwater Image Enhancement for Improved Visual Perception},
volume = {PP},
journal = {IEEE Robotics and Automation Letters},
doi = {10.1109/LRA.2020.2974710}
}
