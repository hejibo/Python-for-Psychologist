'''
By Jibo He @ WSU
Sep 16,2014
demostrate a visual n-back task
'''

from psychopy import visual, core, event
import instructionFile
import EndOfExperimentFile
instructionFile.showInstruction('instruction.txt')



# load the data source
infile = open('datasource.csv','r')
datasource ={}
for line in infile.readlines()[1:]:
    trial,number = line.split(',')
    datasource[trial]=int(number.strip())

print datasource
infile.close()

#create a window to draw in
myWin = visual.Window((800.0,800.0),allowGUI=False,winType='pyglet',
            monitor='testMonitor', units ='deg', screen=0)
myWin.setRecordFrameIntervals()
#choose some fonts. If a list is provided, the first font found will be used.
fancy = ['Monotype Corsiva', 'Palace Script MT', 'Edwardian Script ITC']

ResponseList =[]
#INITIALISE SOME STIMULI
for trial in xrange(1,len(datasource)):
    number = visual.TextStim(myWin, color='#FFFFFF',
                            text = str(datasource[str(trial)]
                       ),
                            units='norm', height=0.1,
                            pos=[0, 0.0], alignHoriz='right',alignVert='top',
                            font=fancy)


    number.draw()
        
    myWin.flip()
    inputs = event.waitKeys()
    print "inputs:",inputs
    ResponseList.extend(inputs)

    #pause, so you get a chance to see it!
    core.wait(5.0)

outfile = open("response-n-back-task.txt",'w')
for i in ResponseList:
    print >>outfile,i
outfile.close()

EndOfExperimentFile.showInstruction('EndOfExperimentInstruction.txt')

