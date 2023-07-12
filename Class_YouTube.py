import cv2
import numpy as np
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.by import By
import sounddevice as sd
import soundfile as sf
import soundcard as sc
import librosa

SAMPLERATE = 44100
FPS = 12
DURATION = 5
SCREEN_SIZE = tuple(pyautogui.size())
class YouTube:
    def __init__(self):
        self.browser = webdriver.Chrome()

    ''' Metoda pentru rularea videoclipului random '''
    def openYouTube(self):
        self.browser.get("https://www.youtube.com/")
        self.browser.maximize_window()
        self.browser.implicitly_wait(120)
        try:
            rej_cookies = self.browser.find_element(By.XPATH,
                                                    "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[1]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]").click()
        except:
            print("No cookies rejection button")

        try:
            video_rand = self.browser.find_element(By.XPATH,
                                                   "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[1]/div/ytd-rich-item-renderer[1]/div/ytd-rich-grid-media/div[1]/ytd-thumbnail/a/yt-image/img").click()
        except:
            print("No video selected")

        try:
            skipButton = self.browser.find_element(By.XPATH,
                                                   "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[18]/div/div[3]/div/div[2]/span/button/div")
            if skipButton:
                skipButton.click()
        except:
            print("No skip button")

    ''' Metoda pentru inregistrarea video '''
    def record_video(self):
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        filename = "output.avi"
        out = cv2.VideoWriter(filename, fourcc, FPS, SCREEN_SIZE)

        print("Recording video ...")

        for i in range(int(DURATION * FPS)):
            img = pyautogui.screenshot()
            frame = np.array(img)
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            out.write(frame)

        print(f"Recording saved to {filename}")

        cv2.destroyAllWindows()
        out.release()

    ''' Metoda pentru inregistrarea audio a microfonului '''
    def record_mic(self):

        print("Recording microphone ...")

        audio = sd.rec(int(DURATION * SAMPLERATE), samplerate=SAMPLERATE, channels=1)
        sd.wait()

        filename = "mic.wav"
        sf.write(filename, audio, SAMPLERATE)

        print(f"Recording saved to {filename}")

    ''' Metoda pentru inregistrare desktop '''
    def record_audio(self):

        filename = "audio.wav"

        try:
            print("Recording audio from desktop ...")

            with sc.get_microphone(id=str(sc.default_speaker().name),include_loopback=True).recorder(samplerate=SAMPLERATE) as mic:
                data = mic.record(numframes=SAMPLERATE * DURATION)
            sf.write(file=filename, data=data[:, 0], samplerate=SAMPLERATE)

            print(f"Recording saved to {filename}")
        except RuntimeError:
            print("Error!!! No desktop audio because sc.get_microphone() fails to find available microphone")

    ''' Metoda pentru analiza audio '''
    def audio_analyse(self):
        audio_file = 'mic.wav'
        audio, sr = librosa.load(audio_file, sr=None)

        print("Analysing audio...")

        rms = librosa.feature.rms(y=audio)

        rms_db = librosa.amplitude_to_db(rms, ref=np.max)

        filename = "VALUESdB.txt"
        with open(filename, 'w') as file:
            for element in rms_db:
                file.write(str(element) + '\n')