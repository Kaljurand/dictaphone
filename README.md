Dictaphone
==========

Dictaphone is a Python commandline program that lets you record audio
by pressing a button to start/stop recording as many times as you like.
At the end of each session, the audio is saved to a WAV file.
When Ctrl-D is pressed all previously saved files are combined into a single WAV file.

Usage example (press `<Enter>`):

    dictaphone_ui.py -c 1 -r 16000 --playback --ui-in=kb


Usage example (press a GPIO button):

    dictaphone_ui.py -c 1 -r 16000 --playback --ui-in=gpiobtn --ui-out=gpioled,beep


Dependencies
------------

PortAudio and PyAudio are required.

Install:

    pip install pyaudio

Version history
---------------

### v0.0.1

Based on <https://github.com/shbhrsaha/dictaphone> with the following changes:

- more commandline options
- earcons converted to mono
- some refactoring


Useful docs
-----------

- <http://wiki.audacityteam.org/wiki/USB_mic_on_Linux>


TODO
----

- add an arg for possible input devices: GPIO/button, ENTER, VAD
- add an arg for possible output feedbacks: GPIO/led, beep
- compress to flac and upload to dropbox, drive, soundcloud, ...
- transcribe
- query over recordings, e.g. "timeframe:10-1234 speaker:id0 phrase:'elas metsas mutionu'"
