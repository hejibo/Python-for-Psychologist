!SLIDE

# PsychoPy : Getting Responses
   
    Created by Jibo He, <a>hejibo@usee.tech</a>

!SLIDE

### Table of Content
- Mouse Clicks
- Keyboard Inputs


!SLIDE left

# Mouse Clicks

!SLIDE left

# Keyboard Inputs
- show text
- capture keyboard inputs

!SLIDE left

# Capture Keyboard Inputs
- show text

~~~~{python}
CapturedResponseString = visual.TextStim(myWin, 
                        units='norm',height = 0.2,
                        pos=(0,-0.40), text='',
                        alignHoriz = 'center',alignVert='center', color=[-1,-1,-1])

captured_string = '' #key presses will be captured in this string
~~~~


!SLIDE left

# Capture Keyboard Inputs

~~~~{python}
CapturedResponseString = visual.TextStim(myWin, 
                        units='norm',height = 0.2,
                        pos=(0,-0.40), text='',
                        alignHoriz = 'center',alignVert='center', color=[-1,-1,-1])

#key presses will be captured in this string
CapturedResponseString.text = event.waitKeys()[0]
~~~~


!SLIDE left

# Capture Mouse Clicks
- event.Mouse() 

~~~~{python}
myMouse = event.Mouse()  #  will use myWin by default

if myMouse.getPressed()[0]:
    myMouse.clickReset()
    print myMouse.getPos()

~~~~

!SLIDE left

# Capture Mouse Clicks
- see testMouseClicks.py

~~~~{python}
#!/usr/bin/env python2
from psychopy import visual, core, event
from pyglet.gl import *

width = 600
height = 600
myWin = visual.Window([width,height], color='white',units='pix',monitor='testMonitor')

#This will set the windows units (pixels) to GL units
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
glOrtho(0, width, 0, height, -1, 1)

glMatrixMode(GL_MODELVIEW)
glLoadIdentity()

glEnable(GL_BLEND)
glBlendFunc(GL_ZERO, GL_SRC_COLOR)

myMouse = event.Mouse()  #  will use myWin by default


while True:
    #Triangle left
    glColor3f(1.0, 0.0, 0.0)
    glBegin(GL_TRIANGLES)
    glVertex3f(150, 550, 1)
    glVertex3f(50, 350, 1)
    glVertex3f(250, 350, -1)
    glEnd()

    if myMouse.getPressed()[0]:
        myMouse.clickReset()
        print myMouse.getPos()

    myWin.flip()

core.quit()
~~~~

