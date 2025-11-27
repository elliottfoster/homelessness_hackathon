# Voice Input Setup Guide

## 🎤 Voice-Enabled Application

The platform now supports **voice input** using Amazon Transcribe, allowing households to speak their information instead of filling out forms.

## Why Voice Input?

- **Accessibility**: Supports households with literacy challenges or disabilities
- **Speed**: Faster than typing for many users
- **Natural**: Speak naturally about your situation
- **Inclusive**: Works for all language proficiency levels

## Prerequisites

### 1. AWS Account

You need an AWS account with access to:
- **Amazon Transcribe** - Speech-to-text service
- **Amazon S3** - Temporary audio file storage

### 2. AWS Credentials

Configure AWS credentials on your machine:

```bash
# Install AWS CLI
pip install awscli

# Configure credentials
aws configure
```

You'll be prompted for:
- AWS Access Key ID
- AWS Secret Access Key
- Default region (e.g., `us-east-1`)
- Default output format (e.g., `json`)

### 3. S3 Bucket

Create an S3 bucket for temporary audio storage:

```bash
# Using AWS CLI
aws s3 mb s3://your-accommodation-matcher-bucket

# Or create via AWS Console:
# https://console.aws.amazon.com/s3/
```

### 4. IAM Permissions

Your AWS user/role needs these permissions:

```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "transcribe:StartTranscriptionJob",
        "transcribe:GetTranscriptionJob",
        "transcribe:DeleteTranscriptionJob"
      ],
      "Resource": "*"
    },
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject"
      ],
      "Resource": "arn:aws:s3:::your-bucket-name/*"
    }
  ]
}
```

## Installation

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

This installs:
- `streamlit` - Web framework
- `pandas` - Data processing
- `numpy` - Numerical operations
- `scikit-learn` - ML utilities
- `boto3` - AWS SDK for Python

### Step 2: Verify AWS Configuration

```bash
# Test AWS credentials
aws sts get-caller-identity

# Test S3 access
aws s3 ls s3://your-bucket-name
```

## Running the Voice-Enabled App

### Launch the Application

```bash
streamlit run app_voice.py
```

The app will open at `http://localhost:8501`

### Using Voice Input

1. **Record your audio**:
   - Use your phone, computer, or recording device
   - Speak clearly about your household situation
   - Include: adults, children, area, budget, needs, etc.

2. **Upload the audio file**:
   - Click "Upload audio file" in the Voice Input tab
   - Supported formats: MP3, WAV, FLAC, OGG, M4A

3. **Configure AWS settings**:
   - Expand "AWS Configuration"
   - Enter your AWS region (e.g., `us-east-1`)
   - Enter your S3 bucket name

4. **Process the audio**:
   - Click "Process Voice Input"
   - Wait for transcription (usually 5-15 seconds)
   - Review the extracted information
   - Edit if needed
   - Click "Find Suitable Accommodation"

## Example Voice Input

**Good example:**

> "Hello, I'm looking for accommodation. I have two adults and two children in my household. We need a place in North London. Our budget is 800 pounds per month. We need wheelchair access because my partner uses a wheelchair. We also need a primary school nearby for our kids. We've been in emergency accommodation for 35 days now. I'm currently part-time employed."

**What gets extracted:**
- Composition: 2 adults, 2 children
- Area: North London
- Budget: £800/month
- Access: Wheelchair access
- Schools: Primary school required
- Employment: Part-time employed
- Days in emergency: 35

## Troubleshooting

### "AWS credentials not found"

**Solution:**
```bash
aws configure
# Enter your credentials
```

### "Access Denied" error

**Solution:**
- Check IAM permissions
- Ensure your user has Transcribe and S3 access
- Verify bucket name is correct

### "Transcription failed"

**Possible causes:**
- Audio file format not supported
- Audio quality too poor
- File too large (max 2GB)
- Network connectivity issues

**Solutions:**
- Convert audio to MP3 or WAV
- Re-record with better quality
- Check internet connection

### "Bucket not found"

**Solution:**
```bash
# Create the bucket
aws s3 mb s3://your-bucket-name

# Verify it exists
aws s3 ls
```

### Poor transcription accuracy

**Tips for better results:**
- Speak clearly and at moderate pace
- Reduce background noise
- Use a good quality microphone
- Speak in complete sentences
- Mention numbers clearly ("eight hundred" or "800")

## Cost Considerations

### Amazon Transcribe Pricing (as of 2024)

- **First 60 minutes/month**: FREE
- **After that**: ~$0.024 per minute

**Example costs:**
- 10 households @ 2 min each = 20 min = FREE
- 100 households @ 2 min each = 200 min = ~$3.36
- 1000 households @ 2 min each = 2000 min = ~$46.56

### Amazon S3 Pricing

- **Storage**: ~$0.023 per GB/month
- **Requests**: Minimal (files deleted immediately)

**Example costs:**
- Audio files are temporary (deleted after transcription)
- Negligible cost for this use case

### Total Cost Estimate

For typical usage (100 households/month):
- Transcribe: ~$3-5/month
- S3: <$1/month
- **Total: ~$4-6/month**

## Alternative: Manual Input

If you don't want to use AWS or voice input:
- Use the "Manual Input" tab
- Fill out the form as before
- No AWS account needed

## Security & Privacy

### Data Handling

- Audio files are **temporarily** stored in S3
- Files are **automatically deleted** after transcription
- Transcripts are **not stored** by AWS (we delete the job)
- All data stays in your AWS account

### Best Practices

1. **Use encryption**: Enable S3 bucket encryption
2. **Limit access**: Use IAM policies to restrict access
3. **Monitor usage**: Check AWS CloudWatch logs
4. **Delete old data**: Set S3 lifecycle policies

### GDPR Compliance

- Audio files are processed in your AWS region
- You control all data (not shared with third parties)
- Files are deleted immediately after processing
- Transcripts are only stored in your application session

## Advanced Configuration

### Custom Vocabulary

For better accuracy with housing-specific terms:

```python
# In src/voice_handler.py, add to start_transcription_job():
Settings={
    'VocabularyName': 'housing-terms',
    'ShowSpeakerLabels': False
}
```

Create custom vocabulary in AWS Console with terms like:
- "wheelchair accessible"
- "ground floor"
- "emergency accommodation"
- "primary school"

### Multiple Languages

Change language code in `src/voice_handler.py`:

```python
LanguageCode='en-GB',  # UK English (default)
# LanguageCode='en-US',  # US English
# LanguageCode='es-ES',  # Spanish
# LanguageCode='fr-FR',  # French
```

### Real-time Transcription

For live microphone input (advanced):
- Use Amazon Transcribe Streaming API
- Requires WebSocket connection
- More complex implementation

## Support

### AWS Documentation

- [Amazon Transcribe](https://docs.aws.amazon.com/transcribe/)
- [Amazon S3](https://docs.aws.amazon.com/s3/)
- [AWS CLI](https://docs.aws.amazon.com/cli/)

### Application Documentation

- **README.md** - Full platform documentation
- **QUICKSTART.md** - Quick start guide
- **USAGE_GUIDE.md** - Usage instructions
- **VOICE_SETUP.md** - This file

## Next Steps

1. Set up AWS account and credentials
2. Create S3 bucket
3. Install dependencies: `pip install -r requirements.txt`
4. Run voice app: `streamlit run app_voice.py`
5. Test with sample audio
6. Deploy for production use

---

**Voice input makes the platform more accessible and user-friendly for all households! 🎤**
