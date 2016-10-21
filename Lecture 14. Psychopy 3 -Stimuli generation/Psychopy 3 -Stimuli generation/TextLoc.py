#!/usr/bin/env python2
from psychopy import visual, core, event

#create a window to draw in
myWin = visual.Window((600.0,600.0),allowGUI=False,winType='pyglet',
            monitor='testMonitor', units ='deg', screen=0)
myWin.setRecordFrameIntervals()
#choose some fonts. If a list is provided, the first font found will be used.
fancy = ['Monotype Corsiva', 'Palace Script MT', 'Edwardian Script ITC']

#INITIALISE SOME STIMULI
topleft = visual.TextStim(myWin, color=(255,0,0),
                        text = u"top left",
                        units='norm', height=0.1,
                        pos=[-0.6, 0.9], alignHoriz='right',alignVert='top',
                        font=fancy)

topright = visual.TextStim(myWin, color=(0,255,0),
                        text = u"top right",
                        units='norm', height=0.1,
                        pos=[0.9, 0.9], alignHoriz='right',alignVert='top',
                        font=fancy)


bottomleft = visual.TextStim(myWin, color=(0,0,255),
                        text = u"bottom left",
                        units='norm', height=0.1,
                        pos=[-0.5, -0.6], alignHoriz='right',alignVert='top',
                        font=fancy)


bottomright = visual.TextStim(myWin, color='#FFFFFF',
                        text = u"bottom right",
                        units='norm', height=0.1,
                        pos=[0.6, -0.6], alignHoriz='right',alignVert='top',
                        font=fancy)

center = visual.TextStim(myWin, color='#FFFFFF',
                        text = u"center",
                        units='norm', height=0.1,
                        pos=[0, 0], alignHoriz='right',alignVert='top',
                        font=fancy)

topleft.draw()
topright.draw()
bottomleft.draw()
bottomright.draw()
center.draw()

myWin.flip()

#pause, so you get a chance to see it!
core.wait(5.0)


