#!/bin/bash

# Install Tesseract OCR
echo "🔍 Installing Tesseract OCR..."
apt-get update
apt-get install -y tesseract-ocr

# Install Python dependencies
echo "📦 Installing Python dependencies..."
pip install -r requirements.txt

echo "✅ Build complete!"
