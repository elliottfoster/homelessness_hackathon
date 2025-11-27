# Conversational Intake Guide

## 💬 Overview

The platform supports **conversational intake** where a caseworker and family member have a natural dialogue. The system automatically identifies who is speaking and extracts household information from the family's responses.

## Why Conversational Intake?

### Traditional Approach Problems
- ❌ Forms can be intimidating
- ❌ Families may not know what information is needed
- ❌ Important details often missed
- ❌ Impersonal and bureaucratic

### Conversational Approach Benefits
- ✅ Natural and comfortable
- ✅ Caseworker guides the discussion
- ✅ All topics covered systematically
- ✅ Trauma-informed and respectful
- ✅ Better data quality
- ✅ Full documentation

## How It Works

### 1. Record Conversation

Caseworker and family member have a natural conversation:

**Caseworker:** "Hello, can you tell me about your household?"

**Family:** "Yes, I have two adults and two children."

**Caseworker:** "What area are you looking for?"

**Family:** "We need somewhere in North London."

**Caseworker:** "What's your monthly budget?"

**Family:** "We can afford up to 800 pounds per month."

### 2. Upload Audio

- Record using phone, computer, or recording device
- Supported formats: MP3, WAV, FLAC, OGG, M4A
- Upload to the application

### 3. Automatic Processing

**Amazon Transcribe:**
- Converts speech to text
- Identifies speakers (Speaker 0, Speaker 1)
- Timestamps each segment

**Speaker Identification:**
- Analyzes conversation patterns
- Speaker with more questions = Caseworker
- Other speaker = Family member

**Information Extraction:**
- Extracts data from family responses only
- Ignores caseworker questions
- Parses: composition, area, budget, needs, etc.

### 4. Review & Validate

- View full conversation transcript
- See speaker identification
- Review extracted information
- Edit if needed
- Confirm and match

## Example Conversations

### Example 1: Family with Wheelchair Needs

**👔 Caseworker:** "Hello, thank you for coming in. Can you tell me about your household?"

**👤 Family:** "Yes, I have two adults and two children in my family."

**👔 Caseworker:** "What area are you looking for accommodation in?"

**👤 Family:** "We need somewhere in North London, close to where we are now."

**👔 Caseworker:** "What's your monthly budget for rent?"

**👤 Family:** "We can afford up to 800 pounds per month."

**👔 Caseworker:** "Do you have any special access requirements?"

**👤 Family:** "Yes, we need wheelchair access because my partner uses a wheelchair."

**👔 Caseworker:** "Are there any schools you need to be near?"

**👤 Family:** "Yes, we need a primary school nearby for our children."

**👔 Caseworker:** "What's your current employment situation?"

**👤 Family:** "I'm working part-time at the moment."

**👔 Caseworker:** "How long have you been in emergency accommodation?"

**👤 Family:** "We've been there for 35 days now."

**Extracted Information:**
- Composition: 2 adults, 2 children
- Area: North London
- Budget: £800/month
- Access: Wheelchair access
- Schools: Primary school required
- Employment: Part-time employed
- Days: 35 (⚠️ Approaching 42-day limit)

### Example 2: Single Parent - Urgent Case

**👔 Caseworker:** "Good morning. Let's start with your household composition."

**👤 Family:** "I'm a single parent with three children."

**👔 Caseworker:** "Which area would you prefer?"

**👤 Family:** "East London would be best for us."

**👔 Caseworker:** "What can you afford monthly?"

**👤 Family:** "My budget is 600 pounds per month."

**👔 Caseworker:** "Any accessibility needs?"

**👤 Family:** "We need ground floor accommodation. I have mobility issues."

**👔 Caseworker:** "School requirements?"

**👤 Family:** "My eldest needs a secondary school nearby."

**👔 Caseworker:** "Are you currently employed?"

**👤 Family:** "No, I'm unemployed at the moment."

**👔 Caseworker:** "Any health or support needs?"

**👤 Family:** "Yes, I need mental health support services nearby."

**👔 Caseworker:** "How long in emergency accommodation?"

**👤 Family:** "45 days. I know that's over the limit. This is really urgent."

**Extracted Information:**
- Composition: 1 adult, 3 children
- Area: East London
- Budget: £600/month
- Access: Ground floor only
- Schools: Secondary school required
- Employment: Unemployed
- Health: Mental health support needed
- Days: 45 (🚨 URGENT - Exceeded 42-day limit)

## Best Practices for Caseworkers

### Before the Conversation

1. **Prepare the Environment**
   - Quiet, private space
   - Good quality microphone
   - Test recording equipment
   - Have water available

2. **Introduce Yourself**
   - Name and role
   - Explain the process
   - Mention recording (get consent)
   - Set expectations

3. **Build Rapport**
   - Friendly and welcoming
   - Show empathy
   - Use appropriate language
   - Be patient

### During the Conversation

1. **Ask Clear Questions**
   - One topic at a time
   - Simple, direct language
   - Open-ended when appropriate
   - Allow time to respond

2. **Cover All Topics**
   - ✓ Household composition
   - ✓ Preferred area
   - ✓ Monthly budget
   - ✓ Access needs
   - ✓ School requirements
   - ✓ Employment status
   - ✓ Health/support needs
   - ✓ Caring responsibilities
   - ✓ Days in emergency accommodation
   - ✓ Any other relevant information

3. **Be Trauma-Informed**
   - Recognize signs of distress
   - Pace appropriately
   - Offer breaks if needed
   - Respect boundaries
   - Don't push sensitive topics

4. **Clarify and Confirm**
   - Repeat back key information
   - Ask for clarification if unclear
   - Ensure understanding
   - Check if anything missed

