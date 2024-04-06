#!/bin/bash

python3 setup.py sdist bdist_wheel

# Test the package after it has been built with the following command
# pip install dist/<wheel_file>/whl
# The file will be auto-generated dependent upon the version number set
# in setup.py in the root directory. Use the correct file name when
# locally installing to test.