from flask import Flask, jsonify, send_from_directory
import os
import sys

app = Flask(__name__)

# ---------------- HEALTH ---------------- #

@app.route("/health")
def health():
    return jsonify({"status": "ok"})

# ---------------- SAFE IMPORTS ---------------- #

def get_whisper_service():
    try:
        import whisper_service
        return whisper_service
    except Exception as e:
        raise RuntimeError(f"Whisper service error: {e}")

def get_gloss_service():
    try:
        import gloss_service
        return gloss_service
    except Exception as e:
        raise RuntimeError(f"Gloss service error: {e}")

# ---------------- DEMO PATH ---------------- #

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DEMO_AUDIO_PATH = os.path.join(
    BASE_DIR, "frontend", "static", "demo", "demo_audio.wav"
)

# ---------------- ROUTES ---------------- #

@app.route("/")
def index():
    return "MVP VoiceMap backend is live 🚀"

@app.route("/transcribe-demo", methods=["POST"])
def transcribe_demo():
    if not os.path.exists(DEMO_AUDIO_PATH):
        return jsonify({"error": "Demo audio not found"}), 404

    try:
        whisper_service = get_whisper_service()
        text, language = whisper_service.transcribe(DEMO_AUDIO_PATH)
        return jsonify({"text": text, "language": language})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/sign-demo", methods=["POST"])
def sign_demo():
    if not os.path.exists(DEMO_AUDIO_PATH):
        return jsonify({"error": "Demo audio not found"}), 404

    try:
        whisper_service = get_whisper_service()
        gloss_service = get_gloss_service()

        text, _ = whisper_service.transcribe(DEMO_AUDIO_PATH)
        gloss = gloss_service.gloss_text(text)

        return jsonify({
            "transcription": text,
            "gloss": gloss
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- RUN ---------------- #

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
