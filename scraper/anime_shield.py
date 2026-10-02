import time
import random

class AnimeShield:
    def __init__(self):
        print("🛡️ Anime Shield activated: Anti-bot bypass ready!")

    def get_safe_headers(self):
        """विज़िट करते समय आईपी या बॉट डिटेक्शन से बचने के लिए रैंडम हेडर्स देता है"""
        user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.2.1 Safari/605.1.15",
            "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36"
        ]
        return {
            "User-Agent": random.choice(user_agents),
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/"
        }

    def random_delay(self):
        """वेबसाइट सर्वर को शक न हो इसलिए रैंडम समय के लिए रुकता है"""
        sleep_time = random.uniform(1.5, 4.0)
        time.sleep(sleep_time)

print("Anime Shield script ready!")