#!/bin/bash

# Requires a twine_creds.sh credentials file to upload to PyPI
source twine_creds.sh
twine upload dist/*