#!/bin/bash

# Quick Start Script for Mini Shell
# Run this script to start Mini Shell with virtual environment

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "❌ Virtual environment not found!"
    echo "Please run setup.sh first:"
    echo "  bash setup.sh"
    exit 1
fi

# Activate virtual environment
source venv/bin/activate

# Run Mini Shell
python3 mini_shell.py

# Deactivate when done
deactivate
