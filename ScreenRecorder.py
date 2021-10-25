import cv2
import pyautogui
import numpy as np


class ScreenRecorder:
    screenSize = (1920, 1080)
    filename = "screen_recording.avi"
    fps = 18.0
    seconds = 20

    def __init__(self):
        self.fourcc = cv2.VideoWriter_fourcc(*"XVID")
        self.out = cv2.VideoWriter(self.filename, self.fourcc, self.fps, self.screenSize)

    def record(self):
        for i in range(self.seconds):
            img = pyautogui.screenshot()
            frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
            self.out.write(frame)

    def stop(self):
        self.out.release()

