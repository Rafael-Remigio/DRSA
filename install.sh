#!/bin/bash

echo "Downloading Argon2 package"
wget -O /tmp/argon2_cffi-23.1.0-py3-none-any.whl  https://files.pythonhosted.org/packages/a4/6a/e8a041599e78b6b3752da48000b14c8d1e8a04ded09c88c714ba047f34f5/argon2_cffi-23.1.0-py3-none-any.whl
echo "Installing Packages"
pip install /tmp/argon2_cffi-23.1.0-py3-none-any.whl 
pip install -r requirments.txt

echo "Removing created files"
rm /tmp/argon2_cffi-23.1.0-py3-none-any.whl 

# here because pycrypto got discontinued for python 3.8
pip uninstall pycrypto
pip install pycryptodome