import time

import pyaudio
import wave
import cv2
import pyautogui
import numpy as np
import concurrent.futures


def screen_record():
    # display screen resolution, get it from your OS settings
    SCREEN_SIZE = (1920, 1080)
    # define the codec
    fourcc = cv2.VideoWriter_fourcc(*"XVID")
    # create the video write object
    out = cv2.VideoWriter("output.avi", fourcc, 18.0, SCREEN_SIZE)
    images = []
    for i in range(400):
        print(i)
        # make a screenshot
        img = pyautogui.screenshot()
        images.append(img)
        # cv2.waitKey()
        # # convert these pixels to a proper numpy array to work with OpenCV
        # frame = np.array(img)
        # # convert colors from BGR to RGB
        # frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # # write the frame
        # out.write(frame)
        # # cv2.waitKey(50)
        # # show the frame
        # # cv2.imshow("screenshot", frame)
        # # if the user clicks q, it exits
        # if cv2.waitKey(1) == ord("q"):
        #     break

    for img in images:
        frame = cv2.cvtColor(np.array(img), cv2.COLOR_BGR2RGB)
        out.write(frame)

    # make sure everything is closed when exited
    cv2.destroyAllWindows()
    out.release()


def audio_record():
    # the file name output you want to record into
    filename = "recorded.wav"
    # set the chunk size of 1024 samples
    chunk = 1024
    # sample format
    FORMAT = pyaudio.paInt16
    # mono, change to 2 if you want stereo
    channels = 1
    # 44100 samples per second
    sample_rate = 44100
    record_seconds = 20
    # initialize PyAudio object
    p = pyaudio.PyAudio()
    # open stream object as input & output
    dev_index = 0
    for i in range(p.get_device_count()):
        dev = p.get_device_info_by_index(i)
        if dev['name'] == 'Stereo Mix (Realtek(R) Audio)' and dev['hostApi'] == 0:
            dev_index = dev['index']
    stream = p.open(format=FORMAT,
                    channels=channels,
                    rate=sample_rate,
                    input=True,
                    output=True,
                    input_device_index=dev_index,
                    frames_per_buffer=chunk)
    frames = []
    print("Recording...")
    for i in range(int(44100 / chunk * record_seconds)):
        data = stream.read(chunk)
        # if you want to hear your voice while recording
        # data = stream.write(chunk)
        frames.append(data)
    print("Finished recording.")
    print("Pana aici")
    # stop and close stream
    stream.stop_stream()
    stream.close()
    # terminate pyaudio object
    p.terminate()
    # save audio file
    # open the file in 'write bytes' mode
    wf = wave.open(filename, "wb")
    # set the channels
    wf.setnchannels(channels)
    # set the sample format
    wf.setsampwidth(p.get_sample_size(FORMAT))
    # set the sample rate
    wf.setframerate(sample_rate)
    # write the frames as bytes
    wf.writeframes(b"".join(frames))
    # close the file
    wf.close()


def audi_video_recording():
    with concurrent.futures.ThreadPoolExecutor() as executor:
        t1 = executor.submit(screen_record)
        t2 = executor.submit(audio_record)
