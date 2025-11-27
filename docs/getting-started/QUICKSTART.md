# Quick Start Guide

## 🚀 Get Started in 3 Minutes

### Option 1: See the Algorithm Demo (No Installation Required)

```bash
python demo_algorithm.py
```

This shows how the matching algorithm works with a step-by-step example.

### Option 2: Run the Core Platform (No AWS Required)

**Step 1: Install core dependencies**
```bash
pip install streamlit pandas numpy scikit-learn
```

**Step 2: Generate data** (already done if you see files in `data/`)
```bash
python src/generate_data.py
```

**Step 3: Launch the web app**
```bash
streamlit run app.py
```

Open your browser to `http://localhost:8501`

### Option 3: Run with Voice Features (AWS Required)

**Step 1: Install all dependencies**
```bash
pip install -r requirements.txt
```

**Step 2: Generate data** (already done if you see files in `data/`)
```bash
python src/generate_data.py
```

**Step 3: Launch the web app**

**Standard version:**
```bash
streamlit run app.py
```

**Voice-enabled version (with in-browser recording):**
```bash
streamlit run app_voice.py
```

Open your browser to `http://localhost:8501`

### Option 3: Test the Matching Engine

```bash
python test_matching.py
```

This runs a sample household through the matching algorithm and shows results in the terminal.

### Option 4: Voice Features Demo

```bash
python demo_conversation.py
```

Shows example conversational intake scenarios.

## 📁 What's Included

```
homelessness_hackathon/
├── app.py                      # Streamlit web application
├── demo_algorithm.py           # Algorithm demo (no dependencies)
├── test_matching.py            # Test script for matching engine
├── requirements.txt            # Python dependencies
├── setup.sh                    # Automated setup script
│
├── src/
│   ├── matching_engine.py      # Core matching algorithm
│   └── generate_data.py        # CSV data generator
│
├── data/
│   ├── household_data.csv      # 7 dummy households
│   └── property_data.csv       # 15 dummy properties
│
├── README.md                   # Full documentation
├── INSTALLATION.md             # Detailed installation guide
└── QUICKSTART.md               # This file
```

## 🎯 Key Features

- ✅ **In-browser audio recording** - Record directly in the app
- ✅ **Conversational intake** - Caseworker-family dialogue
- ✅ **Speaker diarization** - Automatic speaker identification
- ✅ Weighted scoring algorithm (location-first)
- ✅ 42-day emergency accommodation limit enforcement
- ✅ UK bedroom standard compliance
- ✅ Accessibility requirements (wheelchair, ground floor, etc.)
- ✅ Budget constraints
- ✅ School and healthcare proximity
- ✅ Transparent scoring with explanations

## 📊 Sample Data

**7 Households** including:
- Family with wheelchair needs approaching 42-day limit
- Single parent exceeding 42-day limit (URGENT)
- Domestic violence survivor at 42-day limit
- Person in recovery needing support services

**15 Properties** across:
- North, East, South, West, and Central London
- 1-4 bedrooms
- £450-£1100/month rent
- Various accessibility features

## 🔍 How It Works

1. **Input**: User fills in household details (composition, area, budget, needs)
2. **Matching**: Algorithm scores each property using weighted criteria
3. **Output**: Top 3 recommendations with explanations and flags

**Scoring Weights:**
- Location: 35% (highest)
- Bedrooms: 25%
- Affordability: 20%
- Access needs: 15%
- Amenities: 5%

## 💡 Example Usage

1. Open the web app: `streamlit run app.py`
2. Fill in the form:
   - Household: "2 adults, 2 children"
   - Area: "North London"
   - Budget: £800
   - Access: "Wheelchair access"
   - Schools: "Primary school required"
3. Click "Find Suitable Accommodation"
4. Review top 3 recommendations with scores and explanations

## 🆘 Troubleshooting

**"Module not found" error?**
```bash
pip install -r requirements.txt
```

**"Property data not found" error?**
```bash
python src/generate_data.py
```

**Port 8501 already in use?**
```bash
streamlit run app.py --server.port 8502
```

**"AttributeError: 'float' object has no attribute 'lower'" error?**
This has been fixed! See BUGFIX.md for details. Make sure you have the latest code.

**"Couldn't find ffmpeg" warning?**
Install ffmpeg for in-browser recording:
```bash
# macOS
brew install ffmpeg

# Ubuntu/Debian
sudo apt-get install ffmpeg
```
See IN_BROWSER_RECORDING.md for details.

## 📚 Learn More

- **README.md** - Full documentation and algorithm details
- **INSTALLATION.md** - Detailed installation instructions
- **demo_algorithm.py** - See how the algorithm works

## 🎓 Understanding the Algorithm

Run the demo to see a detailed walkthrough:
```bash
python demo_algorithm.py
```

This explains:
- How each property is scored
- Why location has the highest weight
- How the 42-day limit is enforced
- Why weighted scoring beats ML for this use case

## ✅ Next Steps

After getting started:
1. Try different household scenarios
2. Modify the dummy data in `src/generate_data.py`
3. Adjust scoring weights in `src/matching_engine.py`
4. Explore the code to understand the implementation

## 📞 Need Help?

See the full documentation in README.md or check INSTALLATION.md for detailed setup instructions.
