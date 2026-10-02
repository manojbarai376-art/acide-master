from database.db_manager import DBManager

class MainController:
    def __init__(self):
        print("🎮 Main Controller initialized!")

    def fetch_anime_catalog(self):
        """डेटाबेस से एनिमे कैटलॉग लोड करके यूआई को देगा"""
        data = DBManager.load_data()
        anime_list = data.get("anime_list", [])
        return anime_list

    def handle_playback(self, anime_url):
        """एनीमे वीडियो प्ले करने का लॉजिक यहाँ हैंडल होगा"""
        print(f"▶️ Loading video stream for URL: {anime_url}")
        return True

print("Main Controller script ready!")