# Python Source File Available in python_source/launchHubServer.py

from  psychopy.iohub import launchHubServer

"""
Start the ioHub Process using launchHubServer. When started with no key word arguements,
the ioHub Process is started with Display, Keyboard, Mouse, and Experiment devices created
using their default configurations.
"""
io=launchHubServer()

# get the keyboard device
#
keyboard=io.devices.keyboard

print "Press any Key to Stop the ioHub Service:"
print

# Remove any already collected keyboard events
#
keyboard.clearEvents()

while True:
    # Check for new keyboarsd events
    #
    kb_events=keyboard.getEvents()
    if kb_events:
        print "Keyboard Event(s) Detected: "
        print

        # print out each event received
        #
        for e in kb_events:
            print e
            print

        break
    io.wait(0.2)

# Stop the ioHub Process and Exit
io.quit()


