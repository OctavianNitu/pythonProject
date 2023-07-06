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


def conexiune():
    try:
        requests.get('https://google.com/')
        return True
    except:
        return False

class YouTube:
    def __init__(self):
        self.browser = webdriver.Chrome()

    def openYouTube(self):
        self.browser.get("https://www.youtube.com/")
        self.browser.maximize_window()
        self.browser.implicitly_wait(120)
        try:
            rej_cookies = self.browser.find_element(By.XPATH, "/html/body/ytd-app/ytd-consent-bump-v2-lightbox/tp-yt-paper-dialog/div[4]/div[2]/div[6]/div[1]/ytd-button-renderer[1]/yt-button-shape/button/yt-touch-feedback-shape/div/div[2]").click()
        except:
            print("Nu avem butonul Reject ALL")

        try:
            video_rand = self.browser.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-browse/ytd-two-column-browse-results-renderer/div[1]/ytd-rich-grid-renderer/div[6]/ytd-rich-grid-row[1]/div/ytd-rich-item-renderer[1]/div/ytd-rich-grid-media/div[1]/ytd-thumbnail/a/yt-image/img").click()
        except:
            print("Nu ajunge pana in punctul de play")

        try:
            skipButton = self.browser.find_element(By.XPATH, "/html/body/ytd-app/div[1]/ytd-page-manager/ytd-watch-flexy/div[5]/div[1]/div/div[1]/div[2]/div/div/ytd-player/div/div/div[18]/div/div[3]/div/div[2]/span/button/div")
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

    def record_video(self):

        SCREEN_SIZE = tuple(pyautogui.size())
        fourcc = cv2.VideoWriter_fourcc(*"XVID")
        fps = 12.0
        # create the video write object
        out = cv2.VideoWriter("output.avi", fourcc, fps, (SCREEN_SIZE))
        # the time you want to record in seconds
        record_seconds = 10
        for i in range(int(record_seconds * fps)):
            # make a screenshot
            img = pyautogui.screenshot()
            # convert these pixels to a proper numpy array to work with OpenCV
            frame = np.array(img)
            # convert colors from BGR to RGB
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # write the frame
            out.write(frame)
            # if the user clicks q, it exits
            if cv2.waitKey(1) == ord("q"):
                break
        # make sure everything is closed when exited
        ### cv2.destroyAllWindows()
        out.release()


if conexiune():


    site = YouTube()
    site.openYouTube()

    input("Apasa ENTER pentru a inchide pagina")

else:
    print("Nu se conecteaza la Internet")