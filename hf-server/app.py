"""
Flask server for LOOPUP-TTS on Hugging Face Spaces.
Serves the built Vue SPA and proxies model requests to Hugging Face Hub.

Environment variables:
  HF_MODEL_REPO - Hugging Face repo ID for model storage (e.g. "username/loopup-tts-models")
"""

import os
import logging
from pathlib import Path

import requests
from flask import Flask, jsonify, redirect, send_from_directory

app = Flask(__name__, static_folder=None)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Config ---
HF_MODEL_REPO = os.environ.get("HF_MODEL_REPO", "")
HF_API_BASE = "https://huggingface.co/api"
HF_RAW_BASE = "https://huggingface.co"

DIST_DIR = Path(__file__).parent.parent / "dist"


def hf_tree(path=""):
    """List files in an HF repo directory via the tree API."""
    url = f"{HF_API_BASE}/models/{HF_MODEL_REPO}/tree/main/{path}"
    resp = requests.get(url, timeout=30)
    if resp.status_code != 200:
        return []
    return resp.json()


def hf_resolve(path):
    """Build a direct-download URL for a file in the HF repo."""
    return f"{HF_RAW_BASE}/{HF_MODEL_REPO}/resolve/main/{path}"


# --------------- API: Vietnamese TTS models ---------------

@app.route("/api/models")
@app.route("/api/models/")
def api_models():
    """List Vietnamese TTS models (piper/vi/)."""
    try:
        files = hf_tree("piper/vi")
        models = sorted({
            f["path"].rsplit("/", 1)[-1].replace(".onnx.json", "")
            for f in files
            if f.get("type") == "file" and f["path"].endswith(".onnx.json")
        })
        return jsonify({"models": models})
    except Exception as e:
        logger.exception("Error listing models")
        return jsonify({"error": str(e)}), 500


@app.route("/api/piper/<lang>/models")
def api_piper_lang_models(lang):
    """List TTS models for a language (piper/{lang}/)."""
    try:
        files = hf_tree(f"piper/{lang}")
        models = sorted({
            f["path"].rsplit("/", 1)[-1].replace(".onnx.json", "")
            for f in files
            if f.get("type") == "file" and f["path"].endswith(".onnx.json")
        })
        return jsonify({"models": models})
    except Exception as e:
        logger.exception("Error listing piper models for %s", lang)
        return jsonify({"error": str(e)}), 500


# --------------- API: ASR models ---------------

@app.route("/api/asr/models")
def api_asr_models():
    """List ASR model directories (asr/)."""
    try:
        files = hf_tree("asr")
        dirs = {
            f["path"].split("/")[1]
            for f in files
            if f.get("type") == "file" and f["path"].startswith("asr/")
        }
        return jsonify({"models": sorted(dirs)})
    except Exception as e:
        logger.exception("Error listing ASR models")
        return jsonify({"error": str(e)}), 500


# --------------- API: Model file proxy (302 redirect) ---------------
# NOTE: order matters - more specific routes must be defined first,
# otherwise the catch-all `/api/model/<path:name>` would shadow them.

@app.route("/api/model/piper/<lang>/<path:name>")
def api_piper_model_file(lang, name):
    """Serve a language-specific model file by redirecting to HF Hub."""
    return redirect(hf_resolve(f"piper/{lang}/{name}"), code=302)


@app.route("/api/model/asr/<model>/<path:name>")
def api_asr_model_file(model, name):
    """Serve an ASR model file by redirecting to HF Hub."""
    return redirect(hf_resolve(f"asr/{model}/{name}"), code=302)


@app.route("/api/model/<path:name>")
def api_model_file(name):
    """Serve a Vietnamese model file by redirecting to HF Hub."""
    return redirect(hf_resolve(f"piper/vi/{name}"), code=302)


# --------------- SPA static files (catch-all, defined last) ---------------

@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
def serve_spa(path):
    """Serve Vue SPA: static files from dist/, fallback to index.html."""
    if path:
        file_path = DIST_DIR / path
        if file_path.is_file():
            return send_from_directory(DIST_DIR, path)

    index = DIST_DIR / "index.html"
    if index.is_file():
        return send_from_directory(DIST_DIR, "index.html")
    return "Not found", 404


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 7860))
    app.run(host="0.0.0.0", port=port, debug=False)
