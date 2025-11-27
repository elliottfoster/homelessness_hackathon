"""
Demo script showing how voice input is parsed into household information.
This demonstrates the parsing logic without requiring AWS Transcribe.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from voice_handler import VoiceInputHandler

def demo_voice_parsing():
    """Demonstrate voice input parsing with example transcripts."""
    
    print("=" * 80)
    print("VOICE INPUT PARSING DEMONSTRATION")
    print("=" * 80)
    print()
    print("This demo shows how spoken words are converted into household information.")
    print("In production, Amazon Transcribe converts speech to text first.")
    print()
    
    # Initialize handler
    handler = VoiceInputHandler()
    
    # Example transcripts
    examples = [
        {
            "name": "Family with Wheelchair Needs",
            "transcript": """
            Hello, I'm looking for accommodation. I have two adults and two children 
            in my household. We need a place in North London. Our budget is 800 pounds 
            per month. We need wheelchair access because my partner uses a wheelchair. 
            We also need a primary school nearby for our kids. We've been in emergency 
            accommodation for 35 days now. I'm currently part-time employed.
            """
        },
        {
            "name": "Single Parent (Urgent)",
            "transcript": """
            I'm a single parent with three children. I need somewhere in East London. 
            My budget is 600 pounds monthly. We need ground floor accommodation. 
            My kids need a secondary school nearby. I'm unemployed right now and need 
            mental health support. We've been in emergency accommodation for 45 days 
            which I know is over the limit. This is urgent.
            """
        },
        {
            "name": "Person in Recovery",
            "transcript": """
            I'm one adult looking for a place in Central London. I can afford 500 pounds 
            per month. I'm in recovery from substance abuse and need support services 
            nearby. I've been in emergency accommodation for 15 days. I'm currently 
            unemployed but looking for work.
            """
        }
    ]
    
    for idx, example in enumerate(examples, 1):
        print("=" * 80)
        print(f"EXAMPLE {idx}: {example['name']}")
        print("=" * 80)
        print()
        
        print("SPOKEN INPUT:")
        print("-" * 80)
        print(example['transcript'].strip())
        print()
        
        print("PARSING...")
        print("-" * 80)
        
        # Parse the transcript
        household_info = handler.parse_household_info(example['transcript'])
        
        print()
        print("EXTRACTED INFORMATION:")
        print("-" * 80)
        print(f"✓ Household Composition: {household_info['household_composition']}")
        print(f"✓ Preferred Area: {household_info['area_restrictions']}")
        print(f"✓ Monthly Budget: £{household_info['affordability']}")
        print(f"✓ Days in Emergency: {household_info['length_of_placement']}")
        print(f"✓ Priority Level: {household_info['priority_need']}")
        print(f"✓ Access Needs: {household_info['access_needs']}")
        print(f"✓ School Requirements: {household_info['schools']}")
        print(f"✓ Employment Status: {household_info['employment']}")
        print(f"✓ Health/Social Needs: {household_info['health_social_network']}")
        print(f"✓ Caring Responsibilities: {household_info['caring_responsibilities']}")
        print(f"✓ Risk Level: {household_info['risk_level']}")
        print(f"✓ Substance Use: {household_info['drug_use']}")
        print()
        
        # Show urgency flags
        if household_info['length_of_placement'] >= 42:
            print("🚨 URGENT: 42-day emergency limit reached/exceeded!")
        elif household_info['length_of_placement'] >= 35:
            print("⚠️  WARNING: Approaching 42-day emergency limit")
        
        if household_info['priority_need'] == 'Critical':
            print("🚨 CRITICAL PRIORITY NEED")
        
        print()
    
    print("=" * 80)
    print("HOW IT WORKS")
    print("=" * 80)
    print()
    print("1. SPEECH TO TEXT (Amazon Transcribe)")
    print("   - User speaks into microphone or uploads audio file")
    print("   - Amazon Transcribe converts speech to text")
    print("   - Supports UK English and multiple accents")
    print()
    print("2. INFORMATION EXTRACTION (Pattern Matching)")
    print("   - Looks for keywords: 'adults', 'children', 'wheelchair', etc.")
    print("   - Extracts numbers: '800 pounds', '35 days', etc.")
    print("   - Identifies locations: 'North London', 'East London', etc.")
    print("   - Detects needs: 'mental health', 'primary school', etc.")
    print()
    print("3. VALIDATION & EDITING")
    print("   - User reviews extracted information")
    print("   - Can edit any field if needed")
    print("   - Confirms before matching")
    print()
    print("4. MATCHING")
    print("   - Same algorithm as manual input")
    print("   - Weighted scoring based on extracted criteria")
    print("   - Returns top 3 suitable properties")
    print()
    
    print("=" * 80)
    print("BENEFITS OF VOICE INPUT")
    print("=" * 80)
    print()
    print("✓ ACCESSIBILITY")
    print("  - Supports households with literacy challenges")
    print("  - Helps those with typing difficulties")
    print("  - Works for all language proficiency levels")
    print()
    print("✓ SPEED")
    print("  - Faster than typing for most people")
    print("  - Natural conversation style")
    print("  - No need to navigate complex forms")
    print()
    print("✓ ACCURACY")
    print("  - People speak more naturally than they write")
    print("  - Can provide more context and detail")
    print("  - Reduces form-filling errors")
    print()
    print("✓ INCLUSIVITY")
    print("  - Removes barriers for vulnerable populations")
    print("  - Supports multiple languages (with AWS config)")
    print("  - More dignified and respectful process")
    print()
    
    print("=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print()
    print("To use voice input in the application:")
    print()
    print("1. Set up AWS account and credentials")
    print("   See: VOICE_SETUP.md")
    print()
    print("2. Install dependencies:")
    print("   pip install -r requirements.txt")
    print()
    print("3. Run the voice-enabled app:")
    print("   streamlit run app_voice.py")
    print()
    print("4. Record your household information")
    print()
    print("5. Upload and process the audio")
    print()
    print("6. Review and match to properties")
    print()
    
    print("=" * 80)
    print("DEMO COMPLETE")
    print("=" * 80)
    print()

if __name__ == '__main__':
    demo_voice_parsing()
