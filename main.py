import sys
import os
import time
from threading import Thread
from flask import Flask, render_template

# प्रोजेक्ट फोल्डर को पथ में जोड़ना ताकि इम्पोर्ट करने में कोई दिक्कत न आए
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from core.config import APP_NAME, VERSION, ANIME_SHIELD_URL
from database.db_manager import DBManager
from scraper.base_scraper import BaseScraper
from scraper.anime_shield import AnimeShield
from scraper.ai_healer import AIHealer
from scraper.parser import AnimeParser

# Flask ऐप ताकि Render इसे हमेशा ऑनलाइन समझे
app = Flask(__name__)

# बैकग्राउंड वर्कर यहाँ आ जाएगा
t = Thread(target=background_worker)
t.daemon = True
t.start()

@app.route('/')
def index():
    try:
        db_data = DBManager.load_data()
        # यहाँ चेक कर रहे हैं कि डेटा डिक्शनरी में है या सीधे लिस्ट है
        if isinstance(db_data, dict):
            items = db_data.get("anime_list", [])
        elif isinstance(db_data, list):
            items = db_data
        else:
            items = []
    except Exception as e:
        print(f"Error loading index data: {e}")
        items = []
    
    return render_template('index.html', items=items)

def background_worker():
    """लूप में चलने वाला मुख्य स्क्रैपर वर्कर"""
    while True:
        print(f"========================================")
        print(f"  Starting {APP_NAME} v{VERSION}")
        print(f"========================================")
        
        try:
            # 1. डेटाबेस चेक या लोड करना
            db_data = DBManager.load_data()
            print(f"📦 Database loaded. Existing items: {len(db_data.get('items', [])) if isinstance(db_data, dict) else 0}")
            
            # 2. शील्ड और स्क्रैपर एक्टिवेट करना
            shield = AnimeShield()
            healer = AIHealer()
            
            print(f"🎯 Target URL: {ANIME_SHIELD_URL}")
            scraper = BaseScraper(ANIME_SHIELD_URL)
            
            # 3. पेज फेच करने की टेस्टिंग
            print(f"🌐 Fetching target page...")
            shield.random_delay()
            html = scraper.fetch_page()
            
            if html:
                print(f"✅ Connection successful! Page HTML fetched.")
                soup = scraper.parse_content(html)
                if soup:
                    parser = AnimeParser()
                    items = parser.parse_anime_list(soup)
                    if items:
                        DBManager.save_data(items)
                        print(f"✅ {len(items)} items saved to database successfully!")
            else:
                print(f"⚠️ Connection failed or blocked. Testing AI Healer...")
                healer.analyze_and_heal("Connection Timeout / Cloudflare Block")
                
        except Exception as e:
            print(f"❌ Error in main loop: {e}")
            
        print(f"========================================")
        print(f"🔄 Application cycle completed. Restarting in 60 seconds...")
        print(f"========================================")
        time.sleep(60)
    @app.route('/anime/<path:anime_url>')
    def anime_detail(anime_url):
    # यहाँ हम डेटाबेस से उस एनिमी की जानकारी निकालेंगे
    # और उसकी डिटेल्स detail.html पर भेजेंगे
        return render_template('detail.html', anime_url=anime_url)

if __name__ == "__main__":
    # 1. ऐप स्टार्ट होने से पहले एक बार तुरंत डेटा फेच करके सेव कर लेते हैं ताकि फाइल खाली न रहे!
    print("🚀 Initializing startup scrape...")
    try:
        startup_scraper = BaseScraper(ANIME_SHIELD_URL)
        startup_html = startup_scraper.fetch_page()
        if startup_html:
            startup_soup = startup_scraper.parse_content(startup_html)
            if startup_soup:
                parser = AnimeParser()
                initial_items = parser.parse_anime_list(startup_soup)
                if initial_items:
                    DBManager.save_data({"anime_list": initial_items})
                    print(f"✅ Startup success! Saved {len(initial_items)} items.")
    except Exception as e:
        print(f"⚠️ Startup scrape error: {e}")
    # 3. Render के लिए पोर्ट सेट करना
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)