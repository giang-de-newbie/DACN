from underthesea import ner
import re

class EntityExtractor:
    def __init__(self):
        pass

    def extract_entities_with_ner(self, text):
        try:
            entities = ner(text)
            result = {}
            for word, tag in entities:
                if tag == 'TIME':
                    result['time'] = word
                elif tag == 'LOCATION':
                    result['location'] = word
            return result
        except:
            return {}

    def extract_entities_fallback(self, text):
        result = {}
        location_match = re.search(r'(?:o|tai)\s+([^,\.]+)', text, re.IGNORECASE)
        if location_match:
            result['location'] = location_match.group(1).strip()
        return result

    def extract(self, text):
        result = self.extract_entities_with_ner(text)
        if not result:
            result = self.extract_entities_fallback(text)
        return result
