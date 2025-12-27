# app.py
from flask import Flask, jsonify, send_from_directory
import os
import sys

# Import services safely
try:
    import whisper_service
    import gloss_service
except ModuleNotFoundError as e:
    print(f"Service import error: {e}", file=sys.stderr)
    sys.exit(1)

# ---------- INIT ---------- #

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
FRONTEND_DIR = os.path.join(BASE_DIR, "frontend")  # Adjust if frontend is inside same repo
DEMO_AUDIO_PATH = os.path.join(FRONTEND_DIR, "static", "demo", "demo_audio.wav")

app = Flask(
    __name__,
    static_folder=FRONTEND_DIR,
    static_url_path=""
)

# ---------- ROUTES ---------- #

@app.route("/")
def index():
    index_path = os.path.join(app.static_folder, "index.html")
    if not os.path.exists(index_path):
        return "index.html not found", 404
    return send_from_directory(app.static_folder, "index.html")


@app.route("/<path:path>")
def serve_static(path):
    full_path = os.path.join(app.static_folder, path)
    if not os.path.exists(full_path):
        return f"{path} not found", 404
    return send_from_directory(app.static_folder, path)


# ---------- MVP DEMO ENDPOINTS ---------- #

@app.route("/transcribe-demo", methods=["POST"])
def transcribe_demo():
    if not os.path.exists(DEMO_AUDIO_PATH):
        return jsonify({"error": "Demo audio not found"}), 404

    try:
        text, language = whisper_service.transcribe(DEMO_AUDIO_PATH)
        return jsonify({"text": text, "language": language})
    except Exception as e:
        return jsonify({"error": f"Transcription failed: {str(e)}"}), 500


@app.route("/sign-demo", methods=["POST"])
def sign_demo():
    if not os.path.exists(DEMO_AUDIO_PATH):
        return jsonify({"error": "Demo audio not found"}), 404

    try:
        text, language = whisper_service.transcribe(DEMO_AUDIO_PATH)
        gloss_tokens = gloss_service.gloss_text(text)

        if isinstance(gloss_tokens, list):
            gloss_str = " ".join(gloss_tokens)
        elif isinstance(gloss_tokens, str):
            gloss_str = gloss_tokens
        else:
            gloss_str = str(gloss_tokens)

        return jsonify({
            "transcription": text,
            "gloss": gloss_str
        })

    except Exception as e:
        return jsonify({"error": f"Glossing failed: {str(e)}"}), 500


# ---------- RUN ---------- #

if __name__ == "__main__":
    # Use PORT from Render or fallback to 5000
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
