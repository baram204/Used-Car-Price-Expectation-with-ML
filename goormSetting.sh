#!/bin/bash

sudo add-apt-repository ppa:deadsnakes/ppa -y &&
sudo apt-get update &&
sudo apt-get install python3.6 -y &&

# https://beomi.github.io/2016/12/28/HowToSetup-Virtualenv-VirtualenvWrapper/
sudo pip install virtualenvwrapper --upgrade --ignore-installed six &&
find / -name *venv* &&
mkdir ~/.virtualenvs &&

# append it to .bashrc
cat >~/.bashrc >>EOL
# python virtualenv settings
export WORKON_HOME=~/.virtualenvs
export VIRTUALENVWRAPPER_PYTHON='$(command \which python3)'  # Usage of python3
source /usr/local/bin/virtualenvwrapper.sh
EOL &&
mkvirtualenv --python=/usr/bin/python3.6 flask
# below without wrapper
# virtualenv --python=/usr/bin/python3.6 flask && \

cat >/etc/myconfig.conf <<EOL