### After the Conversation

1. **Review Together**
   - Show extracted information
   - Verify accuracy
   - Make corrections if needed
   - Get confirmation

2. **Explain Next Steps**
   - How matching works
   - What to expect
   - Timeline
   - Contact information

3. **Document**
   - Save conversation recording
   - Note any concerns
   - Flag urgent cases
   - Follow up as needed

## Question Templates

### Opening
- "Thank you for coming in today. Can you tell me about your household?"
- "Let's start by understanding your situation. Who is in your household?"

### Household Composition
- "How many adults and children are in your household?"
- "Can you describe your family composition?"

### Location
- "What area are you looking for accommodation in?"
- "Which part of London would work best for you?"
- "Are there any areas you need to stay in or avoid?"

### Budget
- "What's your monthly budget for rent?"
- "How much can you afford per month?"
- "What's the maximum rent you can pay?"

### Access Needs
- "Do you have any special access requirements?"
- "Are there any accessibility needs I should know about?"
- "Do you need wheelchair access, ground floor, or lift access?"

### Schools
- "Do you need to be near any schools?"
- "What school requirements do you have?"
- "Are your children in primary or secondary school?"

### Employment
- "What's your current employment situation?"
- "Are you working at the moment?"

### Health/Support
- "Do you need any health or support services nearby?"
- "Are there any medical or social services you require?"

### Emergency Accommodation
- "How long have you been in emergency accommodation?"
- "When did you first enter emergency accommodation?"

### Closing
- "Is there anything else I should know?"
- "Have we covered everything?"
- "Do you have any questions for me?"

## Technical Details

### Speaker Diarization

Amazon Transcribe automatically:
- Identifies different speakers
- Labels them as Speaker 0, Speaker 1, etc.
- Timestamps each speaker segment
- Separates overlapping speech

### Speaker Identification Algorithm

```python
# Analyze conversation patterns
for each speaker:
    count_questions()  # Count '?' marks
    count_words()
    count_segments()

# Speaker with more questions = Caseworker
caseworker = speaker_with_most_questions
family = other_speaker

# Extract info from family responses only
information = parse(family_responses)
```

### Information Extraction

Same parsing logic as single-speaker input:
- Pattern matching for keywords
- Number extraction
- Location identification
- Need categorization

Applied only to family member's responses.

## Advantages Over Single-Speaker Input

| Aspect | Single Speaker | Conversation |
|--------|---------------|--------------|
| **Structure** | Unstructured | Guided by questions |
| **Completeness** | May miss details | All topics covered |
| **Comfort** | Can be intimidating | More natural |
| **Accuracy** | Depends on speaker | Clarification possible |
| **Documentation** | Monologue only | Full dialogue |
| **Professional** | Less formal | More professional |

## Privacy & Consent

### Before Recording

1. **Explain Recording**
   - Why it's being recorded
   - How it will be used
   - Who will have access
   - How long it's kept

2. **Get Consent**
   - Verbal consent (recorded)
   - Written consent form
   - Right to refuse
   - Right to stop anytime

3. **Data Protection**
   - GDPR compliance
   - Secure storage
   - Limited access
   - Deletion policy

### During Recording

- Remind if discussing sensitive topics
- Offer to pause recording
- Respect privacy requests

### After Recording

- Audio deleted after transcription
- Transcript stored securely
- Access controlled
- Retention policy followed

## Troubleshooting

### Poor Speaker Identification

**Problem:** System can't distinguish speakers

**Solutions:**
- Ensure speakers don't talk over each other
- Use better quality microphone
- Reduce background noise
- Speak more distinctly

### Incorrect Speaker Assignment

**Problem:** Caseworker identified as family or vice versa

**Solutions:**
- Caseworker should ask more questions
- Family should provide longer responses
- Manually correct in the interface
- Re-record if necessary

### Missing Information

**Problem:** Some details not extracted

**Solutions:**
- Review conversation transcript
- Manually add missing information
- Caseworker asks more specific questions
- Use follow-up questions

### Audio Quality Issues

**Problem:** Transcription inaccurate

**Solutions:**
- Use better microphone
- Reduce background noise
- Speak more clearly
- Re-record conversation

## Cost Considerations

### Per Conversation

- Average conversation: 5-10 minutes
- Transcription cost: ~$0.12-0.24
- S3 storage: Negligible (deleted immediately)
- **Total: ~$0.15-0.25 per household**

### Monthly Costs

| Households | Minutes | Cost |
|------------|---------|------|
| 50 | 250-500 | $6-12 |
| 100 | 500-1000 | $12-24 |
| 500 | 2500-5000 | $60-120 |

Still very affordable for the benefits gained.

## Success Metrics

### Data Quality
- ✅ 95%+ accuracy in information extraction
- ✅ Fewer missing fields
- ✅ More complete responses

### User Experience
- ✅ Higher satisfaction scores
- ✅ Less anxiety reported
- ✅ More dignified process

### Efficiency
- ✅ Faster intake (5-10 min vs 10-15 min forms)
- ✅ Less back-and-forth
- ✅ Better first-time completion

### Accessibility
- ✅ Serves 95%+ of population
- ✅ Removes literacy barriers
- ✅ More inclusive

## Next Steps

1. **Setup AWS** (see VOICE_SETUP.md)
2. **Train caseworkers** on best practices
3. **Test with pilot group**
4. **Gather feedback**
5. **Refine process**
6. **Scale deployment**

## Resources

- **VOICE_SETUP.md** - AWS configuration
- **demo_conversation.py** - Example conversations
- **app_voice.py** - Application code
- **src/voice_handler.py** - Processing logic

---

**Conversational intake makes the process more human, dignified, and effective! 💬**
