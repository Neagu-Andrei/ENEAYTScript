import concurrent.futures
import pyaudio

from audio_video_recording import audi_video_recording
from Driver import DriverController
import cv2
import numpy as np
import pyautogui


def youtube_api(driver):
    print("Incepe executarea deschiderea yt")
    driver.open_yt()
    driver.agree_cookies()
    driver.search_for_video("jador aseara dansez singura")
    driver.skip_ad()
    print("S-a executat deschiderea yt")


if __name__ == '__main__':
    driver = DriverController()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        t1 = executor.submit(youtube_api, driver)
        t2 = executor.submit(audi_video_recording)

    # audi_video_recording()

        # t1.result()
        # t2.result()
    # t1 = threading.Thread(target=youtube_api)
    # # t2 = threading.Thread(target=screen_record)
    #
    # t1.start()
    # # t2.start()
    #
    # t1.join()
    # # t2.join()
