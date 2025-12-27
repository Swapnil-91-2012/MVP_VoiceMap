from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

def get_whisper_service():
    import whisper_service
    return whisper_service

def get_gloss_service():
    import gloss_service
    return gloss_service

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

DEMO_AUDIO_PATH = os.path.join(
    BASE_DIR, "demo", "demo_audio.wav"
)

@app.route("/")
def index():
    return "MVP VoiceMap backend is live 🚀"

@app.route("/transcribe-demo", methods=["POST"])
def transcribe_demo():
    if not os.path.exists(DEMO_AUDIO_PATH):
        return jsonify({
            "error": "Demo audio not found",
            "expected_path": DEMO_AUDIO_PATH
        }), 404

    whisper_service = get_whisper_service()
    text, language = whisper_service.transcribe(DEMO_AUDIO_PATH)

    return jsonify({
        "text": text,
        "language": language
    })

@app.route("/sign-demo", methods=["POST"])
def sign_demo():
    if not os.path.exists(DEMO_AUDIO_PATH):
        return jsonify({
            "error": "Demo audio not found",
            "expected_path": DEMO_AUDIO_PATH
        }), 404

    whisper_service = get_whisper_service()
    gloss_service = get_gloss_service()

    text, _ = whisper_service.transcribe(DEMO_AUDIO_PATH)
    gloss = gloss_service.gloss_text(text)

    return jsonify({
        "transcription": text,
        "gloss": gloss
    })

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
