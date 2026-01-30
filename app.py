from flask import Flask, request, jsonify, send_file
from pymongo import MongoClient
from datetime import datetime

# Create Flask app
app = Flask(__name__)

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["github_webhook_db"]
collection = db["events"]

# Webhook endpoint (GitHub hits this)
@app.route("/webhook", methods=["POST"])
def github_webhook():
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.json

    if event_type == "push":
        event_data = {
            "author": payload["pusher"]["name"],
            "action": "push",
            "to_branch": payload["ref"].split("/")[-1],
            "from_branch": None,
            "timestamp": datetime.utcnow()
        }
        collection.insert_one(event_data)
        return jsonify({"status": "push stored"}), 200

    elif event_type == "pull_request":
        event_data = {
            "author": payload["pull_request"]["user"]["login"],
            "action": "pull_request",
            "from_branch": payload["pull_request"]["head"]["ref"],
            "to_branch": payload["pull_request"]["base"]["ref"],
            "timestamp": datetime.utcnow()
        }
        collection.insert_one(event_data)
        return jsonify({"status": "pull request stored"}), 200

    return jsonify({"status": "ignored"}), 200

# API for UI polling
@app.route("/events", methods=["GET"])
def get_latest_events():
    events = list(
        collection.find({}, {"_id": 0}).sort("timestamp", -1).limit(10)
    )
    
    # Format timestamps for display
    for event in events:
        event["timestamp"] = event["timestamp"].strftime("%d %B %Y - %I:%M %p UTC")
    
    return jsonify(events)

# Serve UI
@app.route("/")
def serve_ui():
    return send_file("index.html")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)