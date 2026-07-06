import os
from yt_dlp import YoutubeDL

urlarray = []
output_dir = r"c:\temp"     #change path if needed
audio_format ="mp3"         #change format if needed
audio_bitrate = "192"

#Input URL
def URLeingabe():
     while True:
        url = input("URL (space to end): ").strip()
        if not url:
            break
        urlarray.append(url)
        print(f"URL added: {url}")

#Building several options
def build_opts(output_dir: str, audio_format: str, audio_bitrate: str):
    # Vorlage für Dateinamen: Titel – Uploader (VideoID).mp3
     outtmpl = os.path.join(output_dir, "%(title)s - %(uploader)s [%(id)s].%(ext)s")

     postprocessors = [
         {
             "key": "FFmpegExtractAudio",
             "preferredcodec": audio_format,
             "preferredquality": audio_bitrate,
        },
    # Optional: Cover/Thumbnail embed, if supported by fileformat (mp3: yes, m4a: yes)
         {
             "key": "EmbedThumbnail",
         },
    # Optional: write Metadata
         {
            "key": "FFmpegMetadata",
         },
     ]

     ydl_opts = {
         "format": "bestaudio/best",
         "outtmpl": outtmpl,
         "postprocessors": postprocessors,
         "noplaylist": True,            # Skip the entire playlist; process link by link --> Set to FALSE if desired
         "ignoreerrors": True,          # Do not abort in case of errors
         "prefer_ffmpeg": True,         # Using FFmpeg Safely
         "nocheckcertificate": False,   # Check certificates as usual
         "quiet": False,                # Set "logs" to "True" if you want it to be quieter
         "writethumbnail": True,
         # "logger": my_logger,         # optional: own logger
         "ffmpeg_location": r"C:\ffmpeg\bin\ffmpeg.exe",      #Path to ffmpeg_location. Change if needed
         "ffprobe_location": r"C:\ffmpeg\bin\ffprobe.exe",    #Path to ffprobe_location. Change if needed
     }
     return ydl_opts

#Main Function to convert urls
def download_and_convert(urlarray, output_dir, audio_format, audio_bitrate):
    opts = build_opts(output_dir, audio_format, audio_bitrate)
    failed = []

    with YoutubeDL(opts) as ydl:
         for url in urlarray:
             try:
                 print(f"Start Download/Conversion: {url}")
                 ydl.download([url])
             except Exception as e:
                 print(f"Failure at {url}: {e}")
                 failed.append((url, str(e)))

    if failed:
         print("\nNo more errors with the following URLs:")
         for url, err in failed:
             print(f"- {url}: {err}")
    else:
        print("\nAll downloads and conversions have been successfully completed.")





#MAIN

if __name__ == "__main__":
    URLeingabe()

    if urlarray:
        download_and_convert(urlarray, output_dir, audio_format, audio_bitrate)
    else:
        print("No URLs entered. Exit.")