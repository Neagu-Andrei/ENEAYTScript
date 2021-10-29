import errno

import cv2
import pyautogui
import numpy as np
from queue import Queue
import logging

logger = logging.getLogger(__name__)


class ScreenRecorder:
    screenSize = (1920, 1080)
    filename = "screen_recording.avi"
    fps = 11
    seconds = 120

    def __init__(self, filename):
        self.filename = filename    # name of the file
        self.fourcc = cv2.VideoWriter_fourcc(*"XVID")   # video codec
        self.out = cv2.VideoWriter(self.filename, self.fourcc, self.fps, self.screenSize)
        self.images = Queue()

    # Update function that takes a screenshot and adds it to the Queue
    def update(self):
        logger.info("Start screen recording...")
        lent = int(self.fps * self.seconds)
        for _ in range(lent):
            img = pyautogui.screenshot()
            self.images.put(img)
        logger.info("Finished screen recording")

    # Compiles the screen recording
    def write(self):
        try:
            logger.info("Started compiling screen recording")
            while self.images.qsize() > 0:
                # converts screenshot to a numpy array and converts color spaces from BGR to RGB
                frame = cv2.cvtColor(np.array(self.images.get()), cv2.COLOR_BGR2RGB)
                self.out.write(frame)
            logger.info("Finished compilig screen recording")
        except OSError as e:
            if e.errno == errno.ENOSPC:
                logger.error("Couldn't compile screen recording file. Disk space is fulll.")
                raise
            else:
                logger.error(e)
                raise
        finally:
            self.out.release()


