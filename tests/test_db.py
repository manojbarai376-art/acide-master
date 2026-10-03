# Test script for Database Manager
from database.db_manager import DBManager

def test_database_load():
    print("🧪 Running test: Database load...")
    data = DBManager.load_data()
    assert isinstance(data, dict)
    print("✅ Database load test passed!")

def test_local_json_round_trip(tmp_path, monkeypatch):
    from database import db_manager

    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setattr(db_manager, "DB_PATH", str(tmp_path / "storage.json"))
    items = [{
        "title": "Example", "url": "https://example.com/anime",
        "image": "poster.jpg", "video_url": "https://cdn.example/anime.mp4",
    }]

    assert DBManager.save_data(items) is True
    assert DBManager.load_data() == {"anime_list": [{
        "title": "Example", "url": "https://example.com/anime",
        "image": "https://example.com/poster.jpg",
        "video_url": "https://cdn.example/anime.mp4",
    }]}

def test_empty_scrape_does_not_replace_existing_data(tmp_path, monkeypatch):
    from database import db_manager

    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setattr(db_manager, "DB_PATH", str(tmp_path / "storage.json"))
    items = [{"title": "Example", "url": "https://example.com/anime", "image": "poster.jpg"}]
    DBManager.save_data(items)

    assert DBManager.save_data([]) is False
    assert DBManager.load_data() == {"anime_list": [{
        "title": "Example", "url": "https://example.com/anime",
        "image": "https://example.com/poster.jpg",
    }]}

def test_scrape_refresh_preserves_existing_poster_and_video_url(tmp_path, monkeypatch):
    from database import db_manager

    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setattr(db_manager, "DB_PATH", str(tmp_path / "storage.json"))
    DBManager.save_data([{
        "title": "Example", "url": "https://example.com/anime",
        "image": "https://cdn.example/poster.jpg",
        "video_url": "https://cdn.example/anime.mp4",
    }])

    DBManager.save_data([{"title": "Example Updated", "url": "https://example.com/anime"}])

    assert DBManager.load_data()["anime_list"] == [{
        "title": "Example Updated", "url": "https://example.com/anime",
        "image": "https://cdn.example/poster.jpg",
        "video_url": "https://cdn.example/anime.mp4",
    }]

def test_empty_postgres_is_seeded_from_local_json(tmp_path, monkeypatch):
    from unittest.mock import MagicMock
    from database import db_manager

    monkeypatch.delenv("DATABASE_URL", raising=False)
    monkeypatch.setattr(db_manager, "DB_PATH", str(tmp_path / "storage.json"))
    items = [{"title": "Example", "url": "https://example.com/anime", "image": "poster.jpg"}]
    DBManager.save_data(items)

    connection = MagicMock()
    connection.cursor.return_value.__enter__.return_value.fetchall.return_value = []
    monkeypatch.setattr(DBManager, "_connect_postgres", staticmethod(lambda _: connection))
    save_to_postgres = MagicMock()
    monkeypatch.setattr(DBManager, "_save_postgres_data", staticmethod(save_to_postgres))

    normalized_items = [{
        "title": "Example", "url": "https://example.com/anime",
        "image": "https://example.com/poster.jpg",
    }]
    assert DBManager._load_postgres_data("postgresql://example") == {"anime_list": normalized_items}
    save_to_postgres.assert_called_once_with("postgresql://example", normalized_items)

def test_postgres_load_migrates_and_returns_video_url(monkeypatch):
    from unittest.mock import MagicMock

    connection = MagicMock()
    cursor = connection.cursor.return_value.__enter__.return_value
    cursor.fetchall.return_value = [(
        "Example", "https://example.com/anime", "https://example.com/poster.jpg",
        "https://cdn.example/anime.mp4",
    )]
    monkeypatch.setattr(DBManager, "_connect_postgres", staticmethod(lambda _: connection))

    data = DBManager._load_postgres_data("postgresql://example")

    assert data["anime_list"][0]["video_url"] == "https://cdn.example/anime.mp4"
    executed_sql = " ".join(call.args[0] for call in cursor.execute.call_args_list)
    assert "ADD COLUMN IF NOT EXISTS video_url" in executed_sql
    assert "video_url FROM anime_items" in executed_sql

def test_postgres_save_writes_video_url(monkeypatch):
    from unittest.mock import MagicMock

    connection = MagicMock()
    cursor = connection.cursor.return_value.__enter__.return_value
    monkeypatch.setattr(DBManager, "_connect_postgres", staticmethod(lambda _: connection))
    items = [{
        "title": "Example", "url": "https://example.com/anime",
        "image": "https://example.com/poster.jpg",
        "video_url": "https://cdn.example/anime.mp4",
    }]

    DBManager._save_postgres_data("postgresql://example", items)

    assert cursor.executemany.call_args.args[1] == [(
        "Example", "https://example.com/anime", "https://example.com/poster.jpg",
        "https://cdn.example/anime.mp4",
    )]

def test_postgres_scrape_refresh_preserves_media_fields(monkeypatch):
    existing = [{
        "title": "Example", "url": "https://example.com/anime",
        "image": "https://example.com/poster.jpg",
        "video_url": "https://cdn.example/anime.mp4",
    }]
    saved = []
    monkeypatch.setenv("DATABASE_URL", "postgresql://example")
    monkeypatch.setattr(
        DBManager, "_load_postgres_data", staticmethod(lambda _: {"anime_list": existing})
    )
    monkeypatch.setattr(
        DBManager, "_save_postgres_data", staticmethod(lambda _, items: saved.extend(items))
    )

    assert DBManager.save_data([{"title": "Updated", "url": "https://example.com/anime"}])
    assert saved[0]["image"] == existing[0]["image"]
    assert saved[0]["video_url"] == existing[0]["video_url"]

if __name__ == "__main__":
    test_database_load()