#!/usr/bin/env bash

# Build image
docker build --tag=demolocal .

# List docker images
docker image ls

# Run sentiment app
docker run -it demolocal bash