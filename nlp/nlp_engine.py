from nlp.preprocessor import Preprocessor
from nlp.entity_extractor import EntityExtractor
from nlp.rule_extractor import RuleExtractor
from nlp.time_parser import TimeParser
from datetime import datetime, timedelta
import pytz
import re

class NLPEngine:
    def __init__(self):
        self.preprocessor = Preprocessor()
        self.entity_extractor = EntityExtractor()
        self.rule_extractor = RuleExtractor()
        self.time_parser = TimeParser()

    def validate_result(self, result):
        if not result.get('event'):
            return False, 'No event found'
        return True, 'Valid'

    def extract(self, text):
        prep_result = self.preprocessor.preprocess(text)
        if not prep_result.get('valid'):
            return {
                'event': None, 'start_time': None, 'end_time': None,
                'location': None, 'reminder_minutes': None,
                'valid': False, 'errors': [prep_result.get('error', 'Unknown error')]
            }
        
        processed_text = prep_result['normalized']
        
        rule_result = self.rule_extractor.extract_all(processed_text)
        entity_result = self.entity_extractor.extract(processed_text)
        
        event = rule_result.get('event')
        location = rule_result.get('location') or entity_result.get('location')
        reminder = rule_result.get('reminder_minutes')
        
        start_time = None
        
        # Check if text contains "trong X phut/gio nua" (in X minutes/hours from now)
        trong_phut_pattern = r'trong\s+(\d+)\s*(?:phut|p)\s+nua'
        trong_gio_pattern = r'trong\s+(\d+)\s*gio\s+nua'
        
        trong_phut_match = re.search(trong_phut_pattern, processed_text, re.IGNORECASE)
        trong_gio_match = re.search(trong_gio_pattern, processed_text, re.IGNORECASE)
        
        if trong_phut_match:
            # Calculate start_time as now + X minutes
            minutes = int(trong_phut_match.group(1))
            tz = pytz.timezone('Asia/Ho_Chi_Minh')
            now = datetime.now(tz)
            future_time = now + timedelta(minutes=minutes)
            start_time = future_time.isoformat()
        elif trong_gio_match:
            # Calculate start_time as now + X hours
            hours = int(trong_gio_match.group(1))
            tz = pytz.timezone('Asia/Ho_Chi_Minh')
            now = datetime.now(tz)
            future_time = now + timedelta(hours=hours)
            start_time = future_time.isoformat()
        elif any(c in processed_text for c in ['luc', 'vao']):
            # If text has specific time like "10 giờ"
            try:
                start_time = self.time_parser.parse_to_iso(processed_text)
            except Exception:
                pass
        
        is_valid, error_msg = self.validate_result({'event': event})
        
        return {
            'event': event,
            'start_time': start_time,
            'end_time': None,
            'location': location,
            'reminder_minutes': reminder,
            'valid': is_valid,
            'errors': [] if is_valid else [error_msg],
            'warnings': []
        }

    def extract_batch(self, texts):
        return [self.extract(text) for text in texts]

    def get_extraction_confidence(self, result):
        if not result.get('valid'):
            return 0.0
        score = 0.0
        if result.get('event'):
            score += 25
        if result.get('start_time'):
            score += 25
        if result.get('location'):
            score += 25
        if result.get('reminder_minutes'):
            score += 25
        return score
