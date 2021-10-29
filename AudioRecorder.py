import csv
import errno
import wave
from math import log10

import pyaudio
import logging

from pydub import AudioSegment

logger = logging.getLogger(__name__)


class AudioRecorder:
    chunk = 1024    # number of frames in the buffer
    FORMAT = pyaudio.paInt16
    channels = 1    # mono audio stream
    sampleRate = 44100  # number of frames per second

    def __init__(self, filename, seconds):
        self.filename = filename
        self.seconds = seconds
        self.frames = []
        self.p = pyaudio.PyAudio()
        # If Stereo Mix is not found dev_index = None
        # Switches to the default input device
        dev_index = self.get_stereoMix()
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.channels,
                                  rate=self.sampleRate,
                                  input=True,
                                  output=True,
                                  input_device_index=dev_index,
                                  frames_per_buffer=self.chunk)

    # Function to get Stereo Mix to get the audio from our computer
    def get_stereoMix(self):
        for i in range(self.p.get_device_count()):
            dev = self.p.get_device_info_by_index(i)
            if dev['name'] == 'Stereo Mix (Realtek(R) Audio)' and dev['hostApi'] == 0:
                return dev['index']

    def record(self):
        logger.info("Start audio recording...")
        for i in range(int(44100 / self.chunk * self.seconds)):
            data = self.stream.read(self.chunk)
            # if you want to hear your voice while recording
            # data = stream.write(chunk)
            self.frames.append(data)
        logger.info("Finished audio recording")
        self.stream.start_stream()
        self.stream.close()
        self.p.terminate()

    def save_to_file(self):
        logger.info("Started compiling audio recorder")
        wf = wave.open(self.filename, "wb")
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.sampleRate)
        try:
            wf.writeframes(b"".join(self.frames))
            logger.info("Finished compilig audio recording")
        except OSError as e:
            if e.errno == errno.ENOSPC:
                logger.error("Couldn't compile the audio file. Disk space is full")
                raise
            else:
                logger.error(e)
                raise
        finally:
            wf.close()

    # RMS (Root Mean Squared) = mathematic calculation to measure the avreage amplitude
    # 20*log10(amplitude) = vertical scale in dB
    def sound_intensity(self):
        sound = AudioSegment.from_file(self.filename)  # get the file using pydub
        db = 20 * log10(sound.rms)
        return db

    def write_intensity(self, intensityFile):
        logger.info("Started writing intensity")
        with open(intensityFile, 'a', newline='') as csv_file:
            csv_writer = csv.writer(csv_file)
            try:
                csv_writer.writerow([self.filename, self.sound_intensity()])
                logger.info("Wrote intensity of the sound in file")
            except OSError as e:
                if e.errno == errno.ENOSPC:
                    logger.error("Couldn't write intensity in the file. Disk space is full")
                    raise
                else:
                    logger.error(e)
                    raise
