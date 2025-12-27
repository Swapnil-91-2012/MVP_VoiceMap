from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

# -------------------------
# HEALTH CHECK
# -------------------------
@app.route("/health")
def health():
    return jsonify({"status": "ok"})


# -------------------------
# SERVICES
# -------------------------
def get_whisper_service():
    import whisper_service
    return whisper_service

def get_gloss_service():
    import gloss_service
    return gloss_service


# -------------------------
# PATH SETUP (ROBUST)
# -------------------------
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

BACKEND_DEMO_AUDIO = os.path.join(
    BASE_DIR, "demo", "demo_audio.wav"
)

FRONTEND_DEMO_AUDIO = os.path.abspath(
    os.path.join(BASE_DIR, "..", "frontend", "static", "demo", "demo_audio.wav")
)

def get_demo_audio_path():
    if os.path.exists(BACKEND_DEMO_AUDIO):
        return BACKEND_DEMO_AUDIO
    if os.path.exists(FRONTEND_DEMO_AUDIO):
        return FRONTEND_DEMO_AUDIO
    return None


# -------------------------
# ROOT
# -------------------------
@app.route("/")
def index():
    return "MVP VoiceMap backend is live 🚀"


# -------------------------
# TRANSCRIBER DEMO
# -------------------------
@app.route("/transcribe-demo", methods=["POST"])
def transcribe_demo():

    demo_audio = get_demo_audio_path()
    if not demo_audio:
        return jsonify({
            "error": "Demo audio not found",
            "checked": [
                BACKEND_DEMO_AUDIO,
                FRONTEND_DEMO_AUDIO
            ]
        }), 404

    whisper_service = get_whisper_service()
    text, language = whisper_service.transcribe(demo_audio)

    return jsonify({
        "text": text,
        "language": language
    })


# -------------------------
# SIGN LANGUAGE DEMO
# -------------------------
@app.route("/sign-demo", methods=["POST"])
def sign_demo():

    demo_audio = get_demo_audio_path()
    if not demo_audio:
        return jsonify({
            "error": "Demo audio not found",
