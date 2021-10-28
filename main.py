import concurrent.futures
import time
from AudioRecorder import AudioRecorder
from ScreenRecorder import ScreenRecorder
from Driver import DriverController
from scipy.fft import *
from scipy.io import wavfile
import numpy as np
from pydub import AudioSegment
from math import log10
import logging
import csv

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
    logger.info("Incepe executarea deschiderea yt")
    driver.open_yt()
    driver.agree_cookies()
    driver.search_for_video("music")
    driver.skip_ad()
    logger.info("S-a executat deschiderea yt")


if __name__ == '__main__':
    DIR = "resources/"
    audioFile = DIR + "audio_recording.wav"
    screenFile = DIR + "screen_recording.avi"
    driverContrl = DriverController()
    audioRec = AudioRecorder(audioFile)
    screenRec = ScreenRecorder(screenFile)
    youtube_api(driverContrl)
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(driverContrl.time_connected, 125)
        executor.submit(audioRec.record)
        executor.submit(screenRec.update)
        executor.shutdown(wait=True)
    driverContrl.stop()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.submit(audioRec.save_to_file)
        executor.submit(screenRec.write)
    with open(DIR + 'intensity_record.csv', 'a', newline='') as csv_file:
        fieldnames = ['Audio File', 'Intensity']
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow([audioFile, sound_intensity(audioFile)])
    logger.info("Program ended successfully.\n ")


