# app.py
from flask import Flask, jsonify, send_from_directory
import os
import sys
import traceback

# ---------- SAFE SERVICE IMPORTS ---------- #

try:
    import whisper_service
    import gloss_service
except Exception as e:
    print("❌ Service import failed:", e, file=sys.stderr)
    traceback.print_exc()
    whisper_service = None
    gloss_service = None

# ---------- PATHS ---------- #

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")
DEMO_AUDIO_PATH = os.path.join(
    FRONTEND_DIR, "static", "demo", "demo_audio.wav"
)

# ---------- FLASK INIT ---------- #

app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    static_url_path=""
)

# ---------- HEALTH CHECK (IMPORTANT FOR RENDER) ---------- #

@app.route("/health")
def health():
    return jsonify({"status": "ok"}), 200


# ---------- FRONTEND ROUTES ---------- #

@app.route("/")
def index():
    index_file = os.path.join(app.static_folder, "index.html")
    if not os.path.exists(index_file):
        return "index.html not found", 404
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def serve_static(path):
    file_path = os.path.join(app.static_folder, path)
    if not os.path.exists(file_path):
        return f"{path} not found", 404
    return send_from_directory(app.static_folder, path)


# ---------- MVP DEMO ENDPOINTS ---------- #

@app.route("/transcribe-demo", methods=["POST"])
def transcribe_demo():
    if whisper_service is None:
        return jsonify({"error": "Whisper service unavailable"}), 500

    if not os.path.exists(DEMO_AUDIO_PATH):
        return jsonify({"error": "Demo audio not found"}), 404

    try:
        text, language = whisper_service.transcribe(DEMO_AUDIO_PATH)
        return jsonify({
            "text": text,
            "language": language
        })
    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "error": f"Transcription failed: {str(e)}"
        }), 500


@app.route("/sign-demo", methods=["POST"])
def sign_demo():
    if whisper_service is None or gloss_service is None:
        return jsonify({"error": "Sign services unavailable"}), 500

    if not os.path.exists(DEMO_AUDIO_PATH):
        return jsonify({"error": "Demo audio not found"}), 404

    try:
        text, language = whisper_service.transcribe(DEMO_AUDIO_PATH)
        gloss_tokens = gloss_service.gloss_text(text)

        if isinstance(gloss_tokens, list):
            gloss_str = " ".join(gloss_tokens)
        else:
            gloss_str = str(gloss_tokens)

        return jsonify({
            "transcription": text,
            "gloss": gloss_str,
            "language": language
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({
            "error": f"Glossing failed: {str(e)}"
        }), 500


# ---------- LOCAL DEV ONLY ---------- #

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
