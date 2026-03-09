#!/usr/bin/env pwsh

# PowerShell script to fix Docker Compose in WSL from Windows
# This script handles the sudo password automatically

Write-Host "════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "Docker Compose v2 Upgrade for Hyperledger Fabric" -ForegroundColor Cyan
Write-Host "════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host ""

# Password (already provided by user)
$password = "Jv@123"

Write-Host "Step 1: Checking current Docker Compose version..." -ForegroundColor Yellow
wsl bash -c "docker-compose --version"
Write-Host ""

Write-Host "Step 2: Getting latest Docker Compose v2..." -ForegroundColor Yellow
wsl bash -c @"
LATEST=`$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d'"' -f4)
echo "Latest version: `$LATEST"
"@
Write-Host ""

Write-Host "Step 3: Downloading Docker Compose v2..." -ForegroundColor Yellow
wsl bash -c @"
LATEST=`$(curl -s https://api.github.com/repos/docker/compose/releases/latest | grep 'tag_name' | cut -d'"' -f4)
echo "Downloading from: https://github.com/docker/compose/releases/download/`$LATEST/docker-compose-Linux-x86_64"
cd /tmp
curl -L "https://github.com/docker/compose/releases/download/`$LATEST/docker-compose-`$(uname -s)-`$(uname -m)" -o docker-compose
chmod +x docker-compose
echo "Downloaded successfully"
"@
Write-Host ""

Write-Host "Step 4: Installing to /usr/local/bin..." -ForegroundColor Yellow
# Create a script that handles the password
$sudoScript = @"
#!/bin/bash
echo "$password" | sudo -S cp /tmp/docker-compose /usr/local/bin/docker-compose
echo "$password" | sudo -S chmod +x /usr/local/bin/docker-compose
"@

# Save the script temporarily
$scriptPath = "/tmp/install-compose.sh"
wsl bash -c "echo '$sudoScript' > $scriptPath && chmod +x $scriptPath && $scriptPath"
Write-Host ""

Write-Host "Step 5: Verifying installation..." -ForegroundColor Yellow
wsl bash -c "docker-compose --version"
Write-Host ""

Write-Host "✅ Docker Compose upgraded successfully!" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Cyan
Write-Host "1. Run: wsl -e bash -c 'cd ~/hyperledger-fabric/fabric-samples/test-network && ./network.sh up'" -ForegroundColor White
Write-Host ""
