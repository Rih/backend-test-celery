#!/bin/bash

# container=$1
docker exec -it $(docker-compose ps -q backend) bash



