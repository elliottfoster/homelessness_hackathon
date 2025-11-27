#!/bin/bash
# Setup script for Temporary Accommodation Matching Platform

echo "🏠 Setting up Temporary Accommodation Matching Platform..."
echo ""

# Check Python version
echo "Checking Python version..."
python --version

# Install dependencies
echo ""
echo "Installing dependencies..."
pip install -r requirements.txt

# Generate data
echo ""
echo "Generating dummy data..."
python src/generate_data.py

echo ""
echo "✅ Setup complete!"
echo ""
echo "To run the application:"
echo "  streamlit run app.py"
