from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# ---------------- HEALTH ---------------- #

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

# ---------------- DEMO PATH ---------------- #

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEMO_AUDIO_PATH = os.path.join(BASE_DIR, "demo", "demo_audio.wav")

@app.route("/")
def index():
    return "MVP VoiceMap backend is live 🚀"

# ---------------- TRANSCRIBE DEMO ---------------- #

@app.route("/transcribe-demo", methods=["POST"])
def transcribe_demo():
    if not os.path.exists(DEMO_AUDIO_PATH):
        return jsonify({
            "error": "Demo audio not found",
            "expected_path": DEMO_AUDIO_PATH,
            "files_in_demo": os.listdir(os.path.join(BASE_DIR, "de_
