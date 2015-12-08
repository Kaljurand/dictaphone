Dictaphone
==========

Dictaphone is a Python commandline program that lets you record audio
by pressing a button to start/stop recording as many times as you like.
At the end of each session, the audio is saved to a WAV file.
When Ctrl-D is pressed all previously saved files are combined into a single WAV file
and optionally transcribed.

Usage example (press `<Enter>`):

    dictaphone_ui.py -c 1 -r 16000 --playback --ui-in=kb --transcribe


Usage example (press a GPIO button):

    dictaphone_ui.py -c 1 -r 16000 --playback --ui-in=gpiobtn --ui-out=gpioled,beep


Dependencies
------------

PortAudio and PyAudio are required.

Install:

    pip install pyaudio

Version history
---------------

### v0.1.0

- recordings are now stored in directories named by timestamps
- optional Estonian transcription using <https://github.com/alumae/kaldi-gstreamer-server>

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
- show (preliminary) transcription during recording
- do final transcription with <https://github.com/alumae/kaldi-offline-transcriber>
- query over recordings, e.g. "timeframe:10-1234 speaker:id0 phrase:'elas metsas mutionu'"
