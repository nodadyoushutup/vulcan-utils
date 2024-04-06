#!/bin/bash
# publish.sh

# Check if an argument was provided
if [ $# -eq 0 ]; then
    echo "No arguments provided. Please specify 'major', 'minor', or 'patch'."
    exit 1
fi

python3 update_version.py $1

# Run the pip.sh script before uploading
./pip.sh

# Check if pip.sh succeeded
if [ $? -ne 0 ]; then
    echo "pip.sh failed, aborting publish."
    exit 1
fi

# Run the twine.sh script before uploading
./twine.sh

# Check if twine.sh succeeded
if [ $? -ne 0 ]; then
    echo "twine.sh failed, aborting publish."
    exit 1
fi