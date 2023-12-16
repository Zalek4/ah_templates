from pytube import YouTube
import ffmpeg
import requests
import os
from pathlib import Path

# Create our download path
user = os.getlogin()
download_directory = f"C:/Users/{user}/Downloads/youtube_downloads"
# Make our download location if it doesn't exist yet
Path(download_directory).mkdir(parents=True, exist_ok=True)

def download_audio_video(url):
    video = False
    audio = False

    # See if our URL is valid
    try:
        response = requests.get(url)
    except:
        print("INVALID URL")
        prompt()
        return
    
    video_url = YouTube(url)
    for i in video_url.streams.filter(adaptive=True):
        print(i)

    # Get the default file name for the video
    filename = video_url.streams[0].default_filename
    filename_without_ext = os.path.splitext(os.path.basename(filename))[0]
    print(filename_without_ext)

    # Find a video stream to download
    try:
        video = video_url.streams.filter(mime_type="video/webm", res="1080p").first()
        print(video)
        print("1080p video found. Downloading...")
        video.download(output_path=download_directory, filename="video.webm")
        video = True
        
    except:
        print("No 1080p video available. Looking for 720p video.")

        try: 
            video = video_url.streams.filter(mime_type="video/webm", res="720p").first()
            print(video)
            print("720p video found. Downloading...")
            video.download(output_path=download_directory, filename="video.webm")
            video = True
        except:
            print("No 720p video available. Exiting...")
            return

    # Find an audio stream to download
    try:
        audio = video_url.streams.filter(mime_type="audio/mp4", type="audio").first()
        print(audio)
        print("Audio found. Downloading...")
        audio.download(output_path=download_directory, filename="audio.mp4")
        audio = True
    except:
        print("No audio available. Exiting...")
        return
    
    if video == True and audio == True:
        combine_audio_video(filename_without_ext)

    else:
        print("Only audio or video found. Unable to combine files into final video.")
        prompt()
        return
    
    prompt()

def combine_audio_video(filename):
    # Convert audio and video files into one mp4
    video_stream = ffmpeg.input(f"{download_directory}/video.webm")
    audio_stream = ffmpeg.input(f"{download_directory}/audio.mp4")
    ffmpeg.output(audio_stream, video_stream, f"{download_directory}/{filename}.mp4").run()

    # Clear old files
    os.remove(f"{download_directory}/video.webm")
    os.remove(f"{download_directory}/audio.mp4")

def prompt():
    print("Enter a YouTube video URL, or type 'exit' to kill the program:")
    choice = input()

    if choice != 'exit':
        download_audio_video(choice)
    else:
        pass

prompt()