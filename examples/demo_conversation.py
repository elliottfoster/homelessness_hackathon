"""
Demo script showing conversational intake between caseworker and family.
Demonstrates how the system extracts information from natural dialogue.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / 'src'))

from voice_handler import VoiceInputHandler

def demo_conversations():
    """Demonstrate conversational intake with example dialogues."""
    
    print("=" * 80)
    print("CONVERSATIONAL INTAKE DEMONSTRATION")
    print("=" * 80)
    print()
    print("This demo shows how caseworker-family conversations are processed.")
    print("The system uses Amazon Transcribe's speaker diarization to identify")
    print("who is speaking and extracts information from the family's responses.")
    print()
    
    # Initialize handler
    handler = VoiceInputHandler()
    
    # Example conversations
    conversations = [
        {
            "name": "Family with Wheelchair Needs",
            "dialogue": [
                ("Caseworker", "Hello, thank you for coming in today. Can you tell me about your household?"),
                ("Family", "Yes, I have two adults and two children in my family."),
                ("Caseworker", "Okay, and what area are you looking for accommodation in?"),
                ("Family", "We need somewhere in North London, close to where we are now."),
                ("Caseworker", "What's your monthly budget for rent?"),
                ("Family", "We can afford up to 800 pounds per month."),
                ("Caseworker", "Do you have any special access requirements?"),
                ("Family", "Yes, we need wheelchair access because my partner uses a wheelchair."),
                ("Caseworker", "Are there any schools you need to be near?"),
                ("Family", "Yes, we need a primary school nearby for our children."),
                ("Caseworker", "What's your current employment situation?"),
                ("Family", "I'm working part-time at the moment."),
                ("Caseworker", "How long have you been in emergency accommodation?"),
                ("Family", "We've been there for 35 days now."),
                ("Caseworker", "Okay, thank you. Let me search for suitable properties for you."),
            ]
        },
        {
            "name": "Single Parent - Urgent Case",
            "dialogue": [
                ("Caseworker", "Good morning. Let's start with your household composition."),
                ("Family", "I'm a single parent with three children."),
                ("Caseworker", "Which area would you prefer?"),
                ("Family", "East London would be best for us."),
                ("Caseworker", "What can you afford monthly?"),
                ("Family", "My budget is 600 pounds per month."),
                ("Caseworker", "Any accessibility needs?"),
                ("Family", "We need ground floor accommodation. I have mobility issues."),
                ("Caseworker", "School requirements?"),
                ("Family", "My eldest needs a secondary school nearby."),
                ("Caseworker", "Are you currently employed?"),
                ("Family", "No, I'm unemployed at the moment."),
                ("Caseworker", "Any health or support needs?"),
                ("Family", "Yes, I need mental health support services nearby."),
                ("Caseworker", "How long in emergency accommodation?"),
                ("Family", "45 days. I know that's over the limit. This is really urgent."),
                ("Caseworker", "I understand. Let me find you something right away."),
            ]
        },
        {
            "name": "Domestic Violence Survivor",
            "dialogue": [
                ("Caseworker", "Thank you for being here. I know this is difficult. Can you tell me about your household?"),
                ("Family", "It's just me and my baby. One adult and one child."),
                ("Caseworker", "Where would you feel safe?"),
                ("Family", "East London, away from where I was before."),
                ("Caseworker", "What's your budget?"),
                ("Family", "I can manage 550 pounds per month."),
                ("Caseworker", "Any specific requirements for the property?"),
                ("Family", "Ground floor would be better, and somewhere with security."),
                ("Caseworker", "Do you need any support services?"),
                ("Family", "Yes, I need domestic violence support and childcare services nearby."),
                ("Caseworker", "Employment status?"),
                ("Family", "I'm unemployed right now."),
                ("Caseworker", "How long have you been in emergency accommodation?"),
                ("Family", "Exactly 42 days today."),
                ("Caseworker", "Okay, this is priority. Let me find you somewhere safe immediately."),
            ]
        }
    ]
    
    for idx, conv in enumerate(conversations, 1):
        print("=" * 80)
        print(f"EXAMPLE {idx}: {conv['name']}")
        print("=" * 80)
        print()
        
        print("CONVERSATION:")
        print("-" * 80)
        
        # Display conversation
        family_responses = []
        for speaker, text in conv['dialogue']:
            if speaker == "Caseworker":
                print(f"👔 {speaker}: {text}")
            else:
                print(f"👤 {speaker}: {text}")
                family_responses.append(text)
        
        print()
        print("PROCESSING...")
        print("-" * 80)
        
        # Combine family responses for parsing
        family_text = ' '.join(family_responses)
        
        # Parse the information
        household_info = handler.parse_household_info(family_text)
        
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
        print()
        
        # Show urgency flags
        if household_info['length_of_placement'] >= 42:
            print("🚨 URGENT: 42-day emergency limit reached/exceeded!")
            print("   → Immediate placement required")
        elif household_info['length_of_placement'] >= 35:
            print("⚠️  WARNING: Approaching 42-day emergency limit")
            print("   → Placement needed within 7 days")
        
        if household_info['priority_need'] == 'Critical':
            print("🚨 CRITICAL PRIORITY NEED")
        
        print()
        print("KEY INSIGHTS:")
        print("-" * 80)
        
        # Analyze the conversation
        num_turns = len(conv['dialogue'])
        caseworker_turns = sum(1 for s, _ in conv['dialogue'] if s == "Caseworker")
        family_turns = sum(1 for s, _ in conv['dialogue'] if s == "Family")
        
        print(f"• Total conversation turns: {num_turns}")
        print(f"• Caseworker questions: {caseworker_turns}")
        print(f"• Family responses: {family_turns}")
        print(f"• Information extracted from family responses only")
        print(f"• Caseworker questions help structure the conversation")
        print()
    
    print("=" * 80)
    print("HOW CONVERSATIONAL INTAKE WORKS")
    print("=" * 80)
    print()
    
    print("1. SPEAKER DIARIZATION (Amazon Transcribe)")
    print("   - Identifies who is speaking (Speaker 0, Speaker 1)")
    print("   - Timestamps each speaker segment")
    print("   - Separates caseworker from family member")
    print()
    
    print("2. SPEAKER IDENTIFICATION")
    print("   - Analyzes conversation patterns")
    print("   - Caseworker: Asks questions (more '?' marks)")
    print("   - Family: Provides information (longer responses)")
    print("   - Automatically determines roles")
    print()
    
    print("3. INFORMATION EXTRACTION")
    print("   - Focuses on family member's responses")
    print("   - Ignores caseworker questions")
    print("   - Extracts: numbers, locations, needs, etc.")
    print("   - Uses same parsing logic as single-speaker input")
    print()
    
    print("4. VALIDATION")
    print("   - Shows full conversation transcript")
    print("   - Highlights which speaker is which")
    print("   - User can review and edit extracted data")
    print("   - Confirms before matching")
    print()
    
    print("=" * 80)
    print("BENEFITS OF CONVERSATIONAL INTAKE")
    print("=" * 80)
    print()
    
    print("✓ NATURAL INTERACTION")
    print("  - Feels like a normal conversation")
    print("  - Caseworker can guide the discussion")
    print("  - Family member can ask questions")
    print("  - More comfortable than monologue")
    print()
    
    print("✓ STRUCTURED INFORMATION")
    print("  - Caseworker ensures all topics covered")
    print("  - Questions prompt complete responses")
    print("  - Less likely to miss important details")
    print("  - Professional and organized")
    print()
    
    print("✓ BETTER ACCURACY")
    print("  - Clarifying questions improve data quality")
    print("  - Caseworker can rephrase if needed")
    print("  - Family member can elaborate")
    print("  - Reduces misunderstandings")
    print()
    
    print("✓ TRAUMA-INFORMED")
    print("  - Caseworker can pace the conversation")
    print("  - Sensitive topics handled carefully")
    print("  - Family member feels supported")
    print("  - More dignified process")
    print()
    
    print("✓ DOCUMENTATION")
    print("  - Full conversation recorded")
    print("  - Can review later if needed")
    print("  - Audit trail for decisions")
    print("  - Protects both parties")
    print()
    
    print("=" * 80)
    print("COMPARISON: MONOLOGUE VS CONVERSATION")
    print("=" * 80)
    print()
    
    print("MONOLOGUE (Single Speaker):")
    print("  • Family speaks alone")
    print("  • May forget important details")
    print("  • Can be intimidating")
    print("  • Less structured")
    print()
    
    print("CONVERSATION (Two Speakers):")
    print("  • Caseworker guides discussion")
    print("  • All topics covered systematically")
    print("  • More comfortable and natural")
    print("  • Professional and thorough")
    print()
    
    print("=" * 80)
    print("TECHNICAL IMPLEMENTATION")
    print("=" * 80)
    print()
    
    print("Amazon Transcribe Settings:")
    print("  • ShowSpeakerLabels: True")
    print("  • MaxSpeakerLabels: 2")
    print("  • LanguageCode: en-GB (UK English)")
    print()
    
    print("Speaker Identification Algorithm:")
    print("  1. Count questions per speaker")
    print("  2. Speaker with more questions = Caseworker")
    print("  3. Other speaker = Family member")
    print("  4. Extract info from family responses only")
    print()
    
    print("Information Extraction:")
    print("  • Same parsing logic as single-speaker")
    print("  • Applied to family responses only")
    print("  • Caseworker questions ignored")
    print("  • Full transcript preserved for review")
    print()
    
    print("=" * 80)
    print("BEST PRACTICES FOR CASEWORKERS")
    print("=" * 80)
    print()
    
    print("1. START WITH RAPPORT")
    print("   - Introduce yourself")
    print("   - Explain the process")
    print("   - Make them comfortable")
    print()
    
    print("2. ASK CLEAR QUESTIONS")
    print("   - One topic at a time")
    print("   - Use simple language")
    print("   - Allow time to respond")
    print()
    
    print("3. COVER ALL TOPICS")
    print("   - Household composition")
    print("   - Preferred area")
    print("   - Budget")
    print("   - Access needs")
    print("   - Schools")
    print("   - Employment")
    print("   - Health/support needs")
    print("   - Days in emergency accommodation")
    print()
    
    print("4. BE SENSITIVE")
    print("   - Trauma-informed approach")
    print("   - Respect privacy")
    print("   - Don't rush")
    print("   - Show empathy")
    print()
    
    print("5. CONFIRM UNDERSTANDING")
    print("   - Summarize key points")
    print("   - Ask if anything missed")
    print("   - Review extracted information")
    print("   - Get confirmation before proceeding")
    print()
    
    print("=" * 80)
    print("NEXT STEPS")
    print("=" * 80)
    print()
    
    print("To use conversational intake:")
    print()
    print("1. Set up AWS Transcribe (see VOICE_SETUP.md)")
    print()
    print("2. Record caseworker-family conversation")
    print("   - Use good quality microphone")
    print("   - Minimize background noise")
    print("   - Speak clearly")
    print()
    print("3. Upload audio to app:")
    print("   streamlit run app_voice.py")
    print()
    print("4. Review conversation transcript")
    print("   - Check speaker identification")
    print("   - Verify extracted information")
    print()
    print("5. Edit if needed and match")
    print()
    
    print("=" * 80)
    print("DEMO COMPLETE")
    print("=" * 80)
    print()

if __name__ == '__main__':
    demo_conversations()
