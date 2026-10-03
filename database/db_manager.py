import json
import os
from core.config import DB_PATH

class DBManager:
    @staticmethod
    def load_data():
        """डेटाबेस फाइल से डेटा रीड करता है"""
        if not os.path.exists(DB_PATH):
            return {"anime_list": []}
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading database: {e}")
            return {"anime_list": []}

    @staticmethod
    def save_data(data):
        """नया डेटा डेटाबेस फाइल में सेव करता है"""
        try:
            with open(DB_PATH, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
            print("Database updated successfully!")
        except Exception as e:
            print(f"Error saving database: {e}")

print("Database Manager script ready!")