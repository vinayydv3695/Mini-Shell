#!/bin/bash

# Mini Shell Setup Script
# This script sets up Mini Shell on any Linux/macOS machine

echo "=========================================="
echo "  Mini Shell Setup"
echo "=========================================="
echo ""

# Check Python version
echo "Checking Python version..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed!"
    echo "Please install Python 3.6 or higher"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo "✅ Found Python $PYTHON_VERSION"
echo ""

# Check if virtual environment exists
if [ -d "venv" ]; then
    echo "⚠️  Virtual environment already exists"
    read -p "Do you want to recreate it? (y/n) " -n 1 -r
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        echo "Removing old virtual environment..."
        rm -rf venv
    else
        echo "Using existing virtual environment"
    fi
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        echo "✅ Virtual environment created"
    else
        echo "❌ Failed to create virtual environment"
        exit 1
    fi
fi
echo ""

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate
echo "✅ Virtual environment activated"
echo ""

# Install requirements (if any)
if [ -f "requirements.txt" ]; then
    echo "Installing requirements..."
    pip install --upgrade pip
    pip install -r requirements.txt
    echo "✅ Requirements installed"
else
    echo "ℹ️  No requirements.txt found (Mini Shell uses standard library only)"
fi
echo ""

# Make mini_shell.py executable
echo "Making mini_shell.py executable..."
chmod +x mini_shell.py
echo "✅ mini_shell.py is now executable"
echo ""

# Success message
echo "=========================================="
echo "  Setup Complete! 🎉"
echo "=========================================="
echo ""
echo "To start Mini Shell:"
echo "  1. Activate virtual environment: source venv/bin/activate"
echo "  2. Run the shell: python3 mini_shell.py"
echo "     or simply: ./mini_shell.py"
echo ""
echo "To deactivate virtual environment later: deactivate"
echo ""
