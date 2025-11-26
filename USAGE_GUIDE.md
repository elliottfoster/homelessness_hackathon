# Usage Guide

## 🎯 How to Use the Temporary Accommodation Matching Platform

---

## Quick Start

### 1. See the Algorithm in Action (No Installation)

```bash
python demo_algorithm.py
```

This shows a complete walkthrough of how the matching algorithm works with example data.

---

## Using the Web Application

### Step 1: Launch the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

### Step 2: Fill in the Household Form

The form has two sections:

#### **Basic Information** (Left Column)

1. **Household Composition*** (Required)
   - Example: "2 adults, 2 children"
   - Example: "1 adult, 3 children"
   - Example: "2 adults"
   - Example: "1 adult"

2. **Preferred Area*** (Required)
   - Select from: North London, East London, South London, West London, Central London

3. **Monthly Budget (£)*** (Required)
   - Enter maximum affordable rent
   - Example: 800 (for £800/month)

4. **Days in Emergency Accommodation*** (Required)
   - Enter number of days already spent in emergency accommodation
   - Important: 42 days is the legal limit for families

5. **Priority Need Level*** (Required)
   - Low, Medium, High, or Critical

6. **Eligibility Status*** (Required)
   - Eligible, Under Review, or Not Eligible

#### **Specific Needs** (Right Column)

7. **Access Needs**
   - Example: "Wheelchair access"
   - Example: "Ground floor only"
   - Example: "Lift required"
   - Leave blank if none

8. **School Requirements**
   - Example: "Primary school required"
   - Example: "Secondary school required"
   - Example: "Primary and secondary required"
   - Leave blank if not applicable

9. **Employment Status**
   - Select from: Full-time employed, Part-time employed, Self-employed, Unemployed, Student

10. **Health/Social Support Needs**
    - Example: "Mental health support needed"
    - Example: "Hospital nearby needed"
    - Example: "Substance abuse support"
    - Leave blank if none

11. **Caring Responsibilities**
    - Select from: No, Yes - young children, Yes - elderly parent, Yes - disabled child, Yes - other

12. **Risk Level**
    - Select from: Low, Medium, High

13. **Substance Use History**
    - Select from: No, Yes - in recovery, Yes - active support needed

### Step 3: Submit the Form

Click the **"🔍 Find Suitable Accommodation"** button at the bottom of the form.

### Step 4: Review Results

The results page shows:

#### **Urgent Alerts** (if applicable)
- 🚨 Red alert if 42-day limit reached/exceeded
- ⚠️ Yellow warning if approaching 42-day limit (35+ days)

#### **Top 3 Recommended Properties**

Each property card shows:

**Property Details:**
- Location (e.g., North London)
- Number of bedrooms
- Number of rooms
- Monthly rent
- Tenure length (short/long)

**Features & Amenities:**
- Access features (wheelchair, lift, ground floor, etc.)
- Neighbourhood quality
- Nearby amenities (schools, healthcare, etc.)

**Suitability Scores:**
- Location score (0-1)
- Bedroom score (0-1)
- Affordability score (0-1)
- Access score (0-1)
- Amenities score (0-1)

**Match Explanation:**
- Plain English explanation of why the property is suitable or not
- Example: "✓ Location matches preferred area (North London) | ✓ Suitable bedroom count (2 beds for 2 required) | ✓ Within budget (£800/month) | ✓ Access needs met"

**Suitability Flags:**
- ⚠️ Warnings for any issues (over budget, access needs not met, etc.)
- ✅ Green checkmark if no issues

#### **All Properties Ranked**

A table showing all properties sorted by suitability score, with:
- Property ID
- Location
- Number of beds
- Monthly rent
- Overall score
- Number of issues

---

## Example Scenarios

### Scenario 1: Family with Wheelchair Needs (Urgent)

**Input:**
- Composition: "2 adults, 2 children"
- Area: North London
- Budget: £800
- Days in emergency: 35
- Access: "Wheelchair access"
- Schools: "Primary school required"

**Expected Results:**
- Top match: PROP001 or PROP006 (both wheelchair accessible in North London)
- Warning: Approaching 42-day limit
- High scores for properties meeting all requirements

### Scenario 2: Single Parent Exceeding Limit (Critical)

**Input:**
- Composition: "1 adult, 3 children"
- Area: East London
- Budget: £600
- Days in emergency: 45
- Access: "Ground floor only"
- Schools: "Secondary school required"

**Expected Results:**
- 🚨 URGENT alert (exceeded 42-day limit)
- Top match: PROP002 (East London, ground floor, affordable)
- Critical priority for immediate placement

### Scenario 3: Couple (Standard Case)

**Input:**
- Composition: "2 adults"
- Area: South London
- Budget: £1000
- Days in emergency: 20
- Access: None
- Schools: Not required

**Expected Results:**
- Multiple suitable options
- No urgent warnings
- Properties with 1-2 bedrooms recommended

### Scenario 4: Person in Recovery

**Input:**
- Composition: "1 adult"
- Area: Central London
- Budget: £500
- Days in emergency: 15
- Access: None
- Health: "Substance abuse support"

**Expected Results:**
- Top match: PROP005 or PROP012 (near substance abuse services)
- Affordable options prioritized
- Support services proximity important

