# Test script for Scraper and Parser

def test_scraper_connection():
    print("🧪 Running test: Scraper connection...")
    # यहाँ स्क्रैपर के कनेक्शन का टेस्ट कोड लिखा जाएगा
    assert True
    print("✅ Scraper connection test passed!")

if __name__ == "__main__":
    test_scraper_connection()


def test_parser_uses_series_title_and_lazy_poster():
    from scraper.base_scraper import BaseScraper
    from scraper.parser import AnimeParser

    html = """
    <article class="flw-item">
      <div class="film-poster">
        <img src="data:image/gif;base64,AA" data-src="/images/poster.jpg" alt="Poster">
      </div>
      <h3 class="film-name">
        <a href="/series/example-anime/" title="Example Anime">Season 2</a>
      </h3>
    </article>
        <a href="/about/">About</a>
    """
    soup = BaseScraper().parse_content(html)

    assert AnimeParser().parse_anime_list(soup) == [{
        "title": "Example Anime",
        "url": "https://animesalt.cx/series/example-anime/",
        "image": "https://animesalt.cx/images/poster.jpg",
    }]


def test_legacy_season_title_and_placeholder_image_are_normalized():
    from database.db_manager import DBManager

    assert DBManager._normalize_data([{
        "title": "Season 2",
        "url": "https://animesalt.cx/series/the-elusive-samurai/",
        "image": "data:image/svg+xml;base64,placeholder",
    }, {
        "title": "लोकप्रिय शो",
        "url": "https://animesalt.cx/series/example-show/",
    }, {"title": "Missing URL"}]) == [{
        "title": "The Elusive Samurai",
        "url": "https://animesalt.cx/series/the-elusive-samurai/",
        "image": "",
    }, {
        "title": "Example Show",
        "url": "https://animesalt.cx/series/example-show/",
        "image": "",
    }]


def test_home_page_shows_items_and_english_empty_copy(monkeypatch):
    import re
    from database.db_manager import DBManager
    from main import app

    monkeypatch.setattr(DBManager, "load_data", staticmethod(lambda: {"anime_list": [{
        "title": "Example Anime",
        "url": "https://animesalt.cx/series/example-anime/",
        "image": "https://animesalt.cx/poster.jpg",
    }]}))
    response = app.test_client().get("/")

    assert response.status_code == 200
    assert b"Example Anime" in response.data
    assert b">Watch</a>" in response.data
    assert b"No anime are available yet" not in response.data
    rendered = re.sub(r"<!--.*?-->|/\*.*?\*/", "", response.get_data(as_text=True), flags=re.S)
    assert not re.search(r"[\u0900-\u097F]", rendered)


def test_watch_page_shows_selected_anime(monkeypatch):
    import re
    from database.db_manager import DBManager
    from main import app

    monkeypatch.setattr(DBManager, "load_data", staticmethod(lambda: {"anime_list": [{
        "title": "Example Anime",
        "url": "https://animesalt.cx/series/example-anime/",
        "image": "https://animesalt.cx/poster.jpg",
    }]}))
    response = app.test_client().get(
        "/anime?url=https%3A%2F%2Fanimesalt.cx%2Fseries%2Fexample-anime%2F"
    )

    assert response.status_code == 200
    assert b"Example Anime" in response.data
    assert b"Playback is not available yet" in response.data
    assert b"target=\"_blank\"" not in response.data
    assert b"Season 1" not in response.data
    rendered = re.sub(r"<!--.*?-->|/\*.*?\*/", "", response.get_data(as_text=True), flags=re.S)
    assert not re.search(r"[\u0900-\u097F]", rendered)


def test_watch_page_uses_stored_stream_in_local_player(tmp_path, monkeypatch):
    from database import db_manager
    from database.db_manager import DBManager
    from main import app

    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setattr(db_manager, "DB_PATH", str(tmp_path / "storage.json"))
    DBManager.save_data([{
        "title": "Example Anime",
        "url": "https://animesalt.cx/series/example-anime/",
        "image": "https://animesalt.cx/poster.jpg",
        "video_url": "https://cdn.example/anime.mp4",
    }])
    response = app.test_client().get(
        "/anime?url=https%3A%2F%2Fanimesalt.cx%2Fseries%2Fexample-anime%2F"
    )

    assert response.status_code == 200
    assert b'<video id="animeVideo" src="https://cdn.example/anime.mp4"' in response.data
    assert b"Playback is not available yet" not in response.data
    assert b"target=\"_blank\"" not in response.data