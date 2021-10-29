import errno
import wave
import pyaudio
import logging

logger = logging.getLogger(__name__)


class AudioRecorder:
    chunk = 1024    # number of frames in the buffer
    FORMAT = pyaudio.paInt16
    channels = 1    # mono audio stream
    sampleRate = 44100  # number of frames per second
    seconds = 120

    def __init__(self, filename):
        self.fileName = filename
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
        try:
            logger.info("Started compiling audio recorder")
            wf = wave.open(self.fileName, "wb")
            wf.setnchannels(self.channels)
            wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
            wf.setframerate(self.sampleRate)
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
