#!/bin/bash

echo "Building drf_template image"
docker build -f Dockerfile --rm -t drf_template:1 .
docker images