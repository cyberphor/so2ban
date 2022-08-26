#!/bin/bash

wget https://github.com/ktbyers/netmiko/archive/refs/tags/v4.0.0.tar.gz
gunzip v4.0.0.tar.gz
tar -xf v4.0.0.tar
rm v4.0.0.tar
mv netmiko-4.0.0 netmiko
sed -i '/^    install_requires=\[/a\        "setuptools_scm",' netmiko/setup.py
pip3 download -e netmiko --no-binary :all: --no-cache-dir