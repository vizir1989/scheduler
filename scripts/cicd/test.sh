#!/bin/sh

set -e
set -x

pytest \
    --numprocesses 4 \
    --cov . \
    --cov-report xml \
    --no-cov-on-fail \
    tests

coverage report --skip-covered --show-missing
