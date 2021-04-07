#!/bin/bash

BINS='breakpoint_detection inference save_root_per_nu score simulation tests'

# Build and install python package
cd pyscicone
$PYTHON setup.py install --single-version-externally-managed --record=record.txt
cd ..

# Build the executables using cmake
# NOTE: python build cannot happen after cmake
mkdir build && cd build
cmake ..
make

# Install executables, bin directory not guaranteed to exist during build
cp $BINS $PREFIX/bin
