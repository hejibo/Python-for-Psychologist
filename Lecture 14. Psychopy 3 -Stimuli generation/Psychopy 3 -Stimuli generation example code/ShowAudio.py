#!/usr/bin/env python2
import sys
from psychopy import logging, prefs
logging.console.setLevel(logging.DEBUG)#get messages about the sound lib as it loads

from psychopy import sound,core, visual
if prefs.general['audioLib'][0] == 'pyo':
    #if pyo is the first lib in the list of preferred libs then we could use small buffer
    #pygame sound is very bad with a small buffer though
    sound.init(48000,buffer=128)
print 'Using %s(with %s) for sounds' %(sound.audioLib, sound.audioDriver)
if sys.platform=='win32':
    tada = sound.Sound('tada.wav')
    tada.play()
    core.wait(2)
else:
    tada = sound.Sound('tada.wav')
    tada.play()
    core.wait(2)
print 'done'
core.quit()
