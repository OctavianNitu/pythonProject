import threading

from Class_YouTube import YouTube
from Connection import connection
from Create_video import create_video

''' Main '''

if not connection():
    print("No Internet Connection")
    exit(1)

site = YouTube()  # Constructor

site.openYouTube()

video_thread = threading.Thread(target=site.record_video)
audio_thread = threading.Thread(target=site.record_audio)
mic_thread = threading.Thread(target=site.record_mic)

video_thread.start()
audio_thread.start()
mic_thread.start()

video_thread.join()
audio_thread.join()
mic_thread.join()

create_video("mic.wav", "output.avi")  # Select files to combine

site.audio_analyse()

input("Press ENTER to exit")

