Dictaphone
==========

Dictaphone is a Python commandline program that lets you record audio
by pressing \<Enter\> to start/stop recording as many times as you like.
At the end of each session, the audio is saved to a WAV file.
When Ctrl-D is pressed all previously saved files are combined into a single WAV file.

Usage example:

    dictaphone.py -otest.wav -c 1 -r 16000


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
