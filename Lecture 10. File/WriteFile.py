'''
Jibo He @ WSU
demostrate how to write a file.
September 24, 2014
'''
fhand = open('HelloWorld.txt','w')
for i in range(10):
    print >>fhand,"Hello World"
fhand.close()