from from flask import Flask, request, jsonify
import yt_dlp
import uuid
import os

app = Flask(__name__)
DOWNLOAD_DIR = "downloads"
os.makedirs(DOWNLOAD_DIR, exist_ok=True)

@app.route("/")
def home():
    return "YouTube High-Quality Downloader API is live!"

@app.route("/download", methods=["GET"])
def download_video():
    url = request.args.get("url")
    if not url:
        return jsonify({"error": "Missing 'url' parameter"}), 400

    filename = f"{uuid.uuid4()}.mp4"
    filepath = os.path.join(DOWNLOAD_DIR, filename)

    ydl_opts = {
        "format": "bestvideo+bestaudio",
        "outtmpl": filepath,
        "merge_output_format": "mp4",
        "postprocessors": [{
            "key": "FFmpegMerger",
        }],
        "quiet": True,
    }

    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url, download=True)
            return jsonify({
                "title": info.get("title"),
                "channel": info.get("uploader"),
                "duration": info.get("duration"),
                "file_path": filepath
            })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
