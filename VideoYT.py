import threading
import cv2
import numpy as np
import pyautogui
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
import requests
import sounddevice as sd
import soundfile as sf
import soundcard as sc
import librosa


######### Testare conexioune internet
def conexiune():
    if requests.get('https://google.com/'):
        return True
    else:
        return False


class YouTube:
    def __init__(self):
        self.browser = webdriver.Chrome()
        self.samplerate = 44100
    ####### Metoda pentru rularea videoclipului random
    def openYouTube(self):
        self.browser.get("https://www.youtube.com/")
        self.browser.maximize_window()
        self.browser.implicitly_wait(120)
        try:
            rej_cookies = self.browser.find_element(By.XPATH,
                                                    "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[1]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]").click()
        except:
            print("Nu avem butonul Reject ALL")

        try:
            video_rand = self.browser.find_element(By.XPATH,
                                                   "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[1]/div/ytd-rich-item-renderer[1]/div/ytd-rich-grid-media/div[1]/ytd-thumbnail/a/yt-image/img").click()
        except:
            print("Nu ajunge pana in punctul de play")

        try:
            skipButton = self.browser.find_element(By.XPATH,
                                                   "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[18]/div/div[3]/div/div[2]/span/button/div")
            if skipButton:
                skipButton.click()
        except:
            print("Nu avem buton de Skip")
        # try:
        #     # searchBar = self.browser.find_element(By.XPATH, "/html/body/ytd-app/div[1]/div/ytd-masthead/div[4]/div[2]/ytd-searchbox/form/div[1]/div[1]/div/div[2]/input")
        #     searchBar = WebDriverWait(self.browser, 10).until(EC.visibility_of_element_located((By.XPATH, "/html/body/ytd-app/div[1]/div/ytd-masthead/div[4]/div[2]/ytd-searchbox/form/div[1]/div[1]/div/div[2]/input")))
        #     searchBar.send_keys("Rammstein" + Keys.ENTER)
        # except:
        #     print("nu vede bara de SEARCH")

    ######### Metoda pentru inregisstrarea video
    def record_video(self):

        # display screen resolution, get it using pyautogui itself
        SCREEN_SIZE = tuple(pyautogui.size())
        # define the codec
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        # frames per second
        fps = 12.0
        # create the video write object
        filename = "output.avi"
        out = cv2.VideoWriter(filename, fourcc, fps, (SCREEN_SIZE))
        # the time you want to record in seconds
        record_seconds = 10

        print("Recording video ...")

        for i in range(int(record_seconds * fps)):
            # make a screenshot
            img = pyautogui.screenshot()
            # convert these pixels to a proper numpy array to work with OpenCV
            frame = np.array(img)
            # convert colors from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # write the frame
            out.write(frame)

        print(f"Recording saved to {filename}")

        # make sure everything is closed when exited

        cv2.destroyAllWindows()
        out.release()

    ######## Metoda pentru inregistrarea audio a microfonului
    def record_mic(self):

        # Set the audio settings
        sample_rate = 44100  # Sample rate in Hz
        duration = 5  # Duration of the recording in seconds

        # Record the audio
        print("Recording microphone ...")
        audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1)

        # Wait for the recording to complete
        sd.wait()

        # Save the audio to a file
        filename = "mic.wav"
        sf.write(filename, audio, sample_rate)

        print(f"Recording saved to {filename}")

    ######### Metoda pentru inregistrare desktop

    def record_audio(self):

        filename = "audio.wav"
        # samplerate = 441000
        duration = 5

        print("Recording audio from desktop ...")

        with sc.get_microphone(id=str(sc.default_speaker().name),include_loopback=True).recorder(samplerate=self.samplerate) as mic:
            data = mic.record(numframes=self.samplerate * duration)
        sf.write(file=filename, data=data[:, 0], samplerate=self.samplerate)

        print(f"Recording saved to {filename}")

    ########## Metoda pentru analiza audio
    def analiza_audio(self):

        # Load the audio file
        audio_file = r'C:\Users\nitut\PycharmProjects\pythonProject\mic.wav'
        audio, sr = librosa.load(audio_file, sr=None)

        # Calculate the root mean square (RMS) energy
        rms = librosa.feature.rms(y=audio)

        # Convert RMS to dB
        rms_db = librosa.amplitude_to_db(rms, ref=np.max)

        # Get the average dB value
        average_db = np.mean(rms_db)

        print("Average dB level:", average_db)

        filename = "VALORIdB.txt"
        with open(filename, 'w') as file:
            # Convert each element to string and write to file
            for element in rms_db:
                file.write(str(element) + '\n')

######### De aici incepe rularea programuli:

if conexiune():

    site = YouTube()


    site.openYouTube()

    # # site.record_video()
    # site.record_mic()
    # site.record_audio()

    video_thread = threading.Thread(target=site.record_video)
    audio_thread = threading.Thread(target=site.record_audio)
    mic_thread = threading.Thread(target=site.record_mic)

    video_thread.start()
    audio_thread.start()
    mic_thread.start()

    video_thread.join()
    audio_thread.join()
    mic_thread.join()

    site.analiza_audio()
    input("Nu mai exista instructiuni, apasa ENTER pentru a inchide pagina")
else:
    print("Nu se conecteaza la Internet")
