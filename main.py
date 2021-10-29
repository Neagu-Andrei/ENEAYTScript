import concurrent.futures
import errno
from AudioRecorder import AudioRecorder
from ScreenRecorder import ScreenRecorder
from Driver import DriverController
from scipy.fft import *
from scipy.io import wavfile
import numpy as np
from pydub import AudioSegment
from math import log10
import logging
from threading import Thread
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


def sound_intensity(file):
    sound = AudioSegment.from_file(file)  # get the file using pydub
    db = 20 * log10(sound.rms)
    return db


def youtube_handler(driver):
    logger.info("Incepe executarea deschiderea yt")
    driver.open_yt()
    driver.agree_cookies()
    driver.search_for_video("music")
    driver.skip_ad()
    logger.info("S-a executat deschiderea yt")


# https://audiology-web.s3.amazonaws.com/migrated/NoiseChart_Poster-%208.5x11.pdf_5399b289427535.32730330.pdf
if __name__ == '__main__':
    DIR = "resources/"
    audioFile = DIR + "audio_recording.wav"
    screenFile = DIR + "screen_recording.avi"
    intensityFile = DIR + "intensity_record.csv"
    seconds = 120

    driverContrl = DriverController(seconds)
    audioRec = AudioRecorder(audioFile, seconds)
    screenRec = ScreenRecorder(screenFile, seconds)
    driverContrl.run()

    t1 = Thread(target=driverContrl.time_connected)
    t2 = Thread(target=screenRec.update)
    t3 = Thread(target=audioRec.record)
    t4 = Thread(target=audioRec.save_to_file)
    t5 = Thread(target=screenRec.write)
    t1.start()
    t2.start()
    t3.start()

    t1.join()
    t2.join()
    t3.join()

    driverContrl.stop()

    t4.start()
    t5.start()

    t4.join()
    t5.join()

    audioRec.write_intensity(intensityFile)
    logger.info("Program ended successfully.\n ")


