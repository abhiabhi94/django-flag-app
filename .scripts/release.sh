#!/usr/bin/bash
set -e

rm -rf dist build
python -m pip install -U pip
python -m pip install -U setuptools wheel twine
python setup.py sdist bdist_wheel
twine check dist/*
python -m twine upload dist/*
