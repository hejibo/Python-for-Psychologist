'''
Jibo He @ WSU
demostrate how to write a tab delimitated file.
September 24, 2014
'''
fhand = open('tabbedfile.txt','w')
for i in range(10):
    print >>fhand,1,'\t',2,'\t',3
fhand.close()