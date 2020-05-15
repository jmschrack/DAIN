#!/usr/bin/env bash

echo "Need pytorch>=1.0.0"
source activate pytorch1.0.0

cd MinDepthFlowProjection
rm -rf build *.egg-info dist
python3 setup.py install --user
cd ..

cd FlowProjection
rm -rf build *.egg-info dist
python3 setup.py install --user
cd ..

cd SeparableConv
rm -rf build *.egg-info dist
python3 setup.py install --user
cd ..

cd InterpolationCh
rm -rf build *.egg-info dist
python3 setup.py install --user
cd ..

cd DepthFlowProjection
rm -rf build *.egg-info dist
python3 setup.py install --user
cd ..

cd Interpolation
rm -rf build *.egg-info dist
python3 setup.py install --user
cd ..

cd SeparableConvFlow
rm -rf build *.egg-info dist
python3 setup.py install --user
cd ..

cd FilterInterpolation
rm -rf build *.egg-info dist
python3 setup.py install --user
cd ..

