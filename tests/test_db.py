# Test script for Database Manager
from database.db_manager import DBManager

def test_database_load():
    print("🧪 Running test: Database load...")
    data = DBManager.load_data()
    assert isinstance(data, dict)
    print("✅ Database load test passed!")

if __name__ == "__main__":
    test_database_load()