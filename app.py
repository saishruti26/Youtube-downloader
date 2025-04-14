import streamlit as st
import requests
import os
import re
from urllib.parse import urlparse, parse_qs
from zipfile import ZipFile

st.title("🎥 YouTube Downloader to ZIP")

api_key = st.text_input("🔑 Enter your RapidAPI Key", type="password")
youtube_input = st.text_area("📋 Paste YouTube Links (one per line)")
download_button = st.button("📥 Download Videos & Create ZIP")

def extract_video_id(url):
    parsed = urlparse(url)
    if parsed.hostname == "youtu.be":
        return parsed.path[1:]
    if parsed.hostname in ("www.youtube.com", "youtube.com"):
        qs = parse_qs(parsed.query)
        return qs.get("v", [None])[0]
    return None

if download_button and api_key and youtube_input:
    os.makedirs("downloaded_videos", exist_ok=True)
    headers = {
        "x-rapidapi-host": "ytstream-download-youtube-videos.p.rapidapi.com",
        "x-rapidapi-key": api_key
    }

    urls = youtube_input.strip().split("\n")
    downloaded_files = []

    with st.spinner("Downloading..."):
        for url in urls:
            video_id = extract_video_id(url)
            if not video_id:
                st.warning(f"❌ Couldn't extract video ID from {url}")
                continue

            response = requests.get("https://ytstream-download-youtube-videos.p.rapidapi.com/dl",
                                    headers=headers,
                                    params={"id": video_id})
            try:
                data = response.json()
                download_url = data['video']['url']
                title = re.sub(r'[\\/*?:"<>|]', "", data['title'])
                filename = f"{title}.mp4"
                filepath = os.path.join("downloaded_videos", filename)

                video_data = requests.get(download_url)
                with open(filepath, "wb") as f:
                    f.write(video_data.content)

                downloaded_files.append(filepath)
                st.success(f"✅ Downloaded: {title}")
            except Exception as e:
                st.error(f"Error processing {url}: {e}")

        if downloaded_files:
            zip_path = "youtube_videos.zip"
            with ZipFile(zip_path, "w") as zipf:
                for file in downloaded_files:
                    zipf.write(file, os.path.basename(file))

            with open(zip_path, "rb") as f:
                st.download_button("🎁 Download ZIP", f, file_name=zip_path)
