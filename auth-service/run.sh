#!/bin/bash

# Load environment variables from .env file
set -o allexport
source .env
set +o allexport

FASTAPI_PORT=${PORT:-5000}  # Default to 5001 if not set

# Stop and remove existing containers if they exist
echo "Stopping and removing existing containers..."
docker stop initial-auth-service postgres || true
docker rm initial-auth-service postgres || true

# Run PostgreSQL container
echo "Starting PostgreSQL container..."
docker run --name postgres \
    -e POSTGRES_USER=$POSTGRES_USER \
    -e POSTGRES_PASSWORD=$POSTGRES_PASSWORD \
    -e POSTGRES_DB=$POSTGRES_DB \
    -p 5432:5432 -d postgres

# Build the FastAPI application image
echo "Building FastApI application Docker image..."
docker build -t initial-auth-service .

# Run FastAPI application container
echo "Starting FastAPI application container..."
docker run --name initial-auth-service \
    --env-file .env \
    -p $FASTAPI_PORT:5000 \
    --link postgres:postgres \
    -d initial-auth-service

echo "Containers are up and running!"
