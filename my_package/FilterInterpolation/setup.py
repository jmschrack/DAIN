#!/usr/bin/env python3
import os
import torch

from setuptools import setup, find_packages
from torch.utils.cpp_extension import BuildExtension, CUDAExtension

src = [
    'filterinterpolation_cuda.cc',
    'filterinterpolation_cuda_kernel.cu'
]

cxx_args = ['-std=c++14']

nvcc_args = [
    '-gencode', 'arch=compute_50,code=sm_50',
    '-gencode', 'arch=compute_52,code=sm_52',
    '-gencode', 'arch=compute_60,code=sm_60',
    '-gencode', 'arch=compute_61,code=sm_61'
    # '-gencode', 'arch=compute_70,code=sm_70',
    # '-gencode', 'arch=compute_70,code=compute_70'
]


hip_path = os.getenv('HIP_PATH', '/opt/rocm/hip')
# if HIP_PATH is valid, look for HIP variants.
if os.path.exists(hip_path):
    print('Found HIP_PATH. Looking for HIP variants')
    cxx_args.extend( os.popen(hip_path+'/bin/hipconfig --cpp_config').read().split())
    #nvcc args will be passed to hcc, the above args will cause an error
    nvcc_args=[]
    hip_src=[]
    for f in src:
        hs = "hip/"+f.replace("cuda","hip").replace(".cu",".hip")
        if os.path.exists(hs):
            print('Found:'+hs)
            hip_src.append(hs)
        else:
            hip_src.append(f)
    src=hip_src
        


setup(
    name='filterinterpolation_cuda',
    ext_modules=[
        CUDAExtension('filterinterpolation_cuda',src, extra_compile_args={'cxx': cxx_args, 'nvcc': nvcc_args})
    ],
    cmdclass={
        'build_ext': BuildExtension
    })
