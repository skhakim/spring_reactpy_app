#!/bin/bash

# Build and run Name Lookup ReactPy Docker container

set -e

# Check Docker
command -v docker &> /dev/null || { echo "Docker not installed"; exit 1; }

# Check files
[ -f "name_lookup.py" ] || { echo "name_lookup.py not found"; exit 1; }
[ -f "Dockerfile" ] || { echo "Dockerfile not found"; exit 1; }

# Build and run
docker build -t name-lookup-app .
docker run -d --add-host=host.docker.internal:host-gateway -p 4100:4000 name-lookup-app

echo "App running at http://localhost:4100"
