'''
Jibo He @ WSU
demostrate how to open a file.
September 24, 2014
'''
fhand = open('touch-event-log-file.txt',"r")
for line in fhand:
    print line
fhand.close()
