import concurrent.futures
import subprocess
import time
from AudioRecorder import AudioRecorder
from ScreenRecorder import ScreenRecorder
from Driver import DriverController
from scipy.fft import *
from scipy.io import wavfile
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment
from math import log10
import logging

logging.basicConfig(filename='log_file.log', level=logging.INFO,
                    format='%(levelname)s:%(name)s at %(asctime)s: %(message)s')

logger = logging.getLogger(__name__)


# def freq(file, startTime, endTime):
#     # Open the file and convert to mono
#     sr, data = wavfile.read(file)
#     if data.ndim > 1:
#         data = data[:, 0]
#     else:
#         pass
#
#     # Return a slice of the data from start_time to end_time
#     dataToRead = data[int(startTime * sr / 1000): int(endTime * sr / 1000) + 1]
#     # Fourier Transform
#     N = len(dataToRead)
#     yf = rfft(dataToRead)
#     xf = rfftfreq(N, 1 / sr)
#
#     # Uncomment these to see the frequency spectrum as a plot
#     plt.plot(xf, np.abs(yf))
#     plt.show()
#     print(N)
#
#     # Get the most dominant frequency and return it
#     idx = np.argmax(np.abs(yf))
#     freq = xf[idx]
#     return freq, idx


# RMS (Root Mean Squared) = mathematic calculation to measure the avreage amplitude
# 20*log10(amplitude) = vertical scale in dB
def sound_intensity(file):
    sound = AudioSegment.from_file(file)  # get the file using pydub
    db = 20 * log10(sound.rms)
    return db


def youtube_api(driver):
    # print("Incepe executarea deschiderea yt")
    # driver.open_yt()
    # driver.agree_cookies()
    driver.search_for_video("hasanabi")
    driver.skip_ad()
    print("S-a executat deschiderea yt")


# def combine_audio(vidname, audname, outname):
#     cmd = f"ffmpeg -i {vidname} -i {audname} -c:v copy -c:a aac {outname}"
#     subprocess.call(cmd, shell=True)
#     print("Mixing Done")


if __name__ == '__main__':
    # driverContrl = DriverController()
    # audioRec = AudioRecorder()
    # screenRec = ScreenRecorder()
    # driverContrl.open_yt()
    # driverContrl.agree_cookies()
    # youtube_api(driverContrl)
    # with concurrent.futures.ThreadPoolExecutor() as executor:
    #     # t1 = executor.submit(youtube_api, driverContrl)
    #     t2 = executor.submit(audioRec.record)
    #     t3 = executor.submit(screenRec.update)
    # audioRec.save_to_file()
    # screenRec.write()
    # combine_audio("screen_recording.avi", "recorded.wav", "yt_clip.avi")
    print(sound_intensity("recorded.wav"))
