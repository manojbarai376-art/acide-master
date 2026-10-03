import os
from urllib.parse import urljoin, urlsplit

from flask import Flask, abort, render_template, request

from core.config import ANIME_SHIELD_URL
from database.db_manager import DBManager

app = Flask(__name__)

@app.route('/')
def index():
    try:
        db_data = DBManager.load_data()
        items = db_data.get("anime_list", []) if isinstance(db_data, dict) else db_data
    except Exception as e:
        print(f"Error loading index data: {e}")
        items = []

    return render_template('index.html', items=items)

@app.route('/anime')
@app.route('/anime/<path:anime_url>')
def anime_detail(anime_url=None):
    requested_url = anime_url or request.args.get("url", "").strip()
    if not requested_url:
        abort(404)

    requested_url = urljoin(ANIME_SHIELD_URL, requested_url)
    try:
        data = DBManager.load_data()
        items = data.get("anime_list", []) if isinstance(data, dict) else data
    except Exception as e:
        print(f"Error loading anime details: {e}")
        abort(503)

    anime = next(
        (
            item for item in items
            if isinstance(item, dict)
            and urljoin(ANIME_SHIELD_URL, item.get("url") or item.get("link") or "") == requested_url
        ),
        None,
    )
    if not anime:
        abort(404)

    video_url = (
        anime.get("video_url") or anime.get("stream_url") or anime.get("playback_url") or ""
    )
    if video_url:
        video_url = urljoin(requested_url, str(video_url).strip())
        if urlsplit(video_url).scheme not in {"http", "https"}:
            video_url = ""

    anime = {
        "title": anime.get("title") or anime.get("name") or "Anime",
        "url": requested_url,
        "image": anime.get("image") or anime.get("poster_url") or anime.get("poster") or "",
        "video_url": video_url,
    }
    return render_template('detail.html', anime=anime)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)

    def _ask_local_ai_to_fix_main_data(broken_data):
        import requests
        import json
        try:
            payload = {
                "model": "llama3",
                "prompt": f"Fix this broken data format into a clean valid JSON list structure, return only JSON: {broken_data}",
                "stream": False
        }
            response = requests.post("http://localhost:11434/api/generate", json=payload, timeout=5)
            if response.status_code == 200:
                fixed_text = response.json().get("response", "").strip()
                return json.loads(fixed_text)
            except Exception as e:
                print(f"AI Main Healer Error: {e}")
            return []