#!/usr/bin/env python2
from psychopy import visual, core, event

def showInstruction(instructionFilename):
    #create a window to draw in
    myWin = visual.Window((800.0,800.0),allowGUI=False,winType='pyglet',
                monitor='testMonitor', units ='deg', screen=0)
    myWin.setRecordFrameIntervals()
    #choose some fonts. If a list is provided, the first font found will be used.
    fancy = ['Monotype Corsiva', 'Palace Script MT', 'Edwardian Script ITC']

    infile =open(instructionFilename,'r')
    instructionText =infile.read()
    print instructionText
    infile.close()

    #INITIALISE SOME STIMULI
    instruction = visual.TextStim(myWin, color='#FFFFFF',
                            text =instructionText,
                            units='norm', height=0.1,
                            pos=[0, 0.6], alignHoriz='center',alignVert='top',
                            font=fancy)


    instruction.draw()
        
    myWin.flip()

    #pause, so you get a chance to see it!
    core.wait(5.0)


