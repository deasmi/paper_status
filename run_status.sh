#!/bin/bash

SCRIPT_DIR=$( cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd )

cd $SCRIPT_DIR

. ./venv/bin/activate

python3 >/tmp/status_output 2>&1 ./status.py
