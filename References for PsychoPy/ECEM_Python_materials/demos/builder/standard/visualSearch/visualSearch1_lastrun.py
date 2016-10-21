#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This experiment was created using PsychoPy2 Experiment Builder (v1.78.00), Mon  5 Aug 18:03:33 2013
If you publish work using this script please cite the relevant PsychoPy publications
  Peirce, JW (2007) PsychoPy - Psychophysics software in Python. Journal of Neuroscience Methods, 162(1-2), 8-13.
  Peirce, JW (2009) Generating stimuli for neuroscience using PsychoPy. Frontiers in Neuroinformatics, 2:10. doi: 10.3389/neuro.11.010.2008
"""

from __future__ import division  # so that 1/3=0.333 instead of 1/3=0
from psychopy import visual, core, data, event, logging, sound, gui
from psychopy.constants import *  # things like STARTED, FINISHED
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import sin, cos, tan, log, log10, pi, average, sqrt, std, deg2rad, rad2deg, linspace, asarray
from numpy.random import random, randint, normal, shuffle
import os  # handy system and path functions

# Store info about the experiment session
expName = u'visualSearch1'  # from the Builder filename that created this script
expInfo = {u'session': u'001', u'participant': u'True'}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False: core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# Setup files for saving
if not os.path.isdir('data'):
    os.makedirs('data')  # if this fails (e.g. permissions) we will get error
filename = 'data' + os.path.sep + '%s_%s' %(expInfo['participant'], expInfo['date'])
logFile = logging.LogFile(filename+'.log', level=logging.EXP)
logging.console.setLevel(logging.WARNING)  # this outputs to the screen, not a file

# An ExperimentHandler isn't essential but helps with data saving
thisExp = data.ExperimentHandler(name=expName, version='',
    extraInfo=expInfo, runtimeInfo=None,
    originPath=u'/Users/jwp/Dropbox/ecem/materials/demos/builder/standard/visualSearch/visualSearch1.psyexp',
    savePickle=True, saveWideText=True,
    dataFileName=filename)

# Setup the Window
win = visual.Window(size=(2560, 1440), fullscr=True, screen=0, allowGUI=True, allowStencil=False,
    monitor=u'testMonitor', color=[0,0,0], colorSpace=u'rgb')
# store frame rate of monitor if we can measure it successfully
expInfo['frameRate']=win._getActualFrameRate()
if expInfo['frameRate']!=None:
    frameDur = 1.0/round(expInfo['frameRate'])
else:
    frameDur = 1.0/60.0 # couldn't get a reliable measure so guess

# Initialize components for Routine "trial"
trialClock = core.Clock()
XXX

distractor = visual.TextStim(win=win, ori=0, name='distractor',
    text='K',    font='Arial',
    pos=[0,0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-1.0)
target = visual.TextStim(win=win, ori=0, name='target',
    text='X',    font='Arial',
    pos=[0,0], height=0.1, wrapWidth=None,
    color='white', colorSpace='rgb', opacity=1,
    depth=-2.0)
mouse = event.Mouse(win=win)
x, y = [None, None]

ISI = core.StaticPeriod(win=win, screenHz=expInfo['frameRate'], name='ISI')

# Create some handy timers
globalClock = core.Clock()  # to track the time since experiment started
routineTimer = core.CountdownTimer()  # to track time remaining of each (non-slip) routine 

# set up handler to look after randomisation of conditions etc
trials = data.TrialHandler(nReps=2, method='random', 
    extraInfo=expInfo, originPath=u'/Users/jwp/Dropbox/ecem/materials/demos/builder/standard/visualSearch/visualSearch1.psyexp',
    trialList=data.importConditions('conditions.xlsx'),
    seed=None, name='trials')
thisExp.addLoop(trials)  # add the loop to the experiment
thisTrial = trials.trialList[0]  # so we can initialise stimuli with some values
# abbreviate parameter names if possible (e.g. rgb=thisTrial.rgb)
if thisTrial != None:
    for paramName in thisTrial.keys():
        exec(paramName + '= thisTrial.' + paramName)

for thisTrial in trials:
    currentLoop = trials
    # abbreviate parameter names if possible (e.g. rgb = thisTrial.rgb)
    if thisTrial != None:
        for paramName in thisTrial.keys():
            exec(paramName + '= thisTrial.' + paramName)
    
    #------Prepare to start Routine "trial"-------
    t = 0
    trialClock.reset()  # clock 
    frameN = -1
    routineTimer.add(10.500000)
    # update component parameters for each repeat
    targetX = random()-0.5
    targetY = random()-0.5
    distX = random([nDistractors])-0.5
    distY = random([nDistractors])-0.5
    distractor.setPos((distX[0], distY[0]))
    target.setPos([targetX, targetY])
    # setup some python lists for storing info about the mouse
    
    # keep track of which components have finished
    trialComponents = []
    trialComponents.append(distractor)
    trialComponents.append(target)
    trialComponents.append(mouse)
    trialComponents.append(ISI)
    for thisComponent in trialComponents:
        if hasattr(thisComponent, 'status'):
            thisComponent.status = NOT_STARTED
    
    #-------Start Routine "trial"-------
    continueRoutine = True
    while continueRoutine and routineTimer.getTime() > 0:
        # get current time
        t = trialClock.getTime()
        frameN = frameN + 1  # number of completed frames (so 0 is the first frame)
        # update/draw components on each frame
        
        
        # *distractor* updates
        if t >= 0.5 and distractor.status == NOT_STARTED:
            # keep track of start time/frame for later
            distractor.tStart = t  # underestimates by a little under one frame
            distractor.frameNStart = frameN  # exact frame index
            distractor.setAutoDraw(True)
        elif distractor.status == STARTED and t >= (0.5 + 10):
            distractor.setAutoDraw(False)
        
        # *target* updates
        if t >= 0.5 and target.status == NOT_STARTED:
            # keep track of start time/frame for later
            target.tStart = t  # underestimates by a little under one frame
            target.frameNStart = frameN  # exact frame index
            target.setAutoDraw(True)
        elif target.status == STARTED and t >= (0.5 + 10):
            target.setAutoDraw(False)
        # *mouse* updates
        if t >= 0.5 and mouse.status == NOT_STARTED:
            # keep track of start time/frame for later
            mouse.tStart = t  # underestimates by a little under one frame
            mouse.frameNStart = frameN  # exact frame index
            mouse.status = STARTED
            event.mouseButtons = [0, 0, 0]  # reset mouse buttons to be 'up'
        elif mouse.status == STARTED and t >= (0.5 + 10):
            mouse.status = STOPPED
        if mouse.status == STARTED:  # only update if started and not stopped!
            buttons = mouse.getPressed()
            if sum(buttons) > 0:  # ie if any button is pressed
                # abort routine on response
                continueRoutine = False
        if target.status==STARTED and continueRoutine:
            for distN in range(1,nDistractors):
                pos = distX[distN], distY[distN]
                distractor.setPos(pos)
                distractor.draw()
        # *ISI* period
        if t >= 0.0 and ISI.status == NOT_STARTED:
            # keep track of start time/frame for later
            ISI.tStart = t  # underestimates by a little under one frame
            ISI.frameNStart = frameN  # exact frame index
            ISI.start(0.5)
        elif ISI.status == STARTED: #one frame should pass before updating params and completing
            ISI.complete() #finish the static period
        
        # check if all components have finished
        if not continueRoutine:  # a component has requested a forced-end of Routine
            routineTimer.reset()  # if we abort early the non-slip timer needs reset
            break
        continueRoutine = False  # will revert to True if at least one component still running
        for thisComponent in trialComponents:
            if hasattr(thisComponent, "status") and thisComponent.status != FINISHED:
                continueRoutine = True
                break  # at least one component has not yet finished
        
        # check for quit (the [Esc] key)
        if event.getKeys(["escape"]):
            core.quit()
        
        # refresh the screen
        if continueRoutine:  # don't flip if this routine is over or we'll get a blank screen
            win.flip()
    
    #-------Ending Routine "trial"-------
    for thisComponent in trialComponents:
        if hasattr(thisComponent, "setAutoDraw"):
            thisComponent.setAutoDraw(False)
    trials.addData('targetX',targetX)
    trials.addData('targetY',targetY)
    # get info about the mouse
    x, y = mouse.getPos()
    buttons = mouse.getPressed()
    trials.addData('mouse.x', x)
    trials.addData('mouse.y', y)
    trials.addData('mouse.leftButton', buttons[0])
    trials.addData('mouse.midButton', buttons[1])
    trials.addData('mouse.rightButton', buttons[2])
    
    thisExp.nextEntry()
    
# completed 2 repeats of 'trials'



win.close()
core.quit()
