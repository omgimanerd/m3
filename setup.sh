#!/bin/bash

export PYTHONPATH="$PYTHONPATH:$(dirname "$(realpath -- $0)")"
echo $PYTHONPATH
