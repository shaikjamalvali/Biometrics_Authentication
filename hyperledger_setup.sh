#!/bin/bash

# Hyperledger Fabric 2.5 Setup Script for Linux
# This script installs all prerequisites and Fabric components

set -e  # Exit on any error

echo "=========================================="
echo "Hyperledger Fabric 2.5 Setup Script"
echo "=========================================="
echo ""

# Color codes for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Step 1: Update system packages
print_info "Step 1: Updating system packages..."
sudo apt-get update -y
sudo apt-get upgrade -y
print_success "System packages updated"
echo ""

# Step 2: Install Git
print_info "Step 2: Installing Git..."
if command -v git &> /dev/null; then
    print_warning "Git is already installed: $(git --version)"
else
    sudo apt-get install -y git
    print_success "Git installed: $(git --version)"
fi
echo ""

# Step 3: Install cURL
print_info "Step 3: Installing cURL..."
if command -v curl &> /dev/null; then
    print_warning "cURL is already installed: $(curl --version | head -n1)"
else
    sudo apt-get install -y curl
    print_success "cURL installed"
fi
echo ""

# Step 4: Install Docker
print_info "Step 4: Installing Docker..."
if command -v docker &> /dev/null; then
    print_warning "Docker is already installed: $(docker --version)"
else
    curl -fsSL https://get.docker.com -o get-docker.sh
    sudo sh get-docker.sh
    rm get-docker.sh
    print_success "Docker installed: $(docker --version)"
fi
echo ""

# Step 5: Install Docker Compose
print_info "Step 5: Installing Docker Compose..."
if command -v docker-compose &> /dev/null; then
    print_warning "Docker Compose is already installed: $(docker-compose --version)"
else
    sudo apt-get install -y docker-compose
    print_success "Docker Compose installed: $(docker-compose --version)"
fi
echo ""

# Step 6: Configure Docker (allow non-root user)
print_info "Step 6: Configuring Docker for non-root user..."
if groups $USER | grep -q docker; then
    print_warning "User is already in docker group"
else
    sudo usermod -a -G docker $USER
    print_info "User added to docker group. You may need to log out and log back in."
fi
echo ""

# Step 7: Start Docker daemon
print_info "Step 7: Starting Docker daemon..."
sudo systemctl start docker
print_success "Docker daemon started"
echo ""

# Step 8: Install Go (Optional but recommended)
print_info "Step 8: Installing Go (Optional)..."
if command -v go &> /dev/null; then
    print_warning "Go is already installed: $(go version)"
else
    # Install latest stable Go version
    GO_VERSION="1.21.0"  # Update this as needed
    sudo apt-get install -y golang-go
    print_success "Go installed: $(go version)"
fi
echo ""

# Step 9: Install Node.js (Optional but recommended)
print_info "Step 9: Installing Node.js and npm (Optional)..."
if command -v node &> /dev/null; then
    print_warning "Node.js is already installed: $(node --version)"
else
    curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
    sudo apt-get install -y nodejs
    print_success "Node.js installed: $(node --version)"
    print_success "npm installed: $(npm --version)"
fi
echo ""

# Step 10: Install jq (Optional but useful for tutorials)
print_info "Step 10: Installing jq (Optional)..."
if command -v jq &> /dev/null; then
    print_warning "jq is already installed: $(jq --version)"
else
    sudo apt-get install -y jq
    print_success "jq installed: $(jq --version)"
fi
echo ""

# Step 11: Create Fabric directory
print_info "Step 11: Creating Hyperledger Fabric directory..."
FABRIC_DIR="${HOME}/hyperledger-fabric"
mkdir -p "$FABRIC_DIR"
cd "$FABRIC_DIR"
print_success "Fabric directory created at: $FABRIC_DIR"
echo ""

# Step 12: Download Fabric and Fabric Samples
print_info "Step 12: Downloading Hyperledger Fabric v2.5..."
if [ ! -d "fabric-samples" ]; then
    curl -sSL https://bit.ly/2ysbOFE | bash -s -- 2.5.0 1.5.0
    print_success "Fabric and Samples downloaded"
else
    print_warning "Fabric samples directory already exists"
fi
echo ""

# Step 13: Add Fabric binaries to PATH
print_info "Step 13: Adding Fabric binaries to PATH..."
FABRIC_PATH="$FABRIC_DIR/fabric-samples/bin"
if grep -q "fabric-samples/bin" ~/.bashrc; then
    print_warning "PATH already contains fabric-samples/bin"
else
    echo "" >> ~/.bashrc
    echo "# Hyperledger Fabric" >> ~/.bashrc
    echo "export PATH=\"\$PATH:$FABRIC_PATH\"" >> ~/.bashrc
    print_success "PATH updated in ~/.bashrc"
    print_info "Run: source ~/.bashrc"
fi
echo ""

# Step 14: Verify installation
print_info "Step 14: Verifying installation..."
echo ""
echo "Docker version:"
docker --version
echo ""
echo "Docker Compose version:"
docker-compose --version
echo ""
echo "Git version:"
git --version
echo ""
echo "cURL version:"
curl --version | head -n1
echo ""

if command -v go &> /dev/null; then
    echo "Go version:"
    go version
    echo ""
fi

if command -v node &> /dev/null; then
    echo "Node.js version:"
    node --version
    echo "npm version:"
    npm --version
    echo ""
fi

print_success "All prerequisites installed!"
echo ""

# Step 15: Display next steps
echo "=========================================="
echo "Setup Complete!"
echo "=========================================="
echo ""
echo "Next steps:"
echo "1. Log out and log back in (to apply docker group changes)"
echo "2. Navigate to Fabric Samples:"
echo "   cd $FABRIC_DIR/fabric-samples"
echo "3. Start the test network:"
echo "   cd test-network"
echo "   ./network.sh up"
echo ""
echo "Documentation: https://hyperledger-fabric.readthedocs.io/en/release-2.5/"
echo ""
