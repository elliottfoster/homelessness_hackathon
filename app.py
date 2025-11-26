"""
Streamlit Web Application for Homeless Household to Temporary Accommodation Matching.
Run with: streamlit run app.py
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from matching_engine import AccommodationMatcher

# Page configuration
st.set_page_config(
    page_title="Temporary Accommodation Matcher",
    page_icon="🏠",
    layout="wide"
)

# Title and description
st.title("🏠 Temporary Accommodation Matching Platform")
st.markdown("""
This platform matches homeless households to suitable temporary accommodation 
based on UK housing allocation policies and individual household needs.
""")

# Load property data
@st.cache_data
def load_properties():
    """Load property data from CSV."""
    property_file = Path('data/property_data.csv')
    if not property_file.exists():
        st.error("Property data not found. Please run: python src/generate_data.py")
        return None
    # Read CSV and ensure string columns are strings
    df = pd.read_csv(property_file, dtype={
        'property_id': str,
        'location': str,
        'neighbour_quality': str,
        'tenure_length': str,
        'access_features': str,
        'nearby_amenities': str
    })
    return df

properties_df = load_properties()

if properties_df is not None:
    # Create form
    st.header("📋 Household Information Form")
    st.markdown("Please provide details about the household seeking accommodation.")
    
    with st.form("household_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader("Basic Information")
            
            household_composition = st.text_input(
                "Household Composition*",
                placeholder="e.g., 2 adults, 2 children",
                help="Describe the household members"
            )
            
            area_restrictions = st.selectbox(
                "Preferred Area*",
                ["North London", "East London", "South London", "West London", "Central London"]
            )
            
            affordability = st.number_input(
                "Monthly Budget (£)*",
                min_value=0,
                max_value=2000,
                value=700,
                step=50,
                help="Maximum affordable monthly rent"
            )
            
            length_of_placement = st.number_input(
                "Days in Emergency Accommodation*",
                min_value=0,
                max_value=100,
                value=0,
                help="Number of days already spent in emergency accommodation"
            )
            
            priority_need = st.selectbox(
                "Priority Need Level*",
                ["Low", "Medium", "High", "Critical"]
            )
            
            eligibility = st.selectbox(
                "Eligibility Status*",
                ["Eligible", "Under Review", "Not Eligible"]
            )
        
        with col2:
            st.subheader("Specific Needs")
            
            access_needs = st.text_input(
                "Access Needs",
                placeholder="e.g., Wheelchair access, Ground floor only",
                help="Any accessibility requirements"
            )
            
            schools = st.text_input(
                "School Requirements",
                placeholder="e.g., Primary school required",
                help="School proximity needs"
            )
            
            employment = st.selectbox(
                "Employment Status",
                ["Full-time employed", "Part-time employed", "Self-employed", "Unemployed", "Student"]
            )
            
            health_social_network = st.text_input(
                "Health/Social Support Needs",
                placeholder="e.g., Mental health support needed",
                help="Healthcare or social support requirements"
            )
            
            caring_responsibilities = st.selectbox(
                "Caring Responsibilities",
                ["No", "Yes - young children", "Yes - elderly parent", "Yes - disabled child", "Yes - other"]
            )
            
            risk_level = st.selectbox(
                "Risk Level",
                ["Low", "Medium", "High"]
            )
            
            drug_use = st.selectbox(
                "Substance Use History",
                ["No", "Yes - in recovery", "Yes - active support needed"]
            )
        
        # Submit button
        submitted = st.form_submit_button("🔍 Find Suitable Accommodation", use_container_width=True)
    
    # Process form submission
    if submitted:
        # Validate required fields
        if not household_composition or not area_restrictions:
            st.error("Please fill in all required fields marked with *")
        else:
            # Create household dict
            household = {
                'household_composition': household_composition,
                'area_restrictions': area_restrictions,
                'affordability': affordability,
                'length_of_placement': length_of_placement,
                'priority_need': priority_need,
                'eligibility': eligibility,
                'access_needs': access_needs or 'None',
                'schools': schools or 'Not required',
                'employment': employment,
                'health_social_network': health_social_network or 'None',
                'caring_responsibilities': caring_responsibilities,
                'risk_level': risk_level,
                'drug_use': drug_use
            }
            
            # Run matching
            with st.spinner("Matching household to suitable properties..."):
                matcher = AccommodationMatcher(properties_df)
                results = matcher.match_household(household)
            
            # Display results
            st.header("🎯 Matching Results")
            
            # Check for urgent flags
            if length_of_placement >= 42:
                st.error("🚨 URGENT: This household has reached or exceeded the 42-day emergency accommodation limit. Immediate placement required.")
            elif length_of_placement >= 35:
                st.warning("⚠️ WARNING: This household is approaching the 42-day emergency accommodation limit.")
            
            # Display top 3 recommendations
            st.subheader("Top 3 Recommended Properties")
            
            top_3 = results[:3]
            
            if not top_3:
                st.warning("No properties found matching the criteria.")
            else:
                for idx, prop in enumerate(top_3, 1):
                    with st.expander(f"#{idx} - {prop['property_id']} ({prop['location']}) - Score: {prop['overall_score']:.2f}", expanded=(idx==1)):
                        # Property details
                        col1, col2, col3 = st.columns(3)
                        
                        with col1:
                            st.markdown("**Property Details**")
                            st.write(f"📍 Location: {prop['location']}")
                            st.write(f"🛏️ Bedrooms: {prop['beds']}")
                            st.write(f"🚪 Rooms: {prop['rooms']}")
                            st.write(f"💷 Rent: £{prop['affordability']}/month")
                            st.write(f"📅 Tenure: {prop['tenure_length']}")
                        
                        with col2:
                            st.markdown("**Features & Amenities**")
                            st.write(f"♿ Access: {prop['access_features']}")
                            st.write(f"🏘️ Neighbourhood: {prop['neighbour_quality']}")
                            st.write(f"🏫 Nearby: {prop['nearby_amenities']}")
                        
                        with col3:
                            st.markdown("**Suitability Scores**")
                            scores = prop['component_scores']
                            st.write(f"📍 Location: {scores['location']:.2f}")
                            st.write(f"🛏️ Bedrooms: {scores['bedrooms']:.2f}")
                            st.write(f"💷 Affordability: {scores['affordability']:.2f}")
                            st.write(f"♿ Access: {scores['access']:.2f}")
                            st.write(f"🏫 Amenities: {scores['amenities']:.2f}")
                        
                        # Match explanation
                        st.markdown("**Match Explanation**")
                        st.info(prop['match_explanation'])
                        
                        # Suitability flags
                        if prop['suitability_flags']:
                            st.markdown("**Suitability Flags**")
                            for flag in prop['suitability_flags']:
                                if '🚨' in flag:
                                    st.error(flag)
                                else:
                                    st.warning(flag)
                        else:
                            st.success("✅ No suitability issues identified")
            
            # Show all results in table
            st.subheader("All Properties Ranked")
            
            results_table = []
            for prop in results:
                results_table.append({
                    'Property ID': prop['property_id'],
                    'Location': prop['location'],
                    'Beds': prop['beds'],
                    'Rent (£)': prop['affordability'],
                    'Overall Score': f"{prop['overall_score']:.2f}",
                    'Issues': len(prop['suitability_flags'])
                })
            
            st.dataframe(results_table, use_container_width=True)

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About")
    st.markdown("""
    This platform uses a **weighted scoring algorithm** to match households to temporary accommodation.
    
    **Scoring Weights:**
    - 🎯 Location: 35% (highest priority)
    - 🛏️ Bedroom suitability: 25%
    - 💷 Affordability: 20%
    - ♿ Access needs: 15%
    - 🏫 Amenities: 5%
    
    **Key Policies:**
    - Families cannot remain in emergency accommodation beyond 42 days
    - Bedroom standards must be met
    - Critical access needs are mandatory
    - Budget constraints are enforced
    """)
    
    st.header("📊 Available Properties")
    if properties_df is not None:
        st.metric("Total Properties", len(properties_df))
        st.metric("Locations", properties_df['location'].nunique())
        st.metric("Avg Rent", f"£{properties_df['affordability'].astype(float).mean():.0f}")
