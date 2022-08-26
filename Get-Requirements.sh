#!/bin/bash

wget https://github.com/ktbyers/netmiko/archive/refs/tags/v4.0.0.tar.gz
gunzip v4.0.0.tar.gz
tar -xf v4.0.0.tar
rm v4.0.0.tar
mv netmiko-4.0.0 netmiko
cd netmiko
sed -i '/^    install_requires=\[/a\        "setuptools_scm",' setup.py
pip3 download -r requirements.txt --no-binary :all: --no-cache-dir
