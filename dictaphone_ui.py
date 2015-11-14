#!/usr/bin/env python

from dictaphone import DEFAULT_CHANNELS, DEFAULT_RATE, DEFAULT_INPUT_DEVICE_INDEX, play, record, save_as_wave, save_data_as_wave, get_all_data
import argparse
import os

# TODO:  put into classes that implement an abstract class
LedPin = 12
BtnPin = 7

led_status = 1

def wait_for_start():
    enter = raw_input("Waiting... (press <Enter> to start recording or Ctrl-D to finish)")

def wait_for_stop(lst):
    raw_input("Recording... (press <Enter> to stop)")
    lst.append(None)

def swLed(ev=None):
    global led_status
    led_status = not led_status
    GPIO.output(LedPin, led_status)  # switch led status(on-->off; off-->on)
    if led_status == 1:
        print 'led off...'
    else:
        print '...led on'

def wait_for_start_gpio():
    current_led_status = led_status
    while current_led_status == led_status:
        pass

def wait_for_stop_gpio(lst):
    current_led_status = led_status
    while current_led_status == led_status:
        pass
    lst.append(None)

def setup():
    pass

def destroy():
    pass

def setup_gpio():
    GPIO.setmode(GPIO.BOARD)       # Numbers GPIOs by physical location
    GPIO.setup(LedPin, GPIO.OUT)   # Set LedPin's mode is output
    GPIO.setup(BtnPin, GPIO.IN, pull_up_down=GPIO.PUD_UP)    # Set BtnPin's mode is input, and pull up to high level(3.3V)
    GPIO.output(LedPin, GPIO.HIGH) # Set LedPin high(+3.3V) to off led
    GPIO.add_event_detect(BtnPin, GPIO.FALLING, callback=swLed) # wait for falling

def destroy_gpio():
    GPIO.output(LedPin, GPIO.HIGH)     # led off
    GPIO.cleanup()                     # Release resource

def get_args():
    p = argparse.ArgumentParser(description='Stop-go recording of audio')
    p.add_argument('--ui-type', type=str, action='store', dest='ui_type', default='kb', help='UI type, one of {kb, gpio}')
    p.add_argument('--dir-scratch', type=str, action='store', dest='dir_scratch', default='scratch')
    p.add_argument('-o', '--out', type=str, action='store', dest='file_out', required=True)
    p.add_argument('-c', '--channels', type=int, action='store', dest='channels', default=DEFAULT_CHANNELS)
    p.add_argument('-r', '--rate', type=int, action='store', dest='rate', default=DEFAULT_RATE)
    p.add_argument('--input-device-index', type=int, action='store', dest='input_device_index', default=DEFAULT_INPUT_DEVICE_INDEX)
    p.add_argument('--playback', action='store_true', help='playback the complete recording')
    p.add_argument('--nobackup', action='store_true', help='delete scratch directory when finished')
    p.add_argument('-v', '--version', action='version', version='%(prog)s v0.0.3')
    return p.parse_args()

if __name__ == "__main__":
    args = get_args()

    if args.ui_type == 'gpio':
        import RPi.GPIO as GPIO

        wait_for_start = wait_for_start_gpio
        wait_for_stop = wait_for_stop_gpio
        setup = setup_gpio
        destroy = destroy_gpio

    if not os.path.exists(args.dir_scratch):
        os.makedirs(args.dir_scratch)

    setup()

    counter = 0
    try:
        while True:
            wait_for_start()
            play("beep_hi.wav")
            frames = record(args.channels, args.rate, args.input_device_index, wait_for_stop)
            play("beep_lo.wav")
            print 'Stopped recording, saving as file #{0} ...'.format(counter)
            file_out = os.path.join(args.dir_scratch, str(counter) + '.wav')
            save_as_wave(file_out, frames, args.channels, args.rate)
            counter += 1
    except EOFError:
        destroy()
        print ''
    except KeyboardInterrupt:
        destroy()
        print ''

    data = get_all_data(args.dir_scratch, counter)

    if data:
        save_data_as_wave(args.file_out, data, counter)
        if args.playback:
            play(args.file_out)

    if args.nobackup:
        shutil.rmtree(args.dir_scratch)
