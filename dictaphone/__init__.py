#!/usr/bin/env python

import sys
import os
import time
import shutil
import thread
import pyaudio
import wave
import audioop

DEFAULT_CHANNELS = 2
DEFAULT_RATE = 44100
DEFAULT_INPUT_DEVICE_INDEX = None

CHUNK = 1024
FORMAT = pyaudio.paInt16
#THRESHOLD_MULTIPLIER = 6
#THRESHOLD_TIME = 3

sample_size = pyaudio.PyAudio().get_sample_size(FORMAT)

def play(wave_filename):
    """Plays a WAV file"""
    wf = wave.open(wave_filename, 'rb')

    p = pyaudio.PyAudio()

    def callback(in_data, frame_count, time_info, status):
        data = wf.readframes(frame_count)
        return (data, pyaudio.paContinue)

    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
                    channels=wf.getnchannels(),
                    rate=wf.getframerate(),
                    output=True,
                    stream_callback=callback)

    stream.start_stream()

    while stream.is_active():
        time.sleep(0.1)

    stream.stop_stream()
    stream.close()
    wf.close()
    p.terminate()


def record(channels, rate, input_device_index, input_thread):
    """Records audio until the new thread causes a break"""
    audio = pyaudio.PyAudio()
    stream = audio.open(format=FORMAT,
                        channels=channels,
                        rate=rate,
                        input_device_index=input_device_index,
                        input=True,
                        frames_per_buffer=CHUNK)

    frames = []

    L = []
    thread.start_new_thread(input_thread, (L,))
    while True:
        if L:
            break
        data = stream.read(CHUNK)
        frames.append(data)

    stream.stop_stream()    # Stop Audio Recording
    stream.close()          # Close Audio Recording
    audio.terminate()       # Audio System Close
    return frames


def get_all_data(dir_scratch, counter):
    data = []
    for i in range(counter):
        w = wave.open(os.path.join(dir_scratch, str(i) + '.wav'), 'rb')
        data.append( [w.getparams(), w.readframes(w.getnframes())] )
        w.close()
    return data


def save_as_wave(file_out, frames, channels, rate):
    """Saves the given frames as WAV"""
    wf = wave.open(file_out, 'wb')
    wf.setnchannels(channels)
    wf.setsampwidth(sample_size)
    wf.setframerate(rate)
    wf.writeframes(b''.join(frames))
    wf.close()


def save_data_as_wave(file_out, data, counter):
    """Saves the given frames as WAV"""
    wf = wave.open(file_out, 'wb')
    wf.setparams(data[0][0])
    for i in range(counter):
        wf.writeframes(data[i][1])
    wf.close()
