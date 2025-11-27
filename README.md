# 🏠 Temporary Accommodation Matching Platform

A prototype platform for matching homeless households to suitable temporary accommodation in the UK context.

## Overview

This platform helps match homeless households to temporary accommodation using a transparent, weighted-scoring algorithm that prioritizes:
- Location preferences and area restrictions
- Bedroom suitability based on household composition
- Affordability within budget constraints
- Critical access needs (wheelchair, ground floor, etc.)
- Proximity to schools, healthcare, and support services

The system enforces UK homelessness policies, including the 42-day emergency accommodation limit for families.

## Features

- ✅ **In-browser audio recording** - Record conversations directly in the app (NEW!)
- ✅ **Conversational intake** - Caseworker-family dialogue with automatic speaker identification
- ✅ **Voice input** powered by Amazon Transcribe with speaker diarization
- ✅ Web-based form for household information input
- ✅ Weighted scoring algorithm (location-first approach)
- ✅ Top 3 property recommendations with detailed explanations
- ✅ Suitability flags for policy violations
- ✅ 42-day emergency accommodation limit warnings
- ✅ Transparent scoring breakdown for each property
- ✅ Complete dummy dataset (7 households, 15 properties)

## Technical Stack

- **Backend**: Python 3.11+
- **Web Framework**: Streamlit
- **Data Processing**: Pandas, NumPy
- **Voice Input**: Amazon Transcribe (AWS) with speaker diarization
- **Audio Recording**: streamlit-audiorecorder (in-browser)
- **Audio Processing**: ffmpeg
- **Data Storage**: Local CSV files

## Project Structure

```
homelessness_hackathon/
├── app.py                      # Main Streamlit application
├── src/
│   ├── matching_engine.py      # Weighted scoring algorithm
│   └── generate_data.py        # CSV data generation script
├── data/
│   ├── household_data.csv      # Dummy household data (generated)
│   └── property_data.csv       # Dummy property data (generated)
├── pyproject.toml              # Python dependencies
└── README.md                   # This file
```

## Installation & Setup

### Prerequisites
- Python 3.10 or higher
- pip or uv package manager

### Step 1: Install Dependencies

Using pip:
```bash
pip install streamlit pandas numpy scikit-learn
```

Or using uv (recommended):
```bash
uv pip install streamlit pandas numpy scikit-learn
```

### Step 2: Generate Dummy Data

Run the data generation script to create CSV files:
```bash
python src/generate_data.py
```

This creates:
- `data/household_data.csv` - 7 dummy households with varied needs
- `data/property_data.csv` - 15 dummy properties across London

### Step 3: Run the Application

**Option A: Standard web form**
```bash
streamlit run app.py
```

**Option B: Voice-enabled version with in-browser recording (requires AWS setup)**
```bash
streamlit run app_voice.py
```

See **VOICE_SETUP.md** for AWS configuration and **IN_BROWSER_RECORDING.md** for recording setup.

The application will open in your browser at `http://localhost:8501`

## Usage

1. **Fill in the household form** with required information:
   - Household composition (e.g., "2 adults, 2 children")
   - Preferred area (North/East/South/West/Central London)
   - Monthly budget
   - Days in emergency accommodation
   - Access needs, school requirements, etc.

2. **Click "Find Suitable Accommodation"** to run the matching algorithm

3. **Review results**:
   - Top 3 recommended properties with detailed scores
   - Match explanations showing why each property fits
   - Suitability flags for any policy violations
   - Full ranked list of all properties

## Matching Algorithm

The platform uses a **weighted scoring model** (chosen over ML for transparency and policy alignment):

### Scoring Weights
- **Location**: 35% (highest) - Area restrictions must be met
- **Bedroom Suitability**: 25% - Based on UK bedroom standards
- **Affordability**: 20% - Within budget constraints
- **Access Needs**: 15% - Critical accessibility requirements
- **Amenities**: 5% - Schools, healthcare, support services

### Scoring Logic

**Location Score (0-1)**:
- Exact match = 1.0
- No match = 0.0

**Bedroom Score (0-1)**:
- Insufficient bedrooms = 0.0 (unsuitable)
- Exact match or +1 bedroom = 1.0
- Over-provision = reduced score (inefficient allocation)

**Affordability Score (0-1)**:
- Over budget = 0.0 (unsuitable)
- 80-100% of budget = 1.0
- Well under budget = reduced score

**Access Needs Score (0-1)**:
- Critical needs unmet = 0.0 (unsuitable)
- All needs met = 1.0
- Partial match = 0.3-0.5

**Amenities Score (0-1)**:
- Based on schools, healthcare, employment support proximity

### Policy Enforcement

- ⚠️ **42-day limit**: Flags households at/near emergency accommodation limit
- ⚠️ **Bedroom standards**: Ensures minimum bedroom requirements met
- ⚠️ **Access needs**: Critical accessibility requirements are mandatory
- ⚠️ **Affordability**: Properties over budget are flagged as unsuitable

## Data Schema

### Household Data (`household_data.csv`)
- `household_id`: Unique identifier
- `eligibility_pre_screen`: Pre-screening status
- `area_restrictions`: Preferred location
- `priority_need`: Low/Medium/High/Critical
- `intentional_homeless`: Yes/No
- `eligibility`: Eligible/Under Review/Not Eligible
- `length_of_placement`: Days in emergency accommodation
- `access_needs`: Accessibility requirements
- `schools`: School proximity needs
- `employment`: Employment status
- `health_social_network`: Healthcare/support needs
- `affordability`: Monthly budget (£)
- `caring_responsibilities`: Caring duties
- `household_composition`: Household members
- `risk_level`: Low/Medium/High
- `drug_use`: Substance use history

### Property Data (`property_data.csv`)
- `property_id`: Unique identifier
- `location`: Area (North/East/South/West/Central London)
- `neighbour_quality`: Poor/Fair/Good/Excellent
- `affordability`: Monthly rent (£)
- `rooms`: Total rooms
- `beds`: Number of bedrooms
- `tenure_length`: short/long
- `access_features`: Accessibility features
- `nearby_amenities`: Local services and facilities

## Design Decisions

### Why Weighted Scoring Over ML?

1. **Transparency**: Social housing decisions must be explainable and auditable
2. **Policy Alignment**: Rules-based approach matches UK housing allocation policies
3. **Small Dataset**: 7 households and 15 properties insufficient for reliable ML
4. **Adjustability**: Weights can be easily modified based on policy changes
5. **Trust**: Stakeholders can understand and validate the logic

### Why Location Has Highest Weight?

- Area restrictions often legally binding (e.g., school catchment, support networks)
- Moving households far from support networks increases risk
- Employment and caring responsibilities tied to location
- UK housing policy emphasizes local connection

## Example Scenarios

The dummy data includes realistic scenarios:

1. **HH002**: Family exceeding 42-day limit (URGENT)
2. **HH001**: Family with wheelchair needs approaching limit
3. **HH005**: Single adult in recovery needing support services
4. **HH007**: Domestic violence survivor at 42-day limit

## Limitations & Future Enhancements

**Current Limitations**:
- Simplified bedroom calculation (doesn't account for all UK bedroom standard rules)
- Static weights (could be dynamic based on priority level)
- No real-time availability checking
- No booking/allocation workflow

**Potential Enhancements**:
- Integration with real property databases
- Dynamic weight adjustment based on urgency
- Multi-criteria decision analysis (MCDA)
- Historical outcome tracking for algorithm refinement
- Case worker dashboard for managing multiple households
- Automated alerts for 42-day limit approaching

## License

This is a prototype for demonstration purposes.

## Contact

For questions or improvements, please open an issue.