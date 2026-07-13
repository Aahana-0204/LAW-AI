"""Minimal Vercel Python test — no app imports."""
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "message": "LAWAI Backend is running"})

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def fallback(path):
    return jsonify({"path": path, "status": "minimal mode"}), 200
