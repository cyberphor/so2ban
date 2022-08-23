#!/bin/bash

wget https://github.com/ktbyers/netmiko/archive/refs/tags/v4.0.0.tar.gz -O netmiko.tar.gz
gunzip netmiko.tar.gz
tar -xf netmiko.tar
cd netmiko 
pip3 download -r requirements.txt --no-binary=:all: -d dependencies
