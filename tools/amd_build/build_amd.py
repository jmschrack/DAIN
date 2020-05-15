#!/usr/bin/env python

from __future__ import absolute_import, division, print_function
import os
import subprocess
import argparse
import sys
sys.path.append(os.path.realpath(os.path.join(
    __file__,
    os.path.pardir,
    os.path.pardir,
    os.path.pardir,
    'utils')))

from hipify import hipify_python

parser = argparse.ArgumentParser(description='Top-level script for HIPifying, filling in most common parameters')
parser.add_argument(
    '--out-of-place-only',
    action='store_true',
    help="Whether to only run hipify out-of-place on source files")

parser.add_argument(
    '--project-directory',
    type=str,
    default='',
    help="The root of the project.",
    required=False)

parser.add_argument(
    '--output-directory',
    type=str,
    default='',
    help="The directory to store the hipified project",
    required=False)

parser.add_argument(
    '--extra-include-dir',
    type=str,
    default=[],
    nargs='+',
    help="The list of extra directories in caffe2 to hipify",
    required=False)

args = parser.parse_args()

amd_build_dir = os.path.dirname(os.path.realpath(__file__))
proj_dir = os.path.join(os.path.dirname(os.path.dirname(amd_build_dir)))

if args.project_directory:
    proj_dir = args.project_directory

out_dir = proj_dir
if args.output_directory:
    out_dir = args.output_directory

includes = [
    "my_package/DepthFlowProjection/*",
    "my_package/FilterInterpolation/*",
    "my_package/FlowProjection/*",
    "my_package/Interpolation/*",
    "my_package/InterpolationCh/*",
    "my_package/MinDepthFlowProjection/*",
    "my_package/SeparableConv/*",
    "my_package/SeparableConvFlow/*",
    "PWCNet/correlation_package_pytorch1_0/*",
]

for new_dir in args.extra_include_dir:
    abs_new_dir = os.path.join(proj_dir, new_dir)
    if os.path.exists(abs_new_dir):
        new_dir = os.path.join(new_dir, '**/*')
        includes.append(new_dir)

ignores = [
]

if not args.out_of_place_only:
    # Apply patch files in place (PyTorch only)
    patch_folder = os.path.join(amd_build_dir, "patches")
    for filename in os.listdir(os.path.join(amd_build_dir, "patches")):
        subprocess.Popen(["git", "apply", os.path.join(patch_folder, filename)], cwd=proj_dir)

# Check if the compiler is hip-clang.
def is_hip_clang():
    try:
        hip_path = os.getenv('HIP_PATH', '/opt/rocm/hip')
        return 'HIP_COMPILER=clang' in open(hip_path + '/lib/.hipInfo').read()
    except IOError:
        return False

hipify_python.hipify(
    project_directory=proj_dir,
    output_directory=out_dir,
    includes=includes,
    ignores=ignores,
    out_of_place_only=args.out_of_place_only,
    hip_clang_launch=is_hip_clang())
