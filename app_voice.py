"""
Voice-Enabled Streamlit Application for Homeless Household to Temporary Accommodation Matching.
Uses Amazon Transcribe for speech-to-text conversion.
Run with: streamlit run app_voice.py
"""
import streamlit as st
import pandas as pd
from pathlib import Path
import sys
import tempfile
import os

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from matching_engine import AccommodationMatcher
from voice_handler import VoiceInputHandler

# Try to import audio recorder
try:
    from audiorecorder import audiorecorder
    AUDIO_RECORDER_AVAILABLE = True
except ImportError:
    AUDIO_RECORDER_AVAILABLE = False

# Page configuration
st.set_page_config(
    page_title="Voice-Enabled Accommodation Matcher",
    page_icon="🎤",
    layout="wide"
)

# Title and description
st.title("🎤 Voice-Enabled Temporary Accommodation Matching")
st.markdown("""
This platform matches homeless households to suitable temporary accommodation 
using **voice input** powered by Amazon Transcribe. Simply speak your household 
information instead of filling out forms.
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

def display_results(results, household):
    """Display matching results."""
    st.header("🎯 Matching Results")
    
    # Check for urgent flags
    length_of_placement = int(household.get('length_of_placement', 0))
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

properties_df = load_properties()

if properties_df is not None:
    # Initialize voice handler
    try:
        voice_handler = VoiceInputHandler()
        voice_available = voice_handler.transcribe_client is not None
    except Exception as e:
        st.error(f"Could not initialize voice handler: {e}")
        voice_handler = None
        voice_available = False
    
    # Create tabs for voice and manual input
    tab1, tab2 = st.tabs(["🎤 Voice Input", "📝 Manual Input"])
    
    with tab1:
        st.header("🎤 Conversational Intake Mode")
        
        if not voice_available:
            st.warning("""
            ⚠️ Voice input is not available. 
            
            **To enable voice input:**
            1. Install boto3: `pip install boto3`
            2. Configure AWS credentials: `aws configure`
            3. Restart the application
            
            See **VOICE_SETUP.md** for detailed instructions.
            
            For now, please use the **Manual Input** tab.
            """)
        else:
            st.markdown("""
            **How to use conversational intake:**
            1. Record a conversation between caseworker and family
            2. Caseworker asks questions about the household situation
            3. Family member responds with their information
            4. Upload the audio file
            5. AI transcribes and extracts relevant information
            
            **Example Conversation:** 
            
            **Caseworker:** "Hello, can you tell me about your household?"
            
            **Family:** "Yes, I have two adults and two children."
            
            **Caseworker:** "What area are you looking for accommodation in?"
            
            **Family:** "We need somewhere in North London."
            
            **Caseworker:** "What's your monthly budget?"
            
            **Family:** "We can afford up to 800 pounds per month."
            
            **Caseworker:** "Do you have any special access requirements?"
            
            **Family:** "Yes, we need wheelchair access because my partner uses a wheelchair."
            
            *The system will automatically identify speakers and extract information from the family's responses.*
            """)
            
            # Recording options
            st.subheader("🎙️ Record or Upload Audio")
            
            recording_method = st.radio(
                "Choose recording method:",
                ["📱 Record directly in browser", "📁 Upload audio file"],
                horizontal=True
            )
            
            audio_data = None
            audio_file = None
            audio_file_path = None
            
            if recording_method == "📱 Record directly in browser":
                if AUDIO_RECORDER_AVAILABLE:
                    st.info("Click the microphone button below to start/stop recording")
                    
                    try:
                        audio_data = audiorecorder("🎤 Start Recording", "⏹️ Stop Recording")
                        
                        if len(audio_data) > 0:
                            st.success(f"✅ Recording captured! Duration: {len(audio_data) / audio_data.frame_rate:.1f} seconds")
                            
                            # Play back the recording
                            st.audio(audio_data.export().read())
                            
                            # Save to temp file
                            with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as tmp_file:
                                audio_data.export(tmp_file.name, format="wav")
                                audio_file_path = tmp_file.name
                    except Exception as e:
                        st.error(f"""
                        ❌ Recording error: {str(e)}
                        
                        **This might be due to missing ffmpeg.**
                        
                        **To install ffmpeg:**
                        
                        **macOS:**
                        ```bash
                        brew install ffmpeg
                        ```
                        
                        **Ubuntu/Debian:**
                        ```bash
                        sudo apt-get install ffmpeg
                        ```
                        
                        **Windows:**
                        Download from https://ffmpeg.org/download.html
                        
                        **Alternative:** Use "Upload audio file" option instead.
                        """)
                else:
                    st.warning("""
                    ⚠️ Audio recorder not available.
                    
                    **To enable in-browser recording:**
                    ```bash
                    pip install streamlit-audiorecorder
                    ```
                    
                    For now, please use "Upload audio file" option.
                    """)
            
            else:  # Upload audio file
                audio_file = st.file_uploader(
                    "Upload audio file (MP3, WAV, FLAC)",
                    type=['mp3', 'wav', 'flac', 'ogg', 'm4a'],
                    help="Record your household information and upload the audio file"
                )
                
                if audio_file:
                    st.success(f"✅ File uploaded: {audio_file.name}")
                    st.audio(audio_file)
            
            # AWS Configuration
            with st.expander("⚙️ AWS Configuration (Required for Voice Input)"):
                st.markdown("""
                To use voice input, you need:
                1. AWS account with Transcribe access
                2. S3 bucket for temporary audio storage
                3. AWS credentials configured
                """)
                
                aws_region = st.text_input("AWS Region", value="us-east-1")
                s3_bucket = st.text_input("S3 Bucket Name", placeholder="your-bucket-name")
                
                st.info("""
                **Setup AWS credentials:**
                ```bash
                aws configure
                # Enter your AWS Access Key ID
                # Enter your AWS Secret Access Key
                # Enter region (e.g., us-east-1)
                ```
                """)
            
            # Process button
            has_audio = audio_file_path is not None or (recording_method == "📁 Upload audio file" and audio_file is not None)
            
            if st.button("🎤 Process Voice Input", type="primary", disabled=not has_audio):
                if not s3_bucket:
                    st.error("Please provide an S3 bucket name in the AWS Configuration section")
                else:
                    with st.spinner("Transcribing audio..."):
                        # Determine the audio file path
                        if audio_file_path:
                            # Already saved from recording
                            tmp_path = audio_file_path
                        else:
                            # Save uploaded file temporarily
                            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(audio_file.name).suffix) as tmp_file:
                                tmp_file.write(audio_file.read())
                                tmp_path = tmp_file.name
                        
                        try:
                            # Transcribe audio with speaker diarization
                            transcript_data = voice_handler.transcribe_audio(tmp_path, s3_bucket)
                            
                            if transcript_data:
                                st.success("✅ Audio transcribed successfully!")
                                
                                # Parse conversation
                                with st.spinner("Analyzing conversation and extracting information..."):
                                    household = voice_handler.parse_conversation(transcript_data)
                            
                            # Show conversation analysis
                            st.subheader("💬 Conversation Analysis")
                            
                            conv = household.get('conversation', {})
                            
                            col1, col2, col3 = st.columns(3)
                            with col1:
                                st.metric("Conversation Turns", conv.get('num_turns', 0))
                            with col2:
                                st.metric("Speakers Identified", 2)
                            with col3:
                                caseworker = conv.get('caseworker_speaker', 'spk_0')
                                family = conv.get('family_speaker', 'spk_1')
                                st.metric("Information Source", f"Speaker {family[-1]}")
                            
                            # Show conversation transcript with speaker labels
                            with st.expander("📝 View Full Conversation Transcript"):
                                speaker_segments = conv.get('speaker_segments', [])
                                
                                for seg in speaker_segments:
                                    speaker = seg['speaker']
                                    text = seg['text']
                                    
                                    # Identify role
                                    if speaker == conv.get('caseworker_speaker'):
                                        role = "👔 Caseworker"
                                        st.markdown(f"**{role}:** {text}")
                                    else:
                                        role = "👤 Family Member"
                                        st.markdown(f"**{role}:** _{text}_")
                                
                                st.divider()
                                st.caption(f"Full transcript: {conv.get('full_transcript', '')}")
                            
                            # Show extracted information
                            st.subheader("📊 Extracted Information")
                            col1, col2 = st.columns(2)
                            
                            with col1:
                                st.markdown("**Basic Information:**")
                                st.write(f"• Composition: {household['household_composition']}")
                                st.write(f"• Area: {household['area_restrictions']}")
                                st.write(f"• Budget: £{household['affordability']}/month")
                                st.write(f"• Days in emergency: {household['length_of_placement']}")
                                st.write(f"• Priority: {household['priority_need']}")
                            
                            with col2:
                                st.markdown("**Specific Needs:**")
                                st.write(f"• Access: {household['access_needs']}")
                                st.write(f"• Schools: {household['schools']}")
                                st.write(f"• Employment: {household['employment']}")
                                st.write(f"• Health: {household['health_social_network']}")
                            
                            # Allow editing
                            if st.checkbox("✏️ Edit extracted information"):
                                with st.form("edit_form"):
                                    household['household_composition'] = st.text_input("Household Composition", household['household_composition'])
                                    household['area_restrictions'] = st.selectbox("Area", 
                                        ["North London", "East London", "South London", "West London", "Central London"],
                                        index=["North London", "East London", "South London", "West London", "Central London"].index(household['area_restrictions'])
                                    )
                                    household['affordability'] = st.number_input("Budget (£)", value=household['affordability'])
                                    
                                    if st.form_submit_button("Update Information"):
                                        st.success("Information updated!")
                            
                            # Run matching
                            if st.button("🔍 Find Suitable Accommodation"):
                                with st.spinner("Matching household to properties..."):
                                    matcher = AccommodationMatcher(properties_df)
                                    results = matcher.match_household(household)
                                
                                # Display results (same as original app)
                                display_results(results, household)
                            
                            else:
                                st.error("❌ Failed to transcribe audio. Please check your AWS configuration and try again.")
                        
                        finally:
                            # Cleanup temp file
                            if os.path.exists(tmp_path):
                                os.unlink(tmp_path)
    
    with tab2:
        st.header("📝 Manual Input Mode")
        st.markdown("Fill in the form manually if you prefer not to use voice input.")
        
        # Original form (same as app.py)
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
        
        # Process manual form submission
        if submitted:
            if not household_composition or not area_restrictions:
                st.error("Please fill in all required fields marked with *")
            else:
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
                display_results(results, household)

# Sidebar with information
with st.sidebar:
    st.header("ℹ️ About Voice Input")
    st.markdown("""
    This platform uses **Amazon Transcribe** to convert your spoken words into text.
    
    **Benefits:**
    - 🎤 Faster than typing
    - 🌍 Accessible for all literacy levels
    - 💬 Natural conversation style
    - ♿ Supports those with typing difficulties
    
    **How it works:**
    1. Record your household information
    2. Upload the audio file
    3. Amazon Transcribe converts speech to text
    4. AI extracts household details
    5. Matching algorithm finds suitable properties
    """)
    
    st.header("📊 Scoring Weights")
    st.markdown("""
    - 🎯 Location: 35% (highest priority)
    - 🛏️ Bedroom suitability: 25%
    - 💷 Affordability: 20%
    - ♿ Access needs: 15%
    - 🏫 Amenities: 5%
    """)
    
    if properties_df is not None:
        st.header("📊 Available Properties")
        st.metric("Total Properties", len(properties_df))
        st.metric("Locations", properties_df['location'].nunique())
        st.metric("Avg Rent", f"£{properties_df['affordability'].astype(float).mean():.0f}")
