#!/bin/bash

python blog.py create testblog
cd testblog

python ../blog.py post hello-worlds
python ../blog.py build

tree

python ../blog.py serve

cd ../
rm -rf testblog