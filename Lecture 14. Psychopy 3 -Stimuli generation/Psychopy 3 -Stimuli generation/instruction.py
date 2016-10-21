#!/usr/bin/env python2
from psychopy import visual, core, event

#create a window to draw in
myWin = visual.Window((800.0,800.0),allowGUI=False,winType='pyglet',
            monitor='testMonitor', units ='deg', screen=0)
myWin.setRecordFrameIntervals()
#choose some fonts. If a list is provided, the first font found will be used.
fancy = ['Monotype Corsiva', 'Palace Script MT', 'Edwardian Script ITC']

#INITIALISE SOME STIMULI
instruction = visual.TextStim(myWin, color='#FFFFFF',
                        text = u'''         Instruction
                        
This is an experiment instruction. You need to do the following stuff.
1. Fixate at the dot.
2. press the 'Y' or 'N' key 
Press any key to continue''',
                        units='norm', height=0.1,
                        pos=[0, 0.6], alignHoriz='center',alignVert='top',
                        font=fancy)


instruction.draw()
    
myWin.flip()

#pause, so you get a chance to see it!
core.wait(5.0)


