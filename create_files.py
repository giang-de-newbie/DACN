#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Create preprocessor.py
preprocessor_code = r'''from underthesea import word_tokenize
import re

class Preprocessor:
    def __init__(self):
        self.abbreviations = {
            "vs": "voi", "k": "khong", "ko": "khong",
            "dc": "duoc", "tl": "tra loi", "nt": "nhu the",
            "ntn": "nhu the nao", "cx": "cung", "j": "gi", "ms": "moi",
            "trc": "truoc", "sau": "sau",
        }

    def expand_abbreviations(self, text):
        words = text.split()
        expanded = [self.abbreviations.get(w.lower(), w) for w in words]
        return " ".join(expanded)

    def normalize_text(self, text):
        if not text or not text.strip():
            return ""
        text = text.lower().strip()
        text = self.expand_abbreviations(text)
        text = re.sub(r"(\d+)\s*h\s*(\d+)", r"\1 gio \2 phut", text)
        text = re.sub(r"(\d+)\s*h\b", r"\1 gio", text)
        text = re.sub(r"(\d+)\s*:\s*(\d+)", r"\1 gio \2 phut", text)
        text = re.sub(r"(\d+)\s*\.\s*(\d+)", r"\1 gio \2 phut", text)
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"\s*,\s*", ", ", text)
        text = re.sub(r"\s*\.\s*$", "", text)
        return text.strip()

    def tokenize(self, text):
        if not text or not text.strip():
            return ""
        try:
            return word_tokenize(text, format="text")
        except Exception:
            return text

    def preprocess(self, text):
        if not text or not text.strip():
            return {"original": text, "normalized": "", "tokenized": "", "valid": False, "error": "Van ban rong"}
        if len(text.strip()) < 3:
            return {"original": text, "normalized": text, "tokenized": text, "valid": False, "error": "Van ban qua ngan"}
        if len(text) > 500:
            return {"original": text, "normalized": text, "tokenized": text, "valid": False, "error": "Van ban qua dai"}
        
        normalized = self.normalize_text(text)
        tokenized = self.tokenize(normalized)
        return {"original": text, "normalized": normalized, "tokenized": tokenized, "valid": True}

    def validate_input(self, text):
        errors = []
        if not text or not text.strip():
            errors.append("Vui long nhap noi dung")
            return False, errors
        if len(text.strip()) < 3:
            errors.append("Noi dung qua ngan")
            return False, errors
        if len(text) > 500:
            errors.append("Noi dung qua dai")
            return False, errors
        return True, []
'''

# Create rule_extractor.py
rule_extractor_code = r'''import re

class RuleExtractor:
    EVENT_KEYWORDS = [
        "hop", "meeting", "gap", "hen", "deadline",
        "nop", "thi", "kiem tra", "sinh nhat", "party",
        "phong van", "goi", "hoc", "lam", "du", "tap",
        "review", "seminar", "dong", "di", "du lich",
        "nhai", "tuan", "dam", "chay", "xem",
    ]

    def __init__(self):
        self.event_patterns = [
            r"(?:nham toi|nham nho)\s+(.*?)(?:\s+luc|\s+vao|\s+o|\s+nham|$)",
            r"(.*?)\s+(?:luc|vao)\s+\d+",
            r"(hop|meeting|gap|hen)\s+([^\d]*?)(?:\s+\d+|\s+luc|$)",
        ]
        self.reminder_patterns = [
            r"nham\s+truoc\s+(\d+)\s*(?:phut|p)",
            r"bao\s+truoc\s+(\d+)\s*(?:phut|p)",
            r"nham\s+truoc\s+(\d+)\s*gio",
        ]
        self.location_patterns = [
            r"(?:o|tai)\s+([^\s,]+(?:\s+[^\s,]+)*?)(?:\s*,|\s+nham|$)",
            r"phong\s+(\d+[a-z]?\d*)",
        ]

    def extract_event(self, text):
        event = None
        for pattern in self.event_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                event = match.group(1).strip()
                event = re.sub(r"\s+(?:luc|vao|o|tai|nham).*$", "", event)
                event = event.strip()
                if event and len(event) > 2:
                    break

        if not event:
            words = text.split()
            for i, word in enumerate(words):
                for keyword in self.EVENT_KEYWORDS:
                    if keyword in word.lower():
                        if i + 1 < len(words):
                            event = words[i] + " " + words[i + 1]
                        else:
                            event = words[i]
                        event = re.sub(r"\s+(?:luc|vao|o|tai|nham|khong).*$", "", event)
                        event = event.strip()
                        if event:
                            return event
                        
        return event if event and len(event) > 0 else None

    def extract_reminder_time(self, text):
        for pattern in self.reminder_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                minutes = int(match.group(1))
                if "gio" in match.group(0):
                    minutes *= 60
                return max(1, min(1440, minutes))
        return 15

    def extract_location(self, text):
        for pattern in self.location_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                location = match.group(1).strip() if match.lastindex >= 1 else None
                if location:
                    location = re.sub(r"\s*,\s*$", "", location)
                    return location
        return None

    def extract_all(self, text):
        return {
            "event": self.extract_event(text),
            "location": self.extract_location(text),
            "reminder_minutes": self.extract_reminder_time(text)
        }
'''

with open('nlp/preprocessor.py', 'w', encoding='utf-8') as f:
    f.write(preprocessor_code)

with open('nlp/rule_extractor.py', 'w', encoding='utf-8') as f:
    f.write(rule_extractor_code)

print("Updated nlp/preprocessor.py")
print("Updated nlp/rule_extractor.py with improved keyword matching")
