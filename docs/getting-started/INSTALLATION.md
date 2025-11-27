# Installation Guide

## Prerequisites

### Core Requirements (Required)
- Python 3.11 or higher
- pip package manager
- 100MB free disk space
- Modern web browser

### Optional Requirements (For Voice Features)
- AWS account with Transcribe access
- ffmpeg (for in-browser recording)
- Additional Python packages: boto3, streamlit-audiorecorder, pydub

**Note:** The core platform works without AWS or voice features. Voice capabilities are optional.

## Quick Start (3 Steps)

### Step 1: Install Dependencies

Choose one of the following methods:

**Option A - Core dependencies only (no voice features):**
```bash
pip install streamlit pandas numpy scikit-learn
```

**Option B - All dependencies (including voice features):**
```bash
pip install -r requirements.txt
```

**Option C - Using the setup script:**
```bash
chmod +x setup.sh
./setup.sh
```

### Step 2: Generate Data (if not already done)

```bash
python src/generate_data.py
```

This creates:
- `data/household_data.csv` - 7 dummy households
- `data/property_data.csv` - 15 dummy properties

### Step 3: Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Testing Without Streamlit

To test the matching engine without the web interface:

```bash
python test_matching.py
```

This runs a sample household through the matching algorithm and displays results in the terminal.

## Troubleshooting

### Python Version Issues

The project requires Python 3.11+. Check your version:
```bash
python --version
```

If using pyenv:
```bash
pyenv local 3.11
```

### Module Not Found Errors

If you see `ModuleNotFoundError`, install dependencies:
```bash
pip install -r requirements.txt
```

### Data Files Missing

If the app says "Property data not found":
```bash
python src/generate_data.py
```

### Port Already in Use

If port 8501 is busy, specify a different port:
```bash
streamlit run app.py --server.port 8502
```

## System Requirements

- Python 3.11 or higher
- 100MB free disk space
- Modern web browser (Chrome, Firefox, Safari, Edge)
- Internet connection (for initial package installation only)

## Dependencies

### Core Dependencies (Required)
- `streamlit>=1.28.0` - Web application framework
- `pandas>=2.0.0` - Data manipulation
- `numpy>=1.24.0` - Numerical operations
- `scikit-learn>=1.3.0` - ML utilities (for future enhancements)

### Optional Dependencies (Voice Features)
- `boto3>=1.28.0` - AWS SDK for Python (Amazon Transcribe)
- `streamlit-audiorecorder>=0.0.5` - In-browser audio recording
- `pydub>=0.25.1` - Audio processing

### System Dependencies (Optional)
- `ffmpeg` - Required for in-browser audio recording
  - macOS: `brew install ffmpeg`
  - Ubuntu/Debian: `sudo apt-get install ffmpeg`
  - Windows: Download from https://ffmpeg.org/download.html

## Next Steps

After installation, see README.md for:
- Usage instructions
- Algorithm explanation
- Data schema details
- Example scenarios
