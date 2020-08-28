#!/bin/sh
set -e

export RES_ROOT_DATA_PATH=$1
python -m importers.djornl.parser validate
