#!/bin/bash
echo "[+] Setting up SIMURAZXTR v1.0"

# Create directory structure
mkdir -p core modules utils config data reports

# Install dependencies
pip3 install -r requirements.txt

# Set execution permissions
chmod +x main.py

echo "[+] Installation complete!"
echo "[+] Usage: python3 main.py -t <target> -m <mode>"