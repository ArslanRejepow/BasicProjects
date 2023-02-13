import youtube_dl

# URL of the Youtube audio file
urls = [
    'https://www.youtube.com/watch?v=JZWPs59Mx20',
    'https://www.youtube.com/watch?v=B4l5-7h8Dbs',
    'https://www.youtube.com/watch?v=2-rqcvp-T10',
    'https://www.youtube.com/watch?v=gtn4gSrH5tI',
    'https://www.youtube.com/watch?v=Qm6rkaOSqAM',
    'https://www.youtube.com/watch?v=bIuFi9BX0Lc',
]

# Set the download options
ydl_opts = {
    'format': 'bestaudio/best', 
    'postprocessors': [{
        'key': 'FFmpegExtractAudio',
        'preferredcodec': 'mp3',
        'preferredquality': '192',
    }],
}

# Download the audio file
for url in urls:
    with youtube_dl.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])