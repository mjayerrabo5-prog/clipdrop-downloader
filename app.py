import os, re, uuid
from pathlib import Path
from urllib.parse import urlparse
from flask import Flask, render_template, request, jsonify, send_file, abort
import yt_dlp

BASE_DIR = Path(__file__).resolve().parent
DOWNLOAD_DIR = BASE_DIR / "downloads"
DOWNLOAD_DIR.mkdir(exist_ok=True)
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 2 * 1024 * 1024

def is_tiktok_url(url):
    if not url or len(url) > 2000:
        return False
    try:
        p = urlparse(url.strip())
        host = (p.hostname or "").lower()
        return p.scheme in ("http", "https") and (host == "tiktok.com" or host.endswith(".tiktok.com"))
    except Exception:
        return False

@app.get("/")
def home():
    return render_template("index.html")

@app.post("/api/download")
def download_video():
    data = request.get_json(silent=True) or {}
    url = (data.get("url") or "").strip()
    if not is_tiktok_url(url):
        return jsonify(error="Please paste a valid TikTok link."), 400
    job_id = uuid.uuid4().hex
    opts = {"outtmpl": str(DOWNLOAD_DIR / f"{job_id}.%(ext)s"),
            "format": "best[ext=mp4]/best", "noplaylist": True, "quiet": True,
            "no_warnings": True, "restrictfilenames": True, "max_filesize": 200*1024*1024,
            "socket_timeout": 20, "retries": 1}
    try:
        with yt_dlp.YoutubeDL(opts) as ydl:
            info = ydl.extract_info(url, download=True)
            path = Path(ydl.prepare_filename(info))
            if not path.exists():
                candidates = list(DOWNLOAD_DIR.glob(f"{job_id}.*"))
                if not candidates:
                    raise RuntimeError("Video file was not created")
                path = candidates[0]
            return jsonify(message="Video retrieved. Watermark-free output is not guaranteed.",
                           download_url=f"/api/file/{path.name}", title=(info.get("title") or "TikTok video")[:160])
    except Exception as exc:
        app.logger.warning("Download failed: %s", exc)
        return jsonify(error="Couldn't retrieve this video. It may be restricted or the source may have changed. Try a public link you are allowed to download, or use an authorized provider API."), 422

@app.get("/api/file/<filename>")
def get_file(filename):
    if Path(filename).name != filename or not re.fullmatch(r"[a-f0-9]{32}\\.[A-Za-z0-9]{1,8}", filename):
        abort(404)
    path = DOWNLOAD_DIR / filename
    if not path.is_file():
        abort(404)
    return send_file(path, as_attachment=True, download_name=f"clipdrop-video{path.suffix}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", "5000")), debug=False)
