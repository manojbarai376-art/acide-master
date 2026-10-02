import sys
import os

# प्रोजेक्ट फोल्डर को पाथ में जोड़ना ताकि इम्पोर्ट करने में कोई दिक्कत न आए
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.config import APP_NAME, VERSION, ANIME_SHIELD_URL
from database.db_manager import DBManager
from scraper.base_scraper import BaseScraper
from scraper.anime_shield import AnimeShield
from scraper.ai_healer import AIHealer

def main():
    print(f"========================================")
    print(f"  🚀 Starting {APP_NAME} v{VERSION}")
    print(f"========================================")

    # 1. डेटाबेस चेक या लोड करना
    db_data = DBManager.load_data()
    print(f"📂 Database loaded. Existing items: {len(db_data.get('anime_list', []))}")

    # 2. शील्ड और स्क्रैपर एक्टिवेट करना
    shield = AnimeShield()
    healer = AIHealer()
    
    print(f"🎯 Target URL: {ANIME_SHIELD_URL}")
    scraper = BaseScraper(ANIME_SHIELD_URL)

    # 3. पेज फेच करने की टेस्टिंग
    print("🔄 Fetching target page...")
    shield.random_delay()
    html = scraper.fetch_page()

    if html:
        print("✅ Connection successful! Page HTML fetched.")
        soup = scraper.parse_content(html)
        # यहाँ हम आगे पार्सिंग और एआई हीलर का लॉजिक जोड़ेंगे
    else:
        print("⚠️ Connection failed or blocked. Testing AI Healer...")
        healer.analyze_and_heal("Connection Timeout / Cloudflare Block", "")

    print("========================================")
    print("✨ ACID Master application run completed successfully!")

if __name__ == "__main__":
    main()