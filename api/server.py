from flask import Flask

app = Flask(__name__)

@app.route("/")
def home():
    return {"status": "success", "message": "ACID Master API Server is running smoothly!"}

if __name__ == "__main__":
    print("🌐 Starting ACID API Server...")
    app.run(host="0.0.0.0", port=5000, debug=True)