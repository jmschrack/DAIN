# DAIN (Depth-Aware Video Frame Interpolation)
[Project](https://sites.google.com/view/wenbobao/dain) **|** [Paper](http://arxiv.org/abs/1904.00830)
[Wenbo Bao](https://sites.google.com/view/wenbobao/home),
[Wei-Sheng Lai](http://graduatestudents.ucmerced.edu/wlai24/), 
[Chao Ma](https://sites.google.com/site/chaoma99/),
Xiaoyun Zhang, 
Zhiyong Gao, 
and [Ming-Hsuan Yang](http://faculty.ucmerced.edu/mhyang/)

IEEE Conference on Computer Vision and Pattern Recognition, Long Beach, CVPR 2019

This work is developed based on our TPAMI work [MEMC-Net](https://github.com/baowenbo/MEMC-Net), where we propose the adaptive warping layer. Please also consider referring to it.

### Table of Contents
1. [Introduction](#introduction)
1. [Requirements and Dependencies](#requirements-and-dependencies)
1. [Installation](#installation)
1. [Testing Pre-trained Models](#testing-pre-trained-models)
1. [Downloading Results](#downloading-results)
1. [Slow-motion Generation](#slow-motion-generation)
1. [Training New Models](#training-new-models)


### Introduction
This branch attempts to enable the original source code to be run on ROCm with AMD hardware. This is accomplished by converting the CUDA source code to HIP code.

View the original README.md on the Master branch for full writup.





### Requirements and Dependencies
- Ubuntu 
- Python3
- ROCm-dkms
- GCC (Compiling PyTorch 1.0.0 extension files (.c/.cu) requires gcc = 4.9.1 and nvcc = 9.0 compilers)
- AMD GPU 

### Build Pytorch for AMD 
[Follow AIEater's guide](https://github.com/aieater/rocm_pytorch_informations)
**Note** The guide neglects to initialize submodules of the pytorch repo.  This seems to be intentional as part of the pytorch build_amd script modifies the requirements and dependencies. 
Just follow the guide until python errors out and asks you to initialize.

### Installation
Download repository:

    $ git clone https://github.com/baowenbo/DAIN.git


    
Generate our PyTorch extensions:

    
    $ cd DAIN
    $ python3 tools/amd_build/build_amd.py
    $ cd my_package 
    $ ./build.sh

Generate the Correlation package required by [PWCNet](https://github.com/NVlabs/PWC-Net/tree/master/PyTorch/external_packages/correlation-pytorch-master):
    
    $ cd ../PWCNet/correlation_package_pytorch1_0
    $ ./build.sh


### Testing Pre-trained Models
Make model weights dir and Middlebury dataset dir:

    $ cd DAIN
    $ mkdir model_weights
    $ mkdir MiddleBurySet
    
Download pretrained models, 

    $ cd model_weights
    $ wget http://vllab1.ucmerced.edu/~wenbobao/DAIN/best.pth
    
and Middlebury dataset:
    
    $ cd ../MiddleBurySet
    $ wget http://vision.middlebury.edu/flow/data/comp/zip/other-color-allframes.zip
    $ unzip other-color-allframes.zip
    $ wget http://vision.middlebury.edu/flow/data/comp/zip/other-gt-interp.zip
    $ unzip other-gt-interp.zip
    $ cd ..


We are good to go by:

    $ CUDA_VISIBLE_DEVICES=0 python demo_MiddleBury.py

The interpolated results are under `MiddleBurySet/other-result-author/[random number]/`, where the `random number` is used to distinguish different runnings. 

### Downloading Results
Our DAIN model achieves the state-of-the-art performance on the UCF101, Vimeo90K, and Middlebury ([*eval*](http://vision.middlebury.edu/flow/eval/results/results-n1.php) and *other*).
Dowload our interpolated results with:
    
    $ wget http://vllab1.ucmerced.edu/~wenbobao/DAIN/UCF101_DAIN.zip
    $ wget http://vllab1.ucmerced.edu/~wenbobao/DAIN/Vimeo90K_interp_DAIN.zip
    $ wget http://vllab1.ucmerced.edu/~wenbobao/DAIN/Middlebury_eval_DAIN.zip
    $ wget http://vllab1.ucmerced.edu/~wenbobao/DAIN/Middlebury_other_DAIN.zip
    
    
### Slow-motion Generation
Our model is fully capable of generating slow-motion effect with minor modification on the network architecture.
Run the following code by specifying `time_step = 0.25` to generate x4 slow-motion effect:

    $ CUDA_VISIBLE_DEVICES=0 python demo_MiddleBury_slowmotion.py --netName DAIN_slowmotion --time_step 0.25

or set `time_step` to `0.125` or `0.1` as follows 

    $ CUDA_VISIBLE_DEVICES=0 python demo_MiddleBury_slowmotion.py --netName DAIN_slowmotion --time_step 0.125
    $ CUDA_VISIBLE_DEVICES=0 python demo_MiddleBury_slowmotion.py --netName DAIN_slowmotion --time_step 0.1
to generate x8 and x10 slow-motion respectively. Or if you would like to have x100 slow-motion for a little fun.
    
    $ CUDA_VISIBLE_DEVICES=0 python demo_MiddleBury_slowmotion.py --netName DAIN_slowmotion --time_step 0.01

You may also want to create gif animations by:
    
    $ cd MiddleBurySet/other-result-author/[random number]/Beanbags
    $ convert -delay 1 *.png -loop 0 Beanbags.gif //1*10ms delay 

Have fun and enjoy yourself! 


### Training New Models
Download the Vimeo90K triplet dataset for video frame interpolation task, also see [here](https://github.com/anchen1011/toflow/blob/master/download_dataset.sh) by [Xue et al., IJCV19](https://arxiv.org/abs/1711.09078).
    
    $ cd DAIN
    $ mkdir /path/to/your/dataset & cd /path/to/your/dataset 
    $ wget http://data.csail.mit.edu/tofu/dataset/vimeo_triplet.zip
    $ unzip vimeo_triplet.zip
    $ rm vimeo_triplet.zip

Download the pretrained MegaDepth and PWCNet models
    
    $ cd MegaDepth/checkpoints/test_local
    $ wget http://vllab1.ucmerced.edu/~wenbobao/DAIN/best_generalization_net_G.pth
    $ cd ../../../PWCNet
    $ wget http://vllab1.ucmerced.edu/~wenbobao/DAIN/pwc_net.pth.tar
    $ cd  ..
    
Run the training script:

    $ CUDA_VISIBLE_DEVICES=0 python train.py --datasetPath /path/to/your/dataset --batch_size 1 --save_which 1 --lr 0.0005 --rectify_lr 0.0005 --flow_lr_coe 0.01 --occ_lr_coe 0.0 --filter_lr_coe 1.0 --ctx_lr_coe 1.0 --alpha 0.0 1.0 --patience 4 --factor 0.2
    
The optimized models will be saved to the `model_weights/[random number]` directory, where [random number] is generated for different runs.

Replace the pre-trained `model_weights/best.pth` model with the newly trained `model_weights/[random number]/best.pth` model.
Then test the new model by executing: 

    $ CUDA_VISIBLE_DEVICES=0 python demo_MiddleBury.py


### License
See [MIT License](https://github.com/baowenbo/DAIN/blob/master/LICENSE)
