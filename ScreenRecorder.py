import cv2
import pyautogui
import numpy as np
from queue import Queue
from threading import Thread
import time
import logging

logger = logging.getLogger(__name__)


class ScreenRecorder:
    screenSize = (1920, 1080)
    filename = "screen_recording.avi"
    fps = 11
    seconds = 120

    def __init__(self):
        self.fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.out = cv2.VideoWriter(self.filename, self.fourcc, self.fps, self.screenSize)
        self.images = Queue()

    def update(self):
        logger.info("Start screen recording...")
        lent = int(self.fps * self.seconds)
        # start_time = time.time()
        for _ in range(lent):
            img = pyautogui.screenshot()
            self.images.put(img)
        logger.info("Finished screen recording")
        # print("Finished screen recording at ", time.time()- start_time, " seconds")

    def write(self):
        logger.info("Started compiling screen recording")
        while self.images.qsize() > 0:
            frame = cv2.cvtColor(np.array(self.images.get()), cv2.COLOR_BGR2RGB)
            self.out.write(frame)
        logger.info("Finished compilig screen recording")
        self.out.release()



