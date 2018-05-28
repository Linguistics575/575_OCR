#!/bin/bash
# Script to setup virtual environment for Azure Handwriting Recognition Tools
# Author: James V. Bruno
# Date: 5/27/2018

# make sure we have a good python 3 interpreter
# first we see if we have it with just 'python'
if pyversion=$(python --version 2>&1); then
    if [[ $pyversion = "Python 3"* ]]; then
            echo "Found Python 3 interpeter with python command"
            pycmd=python
    else
        if pyversion=$(python3 --version 2>&1); then
            
            echo "Found Python 3 interpeter with python3 command"
            pycmd=python3
        else
            echo "It seems that only Python 2 is installed on this system."
            echo "Please install Python 3 and try again."
            exit 0
        fi
    fi
else
    echo "It does not seem that python is installed on this system."
    echo "Please install Python 3 and try again."
    exit 0
fi

echo "setting up azure_environment..."
$pycmd -m venv azure_environment

ln ./azure_environment/bin/activate activate -sf
echo "activating environment..."
source ./activate

echo "installing packages from requirements file."
echo "This may take some time."

pip install -r requirements.txt

echo "downloading Natural Language Toolkit Resources"
python -m nltk.downloader perluniprops

echo "setup of environment complete"

echo "to activate envrionment, type \"source activate\""
echo "to deactivate, type \"deactivate\""
