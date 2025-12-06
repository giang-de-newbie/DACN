from underthesea import word_tokenize
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
