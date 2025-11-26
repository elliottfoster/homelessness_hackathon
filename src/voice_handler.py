"""
Voice input handler using Amazon Transcribe for speech-to-text conversion.
Allows households to describe their needs verbally instead of filling forms.
"""
import json
import time
from pathlib import Path
from typing import Dict, Optional
import tempfile

# Optional AWS import
try:
    import boto3
    BOTO3_AVAILABLE = True
except ImportError:
    BOTO3_AVAILABLE = False
    boto3 = None

class VoiceInputHandler:
    """Handle voice input using Amazon Transcribe."""
    
    def __init__(self, region_name: str = 'us-east-1'):
        """
        Initialize AWS Transcribe client.
        
        Args:
            region_name: AWS region for Transcribe service
        """
        if not BOTO3_AVAILABLE:
            print("Warning: boto3 not installed. Voice input will not be available.")
            print("Install with: pip install boto3")
            self.transcribe_client = None
            self.s3_client = None
            return
            
        try:
            self.transcribe_client = boto3.client('transcribe', region_name=region_name)
            self.s3_client = boto3.client('s3', region_name=region_name)
        except Exception as e:
            print(f"Warning: Could not initialize AWS clients: {e}")
            self.transcribe_client = None
            self.s3_client = None
    
    def transcribe_audio(self, audio_file_path: str, bucket_name: str) -> Optional[str]:
        """
        Transcribe audio file using Amazon Transcribe.
        
        Args:
            audio_file_path: Path to audio file (mp3, wav, flac, etc.)
            bucket_name: S3 bucket name for temporary storage
            
        Returns:
            Transcribed text or None if failed
        """
        if not self.transcribe_client or not self.s3_client:
            return None
        
        try:
            # Generate unique job name
            job_name = f"household-intake-{int(time.time())}"
            file_name = Path(audio_file_path).name
            s3_key = f"transcribe-input/{file_name}"
            
            # Upload audio to S3
            self.s3_client.upload_file(audio_file_path, bucket_name, s3_key)
            file_uri = f"s3://{bucket_name}/{s3_key}"
            
            # Start transcription job with speaker diarization
            self.transcribe_client.start_transcription_job(
                TranscriptionJobName=job_name,
                Media={'MediaFileUri': file_uri},
                MediaFormat=Path(audio_file_path).suffix[1:],  # Remove leading dot
                LanguageCode='en-GB',  # UK English
                Settings={
                    'ShowSpeakerLabels': True,  # Enable speaker identification
                    'MaxSpeakerLabels': 2  # Caseworker + Family member
                }
            )
            
            # Wait for completion
            while True:
                status = self.transcribe_client.get_transcription_job(
                    TranscriptionJobName=job_name
                )
                job_status = status['TranscriptionJob']['TranscriptionJobStatus']
                
                if job_status in ['COMPLETED', 'FAILED']:
                    break
                
                time.sleep(2)
            
            if job_status == 'COMPLETED':
                # Get transcript with speaker labels
                transcript_uri = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
                import urllib.request
                with urllib.request.urlopen(transcript_uri) as response:
                    transcript_data = json.loads(response.read())
                
                # Cleanup
                self.transcribe_client.delete_transcription_job(TranscriptionJobName=job_name)
                self.s3_client.delete_object(Bucket=bucket_name, Key=s3_key)
                
                return transcript_data  # Return full data including speaker labels
            else:
                print(f"Transcription failed: {job_status}")
                return None
                
        except Exception as e:
            print(f"Error transcribing audio: {e}")
            return None
    
    def parse_conversation(self, transcript_data: Dict) -> Dict:
        """
        Parse conversation transcript with speaker labels.
        Extracts household information from caseworker-family dialogue.
        
        Args:
            transcript_data: Full transcript data from Amazon Transcribe
            
        Returns:
            Dictionary with conversation analysis and household information
        """
        # Extract full transcript text
        full_transcript = transcript_data['results']['transcripts'][0]['transcript']
        
        # Extract speaker segments
        speaker_segments = self._extract_speaker_segments(transcript_data)
        
        # Identify caseworker vs family member
        caseworker_speaker, family_speaker = self._identify_speakers(speaker_segments)
        
        # Extract family responses (where the information is)
        family_responses = [seg['text'] for seg in speaker_segments if seg['speaker'] == family_speaker]
        family_text = ' '.join(family_responses)
        
        # Parse household information from family responses
        household_info = self.parse_household_info(family_text)
        
        # Add conversation metadata
        household_info['conversation'] = {
            'full_transcript': full_transcript,
            'speaker_segments': speaker_segments,
            'caseworker_speaker': caseworker_speaker,
            'family_speaker': family_speaker,
            'num_turns': len(speaker_segments)
        }
        
        return household_info
    
    def _extract_speaker_segments(self, transcript_data: Dict) -> list:
        """Extract text segments by speaker from transcript data."""
        segments = []
        
        if 'speaker_labels' not in transcript_data['results']:
            # No speaker labels, treat as single speaker
            return [{
                'speaker': 'spk_0',
                'text': transcript_data['results']['transcripts'][0]['transcript'],
                'start_time': 0,
                'end_time': 0
            }]
        
        speaker_labels = transcript_data['results']['speaker_labels']
        items = transcript_data['results']['items']
        
        # Group items by speaker segments
        current_speaker = None
        current_text = []
        current_start = None
        
        for segment in speaker_labels['segments']:
            speaker = segment['speaker_label']
            start_time = float(segment['start_time'])
            end_time = float(segment['end_time'])
            
            # Get text for this segment
            segment_items = segment.get('items', [])
            segment_text = []
            
            for item_data in segment_items:
                # Find matching item in results
                for item in items:
                    if item.get('start_time') == item_data.get('start_time'):
                        if 'alternatives' in item and item['alternatives']:
                            segment_text.append(item['alternatives'][0]['content'])
                        break
            
            text = ' '.join(segment_text)
            
            segments.append({
                'speaker': speaker,
                'text': text,
                'start_time': start_time,
                'end_time': end_time
            })
        
        return segments
    
    def _identify_speakers(self, segments: list) -> tuple:
        """
        Identify which speaker is the caseworker vs family member.
        Caseworker typically asks questions, family member provides information.
        
        Returns:
            (caseworker_speaker_id, family_speaker_id)
        """
        if not segments:
            return ('spk_0', 'spk_1')
        
        # Count question marks and information density per speaker
        speaker_stats = {}
        
        for seg in segments:
            speaker = seg['speaker']
            text = seg['text'].lower()
            
            if speaker not in speaker_stats:
                speaker_stats[speaker] = {
                    'questions': 0,
                    'word_count': 0,
                    'segments': 0
                }
            
            speaker_stats[speaker]['questions'] += text.count('?')
            speaker_stats[speaker]['word_count'] += len(text.split())
            speaker_stats[speaker]['segments'] += 1
        
        # Caseworker likely asks more questions
        speakers = list(speaker_stats.keys())
        if len(speakers) < 2:
            return (speakers[0], speakers[0])
        
        # Speaker with more questions is likely caseworker
        caseworker = max(speakers, key=lambda s: speaker_stats[s]['questions'])
        family = [s for s in speakers if s != caseworker][0]
        
        return (caseworker, family)
    
    def parse_household_info(self, transcript: str) -> Dict:
        """
        Parse transcribed text to extract household information.
        Uses simple keyword matching and pattern recognition.
        
        Args:
            transcript: Transcribed text from voice input
            
        Returns:
            Dictionary with household information
        """
        transcript_lower = transcript.lower()
        
        household_info = {
            'household_composition': self._extract_composition(transcript_lower),
            'area_restrictions': self._extract_area(transcript_lower),
            'affordability': self._extract_budget(transcript_lower),
            'length_of_placement': self._extract_days(transcript_lower),
            'priority_need': self._extract_priority(transcript_lower),
            'eligibility': 'Eligible',  # Default
            'access_needs': self._extract_access_needs(transcript_lower),
            'schools': self._extract_schools(transcript_lower),
            'employment': self._extract_employment(transcript_lower),
            'health_social_network': self._extract_health_needs(transcript_lower),
            'caring_responsibilities': self._extract_caring(transcript_lower),
            'risk_level': self._extract_risk(transcript_lower),
            'drug_use': self._extract_substance_use(transcript_lower),
            'raw_transcript': transcript
        }
        
        return household_info
    
    def _extract_composition(self, text: str) -> str:
        """Extract household composition from text."""
        # Look for patterns like "2 adults", "3 children", etc.
        import re
        
        adults = re.search(r'(\d+|one|two|three|four|five)\s+(adult|adults)', text)
        children = re.search(r'(\d+|one|two|three|four|five)\s+(child|children|kids)', text)
        
        num_map = {'one': 1, 'two': 2, 'three': 3, 'four': 4, 'five': 5}
        
        composition_parts = []
        
        if adults:
            num = adults.group(1)
            num = num_map.get(num, num)
            composition_parts.append(f"{num} adult{'s' if str(num) != '1' else ''}")
        
        if children:
            num = children.group(1)
            num = num_map.get(num, num)
            composition_parts.append(f"{num} child{'ren' if str(num) != '1' else ''}")
        
        if composition_parts:
            return ', '.join(composition_parts)
        
        # Default
        return "1 adult"
    
    def _extract_area(self, text: str) -> str:
        """Extract preferred area from text."""
        areas = ['north london', 'east london', 'south london', 'west london', 'central london']
        
        for area in areas:
            if area in text:
                return area.title()
        
        return "North London"  # Default
    
    def _extract_budget(self, text: str) -> int:
        """Extract budget from text."""
        import re
        
        # Look for patterns like "£800", "800 pounds", etc.
        budget_match = re.search(r'£?(\d+)\s*(pounds?|per month|monthly)?', text)
        
        if budget_match:
            return int(budget_match.group(1))
        
        return 700  # Default
    
    def _extract_days(self, text: str) -> int:
        """Extract days in emergency accommodation."""
        import re
        
        days_match = re.search(r'(\d+)\s*days?', text)
        
        if days_match:
            return int(days_match.group(1))
        
        return 0  # Default
    
    def _extract_priority(self, text: str) -> str:
        """Extract priority level."""
        if 'critical' in text or 'urgent' in text or 'emergency' in text:
            return 'Critical'
        elif 'high priority' in text or 'high' in text:
            return 'High'
        elif 'medium' in text:
            return 'Medium'
        else:
            return 'Medium'  # Default
    
    def _extract_access_needs(self, text: str) -> str:
        """Extract access needs."""
        needs = []
        
        if 'wheelchair' in text:
            needs.append('Wheelchair access')
        if 'ground floor' in text:
            needs.append('Ground floor only')
        if 'lift' in text or 'elevator' in text:
            needs.append('Lift required')
        
        return ', '.join(needs) if needs else 'None'
    
    def _extract_schools(self, text: str) -> str:
        """Extract school requirements."""
        schools = []
        
        if 'primary school' in text or 'primary' in text:
            schools.append('Primary school')
        if 'secondary school' in text or 'secondary' in text:
            schools.append('Secondary school')
        
        if schools:
            return ' and '.join(schools) + ' required'
        
        return 'Not required'
    
    def _extract_employment(self, text: str) -> str:
        """Extract employment status."""
        if 'unemployed' in text or 'not working' in text or 'no job' in text:
            return 'Unemployed'
        elif 'full time' in text or 'full-time' in text:
            return 'Full-time employed'
        elif 'part time' in text or 'part-time' in text:
            return 'Part-time employed'
        elif 'self employed' in text or 'self-employed' in text:
            return 'Self-employed'
        
        return 'Unemployed'  # Default
    
    def _extract_health_needs(self, text: str) -> str:
        """Extract health/social support needs."""
        needs = []
        
        if 'mental health' in text:
            needs.append('Mental health support needed')
        if 'hospital' in text or 'medical' in text:
            needs.append('Hospital nearby needed')
        if 'substance' in text or 'drug' in text or 'alcohol' in text:
            needs.append('Substance abuse support')
        if 'domestic violence' in text or 'domestic abuse' in text:
            needs.append('Domestic violence support')
        if 'disability' in text:
            needs.append('Disability support services')
        
        return ', '.join(needs) if needs else 'None'
    
    def _extract_caring(self, text: str) -> str:
        """Extract caring responsibilities."""
        if 'young child' in text or 'baby' in text or 'infant' in text:
            return 'Yes - young children'
        elif 'elderly parent' in text or 'elderly relative' in text:
            return 'Yes - elderly parent'
        elif 'disabled child' in text:
            return 'Yes - disabled child'
        elif 'caring' in text or 'carer' in text:
            return 'Yes - other'
        
        return 'No'
    
    def _extract_risk(self, text: str) -> str:
        """Extract risk level."""
        if 'high risk' in text or 'dangerous' in text:
            return 'High'
        elif 'medium risk' in text:
            return 'Medium'
        else:
            return 'Low'
    
    def _extract_substance_use(self, text: str) -> str:
        """Extract substance use history."""
        if 'recovery' in text or 'recovering' in text:
            return 'Yes - in recovery'
        elif 'drug' in text or 'substance' in text or 'alcohol' in text:
            if 'support' in text or 'help' in text:
                return 'Yes - active support needed'
        
        return 'No'
