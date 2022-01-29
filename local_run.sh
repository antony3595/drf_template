#!/bin/bash

echo "Running DRF API template .. "

docker-compose -f docker/docker-compose-utils.yml up -d
docker-compose -f docker/docker-compose-servers.yml up -d