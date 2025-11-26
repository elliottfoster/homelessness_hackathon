# Installation Guide

## Quick Start (3 Steps)

### Step 1: Install Dependencies

Choose one of the following methods:

**Option A - Using pip:**
```bash
pip install -r requirements.txt
```

**Option B - Using the setup script:**
```bash
chmod +x setup.sh
./setup.sh
```

**Option C - Manual installation:**
```bash
pip install streamlit pandas numpy scikit-learn
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

- `streamlit` - Web application framework
- `pandas` - Data manipulation
- `numpy` - Numerical operations
- `scikit-learn` - ML utilities (for future enhancements)

## Next Steps

After installation, see README.md for:
- Usage instructions
- Algorithm explanation
- Data schema details
- Example scenarios
