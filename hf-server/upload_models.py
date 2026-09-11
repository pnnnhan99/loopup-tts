"""
Upload TTS/ASR models from the local `public/` directory to Hugging Face Hub.

Usage:
  pip install huggingface_hub
  python hf-server/upload_models.py your-username/loopup-tts-models

Requires a valid HF token (run `huggingface-cli login` or set HF_TOKEN).
"""

import sys
from pathlib import Path

from huggingface_hub import HfApi

PROJECT_ROOT = Path(__file__).parent.parent
MODEL_DIRS = {
    "piper/vi": PROJECT_ROOT / "public" / "tts-model" / "vi",
    "piper/en": PROJECT_ROOT / "public" / "tts-model" / "en",
    "piper/id": PROJECT_ROOT / "public" / "tts-model" / "id",
    "asr": PROJECT_ROOT / "public" / "asr-model",
    "vad": PROJECT_ROOT / "public" / "vad-model",
}


def main():
    if len(sys.argv) < 2:
        print("Usage: python hf-server/upload_models.py <hf_repo_id>")
        sys.exit(1)

    repo_id = sys.argv[1]
    api = HfApi()

    # Ensure repo exists
    try:
        api.create_repo(repo_id, repo_type="model", exist_ok=True)
        print(f"Repo ready: {repo_id}")
    except Exception as e:
        print(f"Creating repo failed (continuing): {e}")

    total = 0
    for prefix, src_dir in MODEL_DIRS.items():
        if not src_dir.is_dir():
            print(f"[skip] {prefix}  (directory not found: {src_dir})")
            continue
        files = [f for f in src_dir.rglob("*") if f.is_file()]
        if not files:
            print(f"[skip] {prefix}  (empty)")
            continue
        print(f"[upload] {prefix}: {len(files)} file(s)")
        for f in files:
            rel = f.relative_to(src_dir.parent)
            dest = f"{prefix}/{rel.as_posix()}"
            print(f"  -> {dest} ({f.stat().st_size / 1e6:.1f} MB)")
            api.upload_file(path_or_fileobj=str(f), path_in_repo=dest, repo_id=repo_id, repo_type="model")
            total += 1

    print(f"\nDone. Uploaded {total} file(s) to {repo_id}")


if __name__ == "__main__":
    main()