import asyncio
import yt_dlp

async def download_video(url, uuid):
    if "youtube.com" in url or "youtu.be" in url:
        ydl_opts = {
            "format": "bestvideo[height<=480]+bestaudio/best[height<=480]",
            "outtmpl": f"tmepvid_{uuid}.%(ext)s",
        }
    else:
        ydl_opts = {
            "format": "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "outtmpl": f"tmepvid_{uuid}.%(ext)s",
        }

    def progress_hook(d):
        if d["status"] == "downloading":
            print(f"Downloading: {d['filename']} - {d.get('_percent_str', '0%')}")
        elif d["status"] == "finished":
            print(f"Download complete: {d['filename']}")

    ydl_opts["progress_hooks"] = [progress_hook]

    loop = asyncio.get_event_loop()
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        await loop.run_in_executor(None, ydl.download, [url])