import os
from flask import Flask, render_template

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

@app.route('/anime/<path:anime_url>')
def anime_detail(anime_url):
    return render_template('detail.html', anime_url=anime_url)

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)