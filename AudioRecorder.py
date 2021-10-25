import wave
import pyaudio


class AudioRecorder:
    fileName = "recorded.wav"
    chunk = 1024
    FORMAT = pyaudio.paInt16
    channels = 1
    sampleRate = 44100
    seconds = 20

    def __init__(self):
        self.frames = None
        self.p = pyaudio.PyAudio()
        dev_index = self.get_stereoMix()
        self.stream = self.p.open(format=self.FORMAT,
                                  channels=self.channels,
                                  rate=self.sampleRate,
                                  input=True,
                                  output=True,
                                  input_device_index=dev_index,
                                  frames_per_buffer=self.chunk)

    def get_stereoMix(self):
        for i in range(self.p.get_device_count()):
            dev = self.p.get_device_info_by_index(i)
            if dev['name'] == 'Stereo Mix (Realtek(R) Audio)' and dev['hostApi'] == 0:
                return dev['index']

    def record(self):
        print("Recording...")
        for i in range(int(44100 / self.chunk * self.seconds)):
            data = self.stream.read(self.chunk)
            # if you want to hear your voice while recording
            # data = stream.write(chunk)
            self.frames.append(data)
        print("Finished recording")
        self.stream.start_stream()
        self.stream.close()
        self.p.terminate()

    def save_to_file(self):
        wf = wave.open(self.fileName, "wb")
        wf.setnchannels(self.channels)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.sampleRate)
        wf.writeframes(b"".join(self.frames))
        wf.close()
