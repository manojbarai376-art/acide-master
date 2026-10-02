from flask import Blueprint, jsonify
from database.db_manager import DBManager

api_bp = Blueprint("api", __name__, url_prefix="/api")

@api_bp.route("/anime", methods=["GET"])
def get_anime_list():
    """डेटाबेस से सभी एनिमे की लिस्ट फेच करके JSON फॉर्मेट में देगा"""
    data = DBManager.load_data()
    return jsonify({
        "status": "success",
        "count": len(data.get("anime_list", [])),
        "data": data.get("anime_list", [])
    })

@api_bp.route("/health", methods=["GET"])
def health_check():
    """सर्वर और सिस्टम की सेहत चेक करने के लिए"""
    return jsonify({
        "status": "healthy",
        "shield": "active",
        "ai_healer": "ready"
    })

print("API Routes script ready!")