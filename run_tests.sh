#!/bin/bash

export PYTHONPATH=$PYTHONPATH:$(pwd)/src/
python -m pytest

