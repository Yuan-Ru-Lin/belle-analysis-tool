#!/bin/bash

export PYTHONPATH=$PYTHONPATH:$(pwd)/src/
python3 -m pytest

