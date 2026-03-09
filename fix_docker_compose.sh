#!/bin/bash

# Fix Docker Compose version for Hyperledger Fabric v2.5.0
# This script upgrades Docker Compose to v2.x which is required

set -e

echo "=============================================="
echo "Docker Compose Upgrade Script"
echo "=============================================="
echo ""

# Check current version
echo "Current Docker Compose version:"
docker-compose --version
echo ""

# Get the latest Docker Compose v2 version
echo "Fetching latest Docker Compose v2.x..."
LATEST=$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d'"' -f4)
echo "Latest version: $LATEST"
echo ""

# Download and install Docker Compose v2
echo "Downloading Docker Compose $LATEST..."
curl -L "https://github.com/docker/compose/releases/download/$LATEST/docker-compose-$(uname -s)-$(uname -m)" -o docker-compose

echo "Making it executable..."
chmod +x docker-compose

echo "Moving to /usr/local/bin..."
echo "Jv@123" | sudo -S mv docker-compose /usr/local/bin/docker-compose

echo ""
echo "Verifying installation..."
docker-compose --version
echo ""
echo "✅ Docker Compose upgraded successfully!"
echo ""
echo "Now try running:"
echo "cd ~/hyperledger-fabric/fabric-samples/test-network"
echo "./network.sh up"
