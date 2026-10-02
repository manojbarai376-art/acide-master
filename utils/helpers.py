import datetime

class Helpers:
    @staticmethod
    def get_current_timestamp():
        """करंट टाइमस्टैम्प देता है"""
        return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    @staticmethod
    def clean_text(text):
        """फालतू स्पेस और कैरेक्टर्स हटाने के लिए"""
        if text:
            return " ".join(text.split())
        return ""

print("Helpers script ready!")