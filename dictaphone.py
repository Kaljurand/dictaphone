#!/usr/bin/env python

import argparse
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

audio = pyaudio.PyAudio()

def input_thread(L):
    raw_input("Recording... (press <Enter> to stop)")
    L.append(None)

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


def record(args):
    """Records audio until key pressed"""
    stream = audio.open(format=FORMAT,
                        channels=args.channels,
                        rate=args.rate,
                        input_device_index=args.input_device_index,
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
    return frames


def save_as_wave(args, frames, counter=0):
    """Saves the given frames as WAV"""
    wf = wave.open(os.path.join(args.dir_scratch, str(counter) + '.wav'), 'wb')
    wf.setnchannels(args.channels)
    wf.setsampwidth(audio.get_sample_size(FORMAT))
    wf.setframerate(args.rate)
    wf.writeframes(b''.join(frames))
    wf.close()


def get_args():
    p = argparse.ArgumentParser(description='Stop-go recording of audio in terminal')
    p.add_argument('--dir-scratch', type=str, action='store', dest='dir_scratch', default='scratch')
    p.add_argument('-o', '--out', type=str, action='store', dest='file_out', required=True)
    p.add_argument('-c', '--channels', type=int, action='store', dest='channels', default=DEFAULT_CHANNELS)
    p.add_argument('-r', '--rate', type=int, action='store', dest='rate', default=DEFAULT_RATE)
    p.add_argument('--input-device-index', type=int, action='store', dest='input_device_index', default=DEFAULT_INPUT_DEVICE_INDEX)
    p.add_argument('--playback', action='store_true', help='playback the complete recording')
    p.add_argument('--nobackup', action='store_true', help='delete scratch directory when finished')
    p.add_argument('-v', '--version', action='version', version='%(prog)s v0.0.2')
    return p.parse_args()


if __name__ == "__main__":
    args = get_args()

    if not os.path.exists(args.dir_scratch):
        os.makedirs(args.dir_scratch)

    counter = 0
    try:
        while True:
            enter = raw_input("Waiting... (press <Enter> to start recording or Ctrl-D to finish)")
            play("beep_hi.wav")
            frames = record(args)
            play("beep_lo.wav")
            print 'Stopped recording, saving as file #{0} ...'.format(counter)
            save_as_wave(args, frames, counter)
            counter += 1
    except EOFError:
        print ''
    except KeyboardInterrupt:
        print ''

    data = []
    for i in range(counter):
        w = wave.open(os.path.join(args.dir_scratch, str(i) + '.wav'), 'rb')
        data.append( [w.getparams(), w.readframes(w.getnframes())] )
        w.close()

    if len(data):
        output = wave.open(args.file_out, 'wb')
        output.setparams(data[0][0])
        for i in range(counter):
            output.writeframes(data[i][1])
        output.close()
        if args.playback:
            play(args.file_out)

    if args.nobackup:
        shutil.rmtree(args.dir_scratch)
