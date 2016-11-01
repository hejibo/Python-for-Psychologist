#!/usr/bin/env python2
from psychopy import visual, core, event

#create a window to draw in
myWin = visual.Window((800.0,800.0),allowGUI=False,winType='pyglet',
            monitor='testMonitor', units ='deg', screen=0)
myWin.setRecordFrameIntervals()
#choose some fonts. If a list is provided, the first font found will be used.
fancy = ['Monotype Corsiva', 'Palace Script MT', 'Edwardian Script ITC']

#INITIALISE SOME STIMULI
THoriLine = visual.Line(myWin, start=(0, 0), end=(2.8, 0))
    
# the first slot is the same for vertical line
TVertiLine = visual.Line(myWin, start=(0, 0), end=(0, 1.1))
THoriLine.draw()
TVertiLine.draw()
    
myWin.flip()

#pause, so you get a chance to see it!
core.wait(5.0)


