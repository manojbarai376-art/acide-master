import time

class ScraperScheduler:
    def __init__(self):
        print("⏰ Scraper Scheduler initialized!")

    def schedule_interval(self, hours=6):
        """
        यह तय करेगा कि हर निश्चित घंटे के बाद स्क्रैपर दोबारा रन हो।
        """
        print(f"⏳ Scheduler set to run scraping task every {hours} hours.")
        # यहाँ हम time module या schedule library का उपयोग करके बैकग्राउंड लूप चला सकते हैं

print("Scheduler script ready!")