# In-Browser Audio Recording

## 🎙️ Record Conversations Directly in the App

The app now supports **in-browser audio recording** - no need to use external recording devices!

## Setup

### Step 1: Install ffmpeg (Required)

The audio recorder needs ffmpeg for audio processing.

**macOS (using Homebrew):**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get update
sudo apt-get install ffmpeg
```

**Windows:**
1. Download from https://ffmpeg.org/download.html
2. Extract to a folder (e.g., `C:\ffmpeg`)
3. Add to PATH: System Properties → Environment Variables → Path → Add `C:\ffmpeg\bin`

**Verify installation:**
```bash
ffmpeg -version
```

### Step 2: Install the Audio Recorder Package

```bash
pip install streamlit-audiorecorder
```

### Step 3: Restart the App

```bash
streamlit run app_voice.py
```

## How to Use

### 1. Choose Recording Method

In the Voice Input tab, you'll see two options:
- **📱 Record directly in browser** (NEW!)
- **📁 Upload audio file**

### 2. Record Your Conversation

**Select "Record directly in browser":**

1. Click **"🎤 Start Recording"** button
2. Have your conversation:
   - Caseworker asks questions
   - Family member responds
   - Natural dialogue
3. Click **"⏹️ Stop Recording"** when done
4. The app will show:
   - ✅ Recording captured
   - Duration of recording
   - Audio playback player

### 3. Review Your Recording

- Click the play button to listen back
- Make sure the conversation is clear
- Re-record if needed (just click Start Recording again)

### 4. Process the Recording

1. Expand "AWS Configuration" section
2. Enter your S3 bucket name
3. Click **"🎤 Process Voice Input"**
4. Wait for transcription (5-15 seconds)
5. Review the conversation transcript
6. Verify extracted information
7. Match to properties!

## Features

### ✅ What Works

- **Direct browser recording** - No external apps needed
- **Instant playback** - Review before processing
- **Automatic format** - Saves as WAV (compatible with Transcribe)
- **No file management** - Handles temp files automatically
- **Works on all devices** - Desktop, laptop, tablet

### 🎤 Recording Tips

**For Best Results:**

1. **Use a good microphone**
   - Built-in laptop mic works
   - External USB mic is better
   - Headset mic is great

2. **Minimize background noise**
   - Close windows
   - Turn off fans/AC
   - Quiet room

3. **Speak clearly**
   - Normal conversational pace
   - Don't rush
   - Pause between speakers

4. **Position microphone**
   - 6-12 inches from mouth
   - Not too close (avoid pops)
   - Not too far (avoid faintness)

5. **Test first**
   - Do a short test recording
   - Play it back
   - Adjust as needed

## Browser Compatibility

### ✅ Fully Supported

- **Chrome** (recommended)
- **Edge**
- **Firefox**
- **Safari** (macOS/iOS)
- **Opera**

### ⚠️ Requirements

- Browser must support **MediaRecorder API**
- Microphone permissions must be granted
- HTTPS or localhost (for security)

### 🔒 Privacy & Security

- **Recording stays local** until you click "Process"
- **Browser asks for permission** before accessing microphone
- **No data sent** until you explicitly process
- **Temporary files deleted** after transcription

## Troubleshooting

### "Microphone permission denied"

**Solution:**
1. Click the 🔒 or ⓘ icon in browser address bar
2. Allow microphone access
3. Refresh the page

### "Audio recorder not available"

**Solution:**
```bash
pip install streamlit-audiorecorder
streamlit run app_voice.py
```

### "Couldn't find ffmpeg or avconv"

**This is the most common issue!**

**Solution - Install ffmpeg:**

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt-get install ffmpeg
```

**Windows:**
- Download from https://ffmpeg.org/download.html
- Add to system PATH

**Verify:**
```bash
ffmpeg -version
```

Then restart the app.

### "Recording is silent"

**Check:**
- Microphone is plugged in
- Correct microphone selected in system settings
- Volume/gain is not muted
- Browser has microphone permission

### "Recording cuts off"

**Possible causes:**
- Browser tab lost focus
- Computer went to sleep
- Network interruption

**Solution:**
- Keep browser tab active
- Disable sleep mode during recording
- Re-record if needed

## Comparison: Recording Methods

| Feature | In-Browser Recording | Upload File |
|---------|---------------------|-------------|
| **Convenience** | ⭐⭐⭐⭐⭐ Very easy | ⭐⭐⭐ Need external app |
| **Quality** | ⭐⭐⭐⭐ Good | ⭐⭐⭐⭐⭐ Depends on device |
| **Setup** | ⭐⭐⭐⭐⭐ One-click | ⭐⭐⭐ Need recording app |
| **Playback** | ⭐⭐⭐⭐⭐ Instant | ⭐⭐⭐⭐ Need to find file |
| **File Management** | ⭐⭐⭐⭐⭐ Automatic | ⭐⭐⭐ Manual |

## Example Workflow

### Complete In-Browser Recording Session

1. **Open app**: `streamlit run app_voice.py`
2. **Go to Voice Input tab**
3. **Select**: "📱 Record directly in browser"
4. **Click**: "🎤 Start Recording"
5. **Have conversation** (2-5 minutes):
   - Caseworker: "Can you tell me about your household?"
   - Family: "I have two adults and two children..."
   - Continue through all questions
6. **Click**: "⏹️ Stop Recording"
7. **Review**: Play back the recording
8. **Configure AWS**: Enter S3 bucket name
9. **Click**: "🎤 Process Voice Input"
10. **Wait**: 5-15 seconds for transcription
11. **Review**: Check conversation transcript
12. **Verify**: Extracted household information
13. **Match**: Find suitable properties!

## Advanced Tips

### For Caseworkers

1. **Prepare questions** beforehand
2. **Keep recording running** throughout conversation
3. **Don't worry about pauses** - they're fine
4. **Re-record if needed** - it's easy!
5. **Save important recordings** (download before processing)

### For IT Administrators

1. **Test on target browsers** before deployment
2. **Ensure HTTPS** for production (required for mic access)
3. **Document browser requirements** for users
4. **Provide fallback** (upload option) for compatibility
5. **Monitor audio quality** and adjust guidance

## Cost Implications

**No additional cost!**
- In-browser recording is free
- Same AWS Transcribe costs as file upload
- No storage costs (temp files only)

## Future Enhancements

Potential improvements:
- Real-time transcription (streaming)
- Audio quality indicators
- Noise cancellation
- Multiple recording formats
- Recording pause/resume
- Automatic silence detection

---

**In-browser recording makes the platform even more accessible and user-friendly! 🎙️**
