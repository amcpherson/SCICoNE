
yum install make git -y
yum install centos-release-scl -y
yum install devtoolset-9-gcc-c++ devtoolset-9-libasan-devel -y

conda config --set always_yes true
conda install conda-build
conda install -f python

scl enable devtoolset-9 conda/conda_build.sh

conda install anaconda-client
anaconda -t $CONDA_UPLOAD_TOKEN upload /usr/local/conda-bld/linux-64/scicone*.tar.bz2
