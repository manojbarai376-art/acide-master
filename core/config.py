import os

# प्रोजेक्ट की बेस डायरेक्टरी
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# टारगेट वेबसाइट का यूआरएल (Anime Salt)
ANIME_SHIELD_URL = "https://animesalt.cx/"

# डेटाबेस फाइल का पाथ (जहाँ लिंक्स सेव होंगे)
DB_PATH = os.path.join(BASE_DIR, "database", "storage.json")

# ऐप का नाम और वर्शन
APP_NAME = "ACID Master - Anime Salt"
VERSION = "1.0.0"

print(f"[{APP_NAME}] Configuration loaded successfully!")