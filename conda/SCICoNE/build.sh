#!/bin/bash

BINS='breakpoint_detection inference save_root_per_nu score simulation tests'

# Build the executables using cmake
# NOTE: python build cannot happen after cmake
mkdir -p build
cd build
cmake ..
make

# Install executables, bin directory not guaranteed to exist during build
mkdir -p $PREFIX/bin
cp $BINS $PREFIX/bin
