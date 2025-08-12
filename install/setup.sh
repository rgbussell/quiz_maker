#!/bin/bash

# Installer script for the Homework Quiz Generator app on Ubuntu Linux
# This script sets up a virtual environment, installs required dependencies,
# installs necessary libraries within the venv, and creates the app.py file using xAI's Grok API.
# Note: Tesseract OCR is a system-level dependency and cannot be installed directly within a Python virtual environment.
# It must be installed system-wide (via apt), while the Python wrapper (pytesseract) is installed in the venv.
# The venv will use the system-installed Tesseract binary.

# Exit on error
set -e

echo "Starting installation for Homework Quiz Generator on Ubuntu..."
echo "Note: Tesseract OCR will be installed system-wide, as it cannot be confined to the virtual environment."
echo "The Python interface (pytesseract) will be installed within the venv."

# Step 1: Update system packages
echo "Updating package list..."
sudo apt update -y

# Step 2: Install Python3, venv, and pip if not already installed
echo "Installing Python3 and venv..."
sudo apt install python3 python3-venv python3-pip -y

# Step 3: Install Tesseract OCR and dependencies (system-wide)
echo "Installing Tesseract OCR (system-wide)..."
sudo apt install tesseract-ocr libtesseract-dev tesseract-ocr-eng -y  # eng for English language pack; add more if needed

# Step 4: Create project directory
PROJECT_DIR="homework_quiz_app"
echo "Creating project directory: $PROJECT_DIR"
mkdir -p $PROJECT_DIR
cd $PROJECT_DIR

# Check if venv exists and delete it if it does
if [ -d "venv" ]; then
    echo "Existing venv found. Deleting..."
    rm -rf "$VENV_DIR"
fi

# Step 5: Create and activate virtual environment
echo "Creating virtual environment..."
python3 -m venv venv
source venv/bin/activate

# Step 6: Install Python libraries within venv
echo "Installing Python libraries in virtual environment..."
pip install streamlit pytesseract pillow xai-sdk
pip install openai python-dotenv

# Step 9: Prompt for xAI API key
echo "App setup complete! Now, edit app.py to add your xAI Grok API key."
echo "For details on obtaining an xAI API key and usage, visit https://x.ai/api"
echo "To edit, cd into $PROJECT_DIR, then source venv/bin/activate, and edit app.py."

# Step 10: Instructions to run the app
echo "To run the app:"
echo "1. cd $PROJECT_DIR"
echo "2. source venv/bin/activate"
echo "3. streamlit run app.py"
echo "This will open the app in your web browser. Ensure your webcam is enabled."

echo "Installation complete! 🎉"