
yum install make git -y
yum install centos-release-scl -y
yum install devtoolset-9-gcc-c++ devtoolset-9-libasan-devel -y

conda config --set always_yes true
conda install conda-build
conda install -f python

scl enable devtoolset-9 conda/conda_build.sh

# anaconda client currently broken with python 3.9
conda create -n anacondaclient python=3.8 anaconda-client
/usr/local/envs/anacondaclient/bin/anaconda -t $CONDA_UPLOAD_TOKEN upload /usr/local/conda-bld/linux-64/scicone*.tar.bz2
