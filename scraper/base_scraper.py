import requests
from bs4 import BeautifulSoup
from core.config import ANIME_SHIELD_URL

class BaseScraper:
    def __init__(self, target_url=ANIME_SHIELD_URL):
        self.target_url = target_url

    def fetch_page(self):
        """टार्गेट वेबसाइट से पेज का HTML फेच करने के लिए"""
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            response = requests.get(self.target_url, headers=headers, timeout=10)
            if response.status_code == 200:
                return response.text
            else:
                print(f"❌ Failed to fetch page. Status code: {response.status_code}")
                return None
        except Exception as e:
            print(f"⚠️ Error connecting to website: {e}")
            return None

    def parse_content(self, html_content):
        """HTML को पार्स करने के लिए सूप ऑब्जेक्ट लौटाएगा"""
        if not html_content:
            return None
        return BeautifulSoup(html_content, 'html.parser')

print("Base Scraper script ready!")