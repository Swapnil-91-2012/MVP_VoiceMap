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
            "files_in_demo": os.listdir(os.path.join(BASE_DIR, "demo")) if os.path.exists(os.path.join(BASE_DIR, "demo")) else "demo folder missing"
        }), 404

    try:
        import whisper_service
        text, language = whisper_service.transcribe(DEMO_AUDIO_PATH)
        return jsonify({"text": text, "language": language})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# ---------------- SIGN DEMO ---------------- #

@app.route("/sign-demo", methods=["POST"])
def sign_demo():
    if not os.path.exists(DEMO_AUDIO_PATH):
        return jsonify({
            "error": "Demo audio not found",
            "expected_path": DEMO_AUDIO_PATH
        }), 404

    try:
        import whisper_service
        import gloss_service

        text, _ = whisper_service.transcribe(DEMO_AUDIO_PATH)
        gloss = gloss_service.gloss_text(text)

        return jsonify({
            "transcription": text,
            "gloss": gloss
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
