#!/bin/bash
set -e

# Build the Spring Boot JAR
./mvnw clean package

# Build the Docker image
docker build -t springdemo-app .

# Run the Docker container, mapping port 8080
# Remove any existing container with the same name first
docker rm -f springdemo-app-running 2>/dev/null || true
docker run --name springdemo-app-running -p 8080:8080 springdemo-app
