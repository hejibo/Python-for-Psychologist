#!/usr/bin/env python2
from psychopy import visual, core, event

#create a window to draw in
myWin = visual.Window((800.0,800.0),allowGUI=False,winType='pyglet',
            monitor='testMonitor', units ='deg', screen=0)
myWin.setRecordFrameIntervals()
#choose some fonts. If a list is provided, the first font found will be used.
fancy = ['Monotype Corsiva', 'Palace Script MT', 'Edwardian Script ITC']

#INITIALISE SOME STIMULI
psychopyTxt = visual.TextStim(myWin, color='#FFFFFF',
                         text = u"unicode (eg \xe6 \u040A \u03A3)",#you can find the unicode character value from MS Word 'insert symbol'
                        units='norm', height=0.1,
                        pos=[0.8, 0.0], alignHoriz='right',alignVert='top',
                        font=fancy)


psychopyTxt.draw()
    
myWin.flip()

#pause, so you get a chance to see it!
core.wait(5.0)


