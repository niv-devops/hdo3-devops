from flask import (
    Flask,
    request,
    jsonify,
    send_from_directory,
    session,
    redirect,
    url_for,
)
from flask_cors import CORS
from flask_session import Session
from pymongo import MongoClient
import logging
from logging_loki import LokiHandler
import os
import sys

app = Flask(__name__, static_url_path="")

loki_handler = LokiHandler(
    url="http://loki-grafana-loki-gateway.default.svc.cluster.local/loki/api/v1/push",
    tags={"application": "test-app"},
    version="1",
)

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        loki_handler,
    ],
)

app.config["SESSION_TYPE"] = "mongodb"
app.config["SECRET_KEY"] = "your-secret-key"

MONGO_USERNAME = os.getenv("MONGO_USERNAME")
MONGO_PASSWORD = os.getenv("MONGO_PASSWORD")
INTERNAL_SERVER_ERROR_MESSAGE = "Internal server error"
LOGIN_HTML = "login.html"

uri = f"mongodb://{MONGO_USERNAME}:{MONGO_PASSWORD}@floopybird-my-mongodb.floopyfloopy.svc.cluster.local/?authSource=admin&authMechanism=SCRAM-SHA-256"
client = MongoClient(uri)
app.config["SESSION_MONGODB"] = client
app.config["SESSION_MONGODB_DB"] = "flappybird"
app.config["SESSION_MONGODB_COLLECT"] = "sessions"
Session(app)

CORS(app)

db = client.flappybird
scores = db.scores
users = db.users


@app.route("/")
def serve_index():
    if "username" not in session:
        return redirect(url_for("login"))
    return send_from_directory("static", "index.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        try:
            data = request.json
            username = data.get("username")
            password = data.get("password")

            if not username or username.strip() == "":
                return jsonify({"error": "Username is required"}), 400
            if not username.strip().isalpha():
                return jsonify({"error": "Username must contain only letters"}), 400
            user = users.find_one({"username": username})
            if not user:
                users.insert_one({"username": username, "password": password})
            session["username"] = username
            return jsonify({"message": "Registration successful!"}), 200

        except Exception as e:
            app.logger.error(f"Unexpected error during registration: {e}")
            return jsonify({"error": "Internal server error"}), 500
    return send_from_directory("static", LOGIN_HTML)


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            data = request.json
            username = data.get("username")
            password = data.get("password")
            user = users.find_one({"username": username})
            if user == None:
                return jsonify({"error": "Username must be registerd"}), 400
            if password == user.get("password"):
                session["username"] = username
                app.logger.info(f"{username} - Login success from Loki.")
                return jsonify(
                    {"message": "Login successful!", "redirect_url": "/"}
                ), 200
            else:
                return jsonify({"error": " The password is wrong"}), 400

        except Exception as e:
            app.logger.error(f"Unexpected error during login: {e}")
            return jsonify({"error": INTERNAL_SERVER_ERROR_MESSAGE}), 500

    return send_from_directory("static", LOGIN_HTML)


@app.route("/logout", methods=["POST"])
def logout():
    try:
        session.clear()
        return send_from_directory("static", LOGIN_HTML)
    except Exception as e:
        app.logger.error(f"Unexpected error during logout: {e}")
        return jsonify({"error": INTERNAL_SERVER_ERROR_MESSAGE}), 500


@app.route("/submit-score", methods=["POST"])
def submit_score():
    if "username" not in session:
        return jsonify({"error": "Unauthorized"}), 401
    try:
        data = request.json
        score = data.get("score")
        if not isinstance(score, (int, float)):
            return jsonify({"error": "Invalid data"}), 400
        score_users = list(scores.find({"username": session["username"]}, {"_id": 0}))
        if len(score_users) > 0:
            last_score = score_users[0].get("score")
            if score > last_score:
                scores.update_one(
                    {"username": session["username"]}, {"$set": {"score": score}}
                )
        else:
            scores.insert_one({"username": session["username"], "score": score})
        return jsonify({"message": "Score saved successfully!"}), 200
    except Exception as e:
        app.logger.error(f"Unexpected error during score submission: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/leaderboard", methods=["GET"])
def get_leaderboard():
    try:
        top_scores = list(scores.find({}, {"_id": 0}).sort("score", -1).limit(20))
        return jsonify(top_scores), 200
    except Exception as e:
        app.logger.error(f"Unexpected error while fetching leaderboard: {e}")
        return jsonify({"error": str(e)}), 500


@app.route("/health", methods=["GET"])
def health_check():
    try:
        client.admin.command("ping")
        return jsonify({"status": "UP"}), 200
    except Exception as e:
        return jsonify({"status": "DOWN", "error": str(e)}), 500


if __name__ == "__main__":
    try:
        app.run(debug=True, host="0.0.0.0", port=3000)
    except Exception as e:
        app.logger.error(f"Unexpected error during application startup: {e}")
