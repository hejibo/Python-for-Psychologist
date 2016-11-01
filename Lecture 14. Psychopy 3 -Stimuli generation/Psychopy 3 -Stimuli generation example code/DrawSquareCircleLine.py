#!/usr/bin/env python2
from psychopy import visual, core, event

#create a window to draw in
myWin = visual.Window((800.0,800.0),allowGUI=False,winType='pyglet',
            monitor='testMonitor', units ='deg', screen=0)
myWin.setRecordFrameIntervals()
#choose some fonts. If a list is provided, the first font found will be used.
fancy = ['Monotype Corsiva', 'Palace Script MT', 'Edwardian Script ITC']

#INITIALISE SOME STIMULI
circle = visual.Circle(myWin, radius=2, edges=32)
circle.pos=(0,0)
circle.draw()

square = visual.Rect(myWin,width=1,height=1)
square.pos= (4,4)
square.draw()


TVertiLine = visual.Line(myWin, start=(-3, -3), end=(-3, 1))
TVertiLine.draw()

myWin.flip()
#pause, so you get a chance to see it!
core.wait(5.0)

