#!/usr/bin/bash

set -euxo pipefail

echo "----------Releasing $(python setup.py --version) --------------"

echo -e "\n------------- Upgrading dependecies ---------------------\n"
python -m pip install -U pip
python -m pip install -U setuptools twine wheel

echo -e "\n------------- Building Package -----------------------\n"
python setup.py sdist bdist_wheel

echo -e "\n------------- Verifying Package ----------------------\n"
twine check dist/*

echo -e "\n------------- Publishing Package ----------------------\n"
twine upload dist/*
