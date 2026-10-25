# ClipDrop 2.0 — mobile-friendly TikTok downloader starter

## Run locally on Windows
1. Extract this ZIP.
2. Open the folder containing `app.py`, `requirements.txt`, and `templates`.
3. In File Explorer address bar, type `cmd` and press Enter.
4. Run `python -m pip install -r requirements.txt`
5. Run `python app.py`
6. Open http://127.0.0.1:5000

## Mobile paste
1. In TikTok, open a public video you own or have permission to save.
2. Tap Share -> Copy link.
3. Open the deployed ClipDrop website in your phone browser.
4. Tap **Paste copied link**. If browser clipboard permission is blocked, press and hold the input box and choose Paste.
5. Tap **Get video**.

Browsers do not allow a website to silently read the clipboard. This app reads it only after the user taps the Paste button, and browser support/HTTPS/permissions may be required.

## Public deployment using Render
1. Create a GitHub account and a new repository.
2. Upload all files from this project, including `app.py`, `requirements.txt`, `render.yaml`, and the `templates` folder.
3. Sign in to Render and connect your GitHub repository.
4. Create a new Web Service. Use build command `pip install -r requirements.txt` and start command `gunicorn app:app`.
5. Deploy. Render will provide a public HTTPS URL you can open on your phone.

## Important
- This ZIP does not itself publish a website. You must deploy it to a hosting provider.
- `yt-dlp` may fail if TikTok returns HTTP 403 or changes its systems. Watermark-free output is not guaranteed.
- For more dependable retrieval, use an authorized provider API that explicitly supports the permitted use case. Keep API keys on the server, never in browser JavaScript.
- Before public launch, add rate limiting, download cleanup, request/time limits, abuse protection, and review applicable platform terms and copyright rules.