---

## Understanding the Scores

### Overall Score (0-1)

The overall score is calculated as:
```
Overall = (Location × 0.35) + (Bedrooms × 0.25) + (Affordability × 0.20) + 
          (Access × 0.15) + (Amenities × 0.05)
```

**Score Interpretation:**
- 0.80-1.00: ✅ Highly Suitable
- 0.60-0.79: ✓ Suitable
- 0.40-0.59: ~ Partially Suitable
- 0.00-0.39: ✗ Not Suitable

### Component Scores

Each component is scored 0-1:

**Location (35% weight):**
- 1.0 = Exact match with preferred area
- 0.0 = Different area

**Bedrooms (25% weight):**
- 1.0 = Perfect match (exact or +1 bedroom)
- 0.7 = Over-provision (more than needed)
- 0.0 = Insufficient (below minimum)

**Affordability (20% weight):**
- 1.0 = Within budget (80-100% of budget)
- 0.9 = Under budget (60-80% of budget)
- 0.7 = Well under budget (<60%)
- 0.0 = Over budget

**Access (15% weight):**
- 1.0 = All access needs met
- 0.5 = Partial match
- 0.0 = Critical needs not met

**Amenities (5% weight):**
- 1.0 = All desired amenities nearby
- 0.5 = Some amenities nearby
- 0.0 = No relevant amenities

---

## Suitability Flags

### Critical Flags (Property Unsuitable)

- ⚠️ **UNAFFORDABLE** - Rent exceeds budget
- ⚠️ **ACCESS NEEDS NOT MET** - Critical accessibility requirement not met
- ⚠️ **INSUFFICIENT BEDROOMS** - Below UK bedroom standard
- ⚠️ **WRONG LOCATION** - Area restriction not met

### Urgent Flags (Household Status)

- 🚨 **URGENT - 42-day limit reached/exceeded** - Immediate placement required
- ⚠️ **WARNING - Approaching 42-day limit** - Placement needed within 7 days

---

## Tips for Best Results

1. **Be specific with access needs**
   - "Wheelchair access" is clearer than "accessible"
   - "Ground floor only" vs "Lift required" are different needs

2. **Accurate household composition**
   - Include all adults and children
   - Example: "2 adults, 2 children" not "family of 4"

3. **Realistic budget**
   - Consider actual affordability
   - Properties over budget will be flagged as unsuitable

4. **School requirements**
   - Specify "Primary" or "Secondary" if needed
   - Leave blank if no children or not applicable

5. **Health/social needs**
   - Mention specific support services needed
   - Example: "Mental health support" or "Hospital nearby"

---

## Interpreting Results

### When Top Properties Have Low Scores

If all properties score below 0.5, it means:
- Limited suitable options available
- May need to adjust requirements (budget, area, etc.)
- Consider properties with highest scores despite issues

### When Multiple Properties Score High

If several properties score above 0.8:
- Good options available
- Consider secondary factors (neighbourhood quality, tenure length)
- Review amenities for best fit

### When Access Needs Not Met

If critical access needs aren't met:
- Property is unsuitable (score will be low)
- Look for alternative properties
- May need to expand search area

---

## Testing the Platform

### Use Pre-loaded Household Data

The platform includes 7 pre-loaded households in `data/household_data.csv`:

1. **HH001** - Family with wheelchair needs, 35 days
2. **HH002** - Single parent, 45 days (EXCEEDS limit)
3. **HH003** - Couple, employed, 20 days
4. **HH004** - Large family, disabled child, 38 days
5. **HH005** - Single adult in recovery, 15 days
6. **HH006** - Single parent with wheelchair, 28 days
7. **HH007** - Domestic violence survivor, 42 days

Try entering these scenarios to see how the algorithm responds.

---

## Troubleshooting

### No Properties Shown

**Possible causes:**
- Property data file missing
- Run: `python src/generate_data.py`

### All Properties Unsuitable

**Possible causes:**
- Budget too low for area
- Access needs too specific
- Area has limited properties
- Try adjusting requirements

### Form Won't Submit

**Possible causes:**
- Required fields not filled
- Check for * marked fields
- Ensure all mandatory fields have values

---

## Advanced Usage

### Modifying Data

To test with different data:

1. Edit `src/generate_data.py`
2. Modify household or property lists
3. Run: `python src/generate_data.py`
4. Restart the app

### Adjusting Weights

To change scoring priorities:

1. Edit `src/matching_engine.py`
2. Modify the `WEIGHTS` dictionary
3. Ensure weights sum to 1.0
4. Restart the app

### Adding New Criteria

To add new matching criteria:

1. Add column to CSV data
2. Add scoring method in `matching_engine.py`
3. Update weight distribution
4. Add form field in `app.py`

---

## Getting Help

- **README.md** - Full documentation
- **INSTALLATION.md** - Setup instructions
- **PROJECT_SUMMARY.md** - Project overview
- **demo_algorithm.py** - Algorithm walkthrough

---

## Next Steps

1. Try different household scenarios
2. Explore the scoring breakdown
3. Review the algorithm explanation
4. Read the code to understand implementation
5. Modify data or weights to experiment

---

**Happy matching! 🏠**
