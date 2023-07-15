#!/bin/sh

# if any of the commands in your code fails the entire scripts fails.
set -o errexit

# exit if any of your variables is not set.
set -o nounset

set -x

# Clear Python caches
find . -name "*.pyc" -exec rm -f {} \;

# fastapi command
python main.py

exec "$@"