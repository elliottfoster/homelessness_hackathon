# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2025-11-27

### Added
- Complete temporary accommodation matching platform
- Weighted scoring algorithm (location-first approach)
- Web-based form interface with Streamlit
- Voice input with Amazon Transcribe integration
- In-browser audio recording capability
- Conversational intake with speaker diarization
- 7 realistic household scenarios in dummy data
- 15 diverse properties across London
- UK homelessness policy enforcement (42-day limit, bedroom standards)
- Comprehensive documentation (14 files)
- Multiple demo and test scripts
- Automated setup scripts

### Core Features
- **Matching Algorithm**: Transparent weighted scoring model
  - Location: 35% (highest priority)
  - Bedroom suitability: 25%
  - Affordability: 20%
  - Access needs: 15%
  - Amenities: 5%
- **Policy Compliance**: 42-day emergency limit tracking, UK bedroom standards
- **Accessibility**: Voice input, conversational intake, in-browser recording
- **Transparency**: Detailed scoring breakdowns and explanations

### Documentation
- README.md - Complete project documentation
- QUICKSTART.md - Quick start guide
- INSTALLATION.md - Installation instructions
- USAGE_GUIDE.md - Complete usage guide
- PROJECT_SUMMARY.md - Project overview
- DELIVERABLES_CHECKLIST.md - Requirements verification
- VOICE_SETUP.md - AWS configuration guide
- CONVERSATIONAL_INTAKE_GUIDE.md - Conversational intake guide
- IN_BROWSER_RECORDING.md - In-browser recording guide
- VOICE_FEATURE_SUMMARY.md - Voice features summary
- BUGFIX.md - Bug fix documentation
- PULL_REQUEST.md - Pull request template
- INDEX.md - Complete file index
- CHANGELOG.md - This file

### Fixed
- AttributeError when CSV columns read as floats instead of strings
- Added defensive str() conversion in matching_engine.py
- Added explicit dtype specification when reading CSV files
- Function definition order in app_voice.py
- Indentation errors in voice input code
- Graceful degradation when AWS/ffmpeg not available

### Technical Details
- Python 3.11+ required
- 4 core dependencies (streamlit, pandas, numpy, scikit-learn)
- 3 optional dependencies for voice features (boto3, streamlit-audiorecorder, pydub)
- Local CSV storage (no external database required)
- AWS Transcribe for speech-to-text (optional)
- ffmpeg for audio processing (optional)

### Testing
- test_matching.py - Matching engine tests
- demo_algorithm.py - Algorithm demonstration
- demo_conversation.py - Conversational intake examples
- demo_voice_parsing.py - Voice parsing demonstration
- verify_fix.py - Bug fix verification

### Known Limitations
- Simplified bedroom calculation (doesn't account for all UK bedroom standard rules)
- Static weights (could be dynamic based on priority level)
- No real-time availability checking
- No booking/allocation workflow
- Voice features require AWS account and setup

### Security
- No hardcoded credentials
- IAM least-privilege permissions recommended
- S3 bucket encryption recommended
- Temporary audio files deleted after processing
- GDPR compliant data handling

## [Unreleased]

### Planned Features
- Real-time microphone input (no file upload)
- Custom vocabulary for housing terms
- Multi-language support
- Dynamic weight adjustment based on urgency
- Integration with real property databases
- Case worker dashboard
- Historical outcome tracking
- PDF export of results

---

## Version History

- **1.0.0** (2025-11-27) - Initial release with complete feature set
- **0.1.0** (Development) - Early prototype versions

---

## Upgrade Guide

### From 0.x to 1.0.0

This is the first stable release. If you were using development versions:

1. Update dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Regenerate data (schema unchanged):
   ```bash
   python src/generate_data.py
   ```

3. No breaking changes to core functionality

4. Voice features now optional - app.py works without AWS

---

## Support

For issues, questions, or contributions:
- Review documentation in README.md
- Check INSTALLATION.md for setup issues
- See BUGFIX.md for known issues and solutions
- Run demo scripts to understand functionality

---

**Current Version**: 1.0.0
**Release Date**: November 27, 2025
**Status**: Production Ready
