import json
import os
import re
import tempfile
from urllib.parse import unquote, urljoin, urlsplit

from core.config import ANIME_SHIELD_URL
from core.config import DB_PATH

class DBManager:
    @staticmethod
    def _normalize_data(data):
        if isinstance(data, dict):
            data = data.get("anime_list", data.get("items", []))
        if not isinstance(data, list):
            return []

        normalized = []
        seen_urls = set()
        for item in data:
            if not isinstance(item, dict):
                continue
            anime_url = str(item.get("url") or item.get("link") or "").strip()
            if not anime_url:
                continue
            anime_url = urljoin(ANIME_SHIELD_URL, anime_url)
            if urlsplit(anime_url).scheme not in {"http", "https"} or anime_url in seen_urls:
                continue

            title = str(item.get("title") or item.get("name") or "").strip()
            if (
                not title
                or re.fullmatch(r"(?:season|episode|ep)\s*\d+", title, re.IGNORECASE)
                or re.search(r"[\u0900-\u097F]", title)
            ):
                slug = unquote(urlsplit(anime_url).path.rstrip("/").split("/")[-1])
                title = re.sub(r"[-_]+", " ", slug).strip().title()
            if not title:
                continue

            image = str(
                item.get("image") or item.get("poster_url") or item.get("poster") or ""
            ).strip()
            image = urljoin(anime_url, image) if image else ""
            if image and urlsplit(image).scheme not in {"http", "https"}:
                image = ""

            normalized_item = {"title": title, "url": anime_url, "image": image}
            video_url = (
                item.get("video_url") or item.get("stream_url") or item.get("playback_url")
            )
            if video_url:
                video_url = urljoin(anime_url, str(video_url).strip())
                if urlsplit(video_url).scheme in {"http", "https"}:
                    normalized_item["video_url"] = video_url

            normalized.append(normalized_item)
            seen_urls.add(anime_url)
        return normalized

    @staticmethod
    def _preserve_media_fields(items, existing_items):
        existing_by_url = {item["url"]: item for item in existing_items if item.get("url")}
        for item in items:
            existing = existing_by_url.get(item["url"], {})
            for field in ("image", "video_url"):
                if not item.get(field) and existing.get(field):
                    item[field] = existing[field]

    @staticmethod
    def _database_url():
        database_url = os.environ.get("DATABASE_URL")
        if database_url and database_url.startswith("postgres://"):
            return database_url.replace("postgres://", "postgresql://", 1)
        return database_url

    @staticmethod
    def _connect_postgres(database_url):
        import psycopg2

        return psycopg2.connect(database_url)

    @classmethod
    def _load_postgres_data(cls, database_url):
        connection = cls._connect_postgres(database_url)
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "CREATE TABLE IF NOT EXISTS anime_items ("
                        "url TEXT PRIMARY KEY, title TEXT NOT NULL, image TEXT NOT NULL DEFAULT '', "
                        "video_url TEXT NOT NULL DEFAULT '')"
                    )
                    cursor.execute(
                        "ALTER TABLE anime_items ADD COLUMN IF NOT EXISTS "
                        "video_url TEXT NOT NULL DEFAULT ''"
                    )
                    cursor.execute("SELECT title, url, image, video_url FROM anime_items ORDER BY title")
                    items = cls._normalize_data([
                        {"title": title, "url": url, "image": image, "video_url": video_url}
                        for title, url, image, video_url in cursor.fetchall()
                    ])
            if not items:
                items = cls._load_json_data()["anime_list"]
                if items:
                    cls._save_postgres_data(database_url, items)
            return {"anime_list": items}
        finally:
            connection.close()

    @classmethod
    def _save_postgres_data(cls, database_url, items):
        connection = cls._connect_postgres(database_url)
        try:
            with connection:
                with connection.cursor() as cursor:
                    cursor.execute(
                        "CREATE TABLE IF NOT EXISTS anime_items ("
                        "url TEXT PRIMARY KEY, title TEXT NOT NULL, image TEXT NOT NULL DEFAULT '', "
                        "video_url TEXT NOT NULL DEFAULT '')"
                    )
                    cursor.execute(
                        "ALTER TABLE anime_items ADD COLUMN IF NOT EXISTS "
                        "video_url TEXT NOT NULL DEFAULT ''"
                    )
                    cursor.execute("DELETE FROM anime_items")
                    cursor.executemany(
                        "INSERT INTO anime_items (title, url, image, video_url) "
                        "VALUES (%s, %s, %s, %s)",
                        [
                            (item["title"], item["url"], item.get("image", ""), item.get("video_url", ""))
                            for item in items
                        ],
                    )
        finally:
            connection.close()

    @staticmethod
    def load_data():
        """Return anime data in a consistent wrapper from Postgres or local JSON."""
        database_url = DBManager._database_url()
        if database_url:
            return DBManager._load_postgres_data(database_url)

        return DBManager._load_json_data()

    @staticmethod
    def _load_json_data():
        if not os.path.exists(DB_PATH):
            return {"anime_list": []}
        try:
            with open(DB_PATH, "r", encoding="utf-8") as f:
                return {"anime_list": DBManager._normalize_data(json.load(f))}
        except Exception as e:
            print(f"⚠️️ Error loading database: {e}. Asking Local AI to heal...")
            try:
                with open(DB_PATH, "r", encoding="utf-8") as f:
                    raw_content = f.read()
                healed = DBManager._ask_local_ai_to_fix_json(raw_content)
                if healed:
                    return {"anime_list": DBManager._normalize_data(healed)}
            except:
                pass
            return {"anime_list": []}

    @staticmethod
    def save_data(data):
        """Save a non-empty scrape result without discarding existing records."""
        items = DBManager._normalize_data(data)
        unique_items = []
        seen_urls = set()
        for item in items:
            if not isinstance(item, dict) or not item.get("title") or not item.get("url"):
                continue
            if item["url"] in seen_urls:
                continue
            seen_urls.add(item["url"])
            normalized_item = {
                "title": str(item["title"]),
                "url": str(item["url"]),
                "image": str(item.get("image") or ""),
            }
            if item.get("video_url"):
                normalized_item["video_url"] = str(item["video_url"])
            unique_items.append(normalized_item)

        if not unique_items:
            print("No valid anime items to save; keeping existing data.")
            return False

        try:
            database_url = DBManager._database_url()
            if database_url:
                existing_items = DBManager._load_postgres_data(database_url)["anime_list"]
            else:
                existing_items = DBManager._load_json_data()["anime_list"]
            DBManager._preserve_media_fields(unique_items, existing_items)

            if database_url:
                DBManager._save_postgres_data(database_url, unique_items)
            else:
                os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
                temporary_path = None
                try:
                    with tempfile.NamedTemporaryFile(
                        "w", encoding="utf-8", dir=os.path.dirname(DB_PATH),
                        delete=False, suffix=".tmp"
                    ) as f:
                        temporary_path = f.name
                        json.dump({"anime_list": unique_items}, f, indent=4, ensure_ascii=False)
                    os.replace(temporary_path, DB_PATH)
                finally:
                    if temporary_path and os.path.exists(temporary_path):
                        os.remove(temporary_path)
            print("Database updated successfully!")
            return True
        except Exception as e:
            print(f"Error saving database: {e}")
            raise

        @staticmethod
        def _ask_local_ai_to_fix_json(broken_data):
            import requests
            try:
                payload = {
                    "model": "llama3",
                    "prompt": f"Fix this broken data format into a clean valid JSON list structure, return only JSON: {broken_data}",
                    "stream": False
                }
                response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=5)
                if response.status_code == 200:
                    import json
                    fixed_text = response.json().get("response", "").strip()
                    return json.loads(fixed_text)
            except Exception as e:
                print(f"AI DB Healer Error: {e}")
            return []