from moviepy.audio.io.AudioFileClip import AudioFileClip
from moviepy.video.compositing.CompositeVideoClip import CompositeVideoClip
from moviepy.video.io.VideoFileClip import VideoFileClip

''' Metoda pentru cuplarea celer doua output-uri '''
def create_video(audio_filename, screen_video_filename):
    audio = AudioFileClip(audio_filename)
    video_file = VideoFileClip(screen_video_filename)

    ratio1 = audio.duration / video_file.duration
    video1 = (video_file.fl_time(lambda t: t / ratio1, apply_to=['video']).set_end(audio.duration))

    video = CompositeVideoClip([video_file]).set_audio(audio)
    video_filename = "Merged.mp4"
    video.write_videofile(video_filename, codec='libx264', fps=12)