import re

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
            r"(?:nham toi|nham nho)\s+(.*?)(?:\s+luc|\s+vao|\s+o|\s+nham|\s+trong|$)",
            r"(.*?)\s+(?:luc|vao)\s+\d+",
            r"(hop|meeting|gap|hen)\s+([^\d]*?)(?:\s+\d+|\s+luc|$)",
        ]
        self.reminder_patterns = [
            r"nham\s+truoc\s+(\d+)\s*(?:phut|p|gio)",
            r"bao\s+truoc\s+(\d+)\s*(?:phut|p|gio)",
            r"trong\s+(\d+)\s*(?:phut|p)\s+nua",
            r"trong\s+(\d+)\s*(?:gio)\s+nua",
        ]
        self.location_patterns = [
            r"(?:o|tai)\s+([^\s,]+(?:\s+[^\s,]+)*?)(?:\s*,|\s+nham|\s+trong|$)",
            r"phong\s+(\d+[a-z]?\d*)",
        ]

    def extract_event(self, text):
        event = None
        for pattern in self.event_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                event = match.group(1).strip()
                # Remove time and location information
                event = re.sub(r"\s+(?:luc|vao|o|tai|nham|trong).*$", "", event)
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
                        # Remove time and location patterns
                        event = re.sub(r"\s+(?:luc|vao|o|tai|nham|khong|trong).*$", "", event)
                        event = event.strip()
                        if event:
                            return event
                        
        return event if event and len(event) > 0 else None

    def extract_reminder_time(self, text):
        # Check for "trong X phut nua" (in X minutes) - means current time + X minutes
        for pattern in self.reminder_patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                minutes = int(match.group(1))
                # If pattern has "gio" or "hour", multiply by 60
                if "gio" in match.group(0).lower():
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
