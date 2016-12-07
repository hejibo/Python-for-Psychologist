'''
__author__ = 'jibo He'
September 8, 2014
Demostrate string operation and file path operation

'''


filename='/Users/hejibo/Dropbox/Barb & Jibo/mobile usability - auto quote system- state farm vs. geico/Subject Data/s06f37state/activityLog-06-27-16-09-04-s06f37state.txt'



conditionidentifier = filename[-15:-4]
print conditionidentifier
condition = conditionidentifier[-5:]
print condition
subject = int(conditionidentifier[1:3])
print subject



lastslash=filename.rfind("/")
rootfolder = filename[:lastslash+1]
print rootfolder

filenameOnly = filename[lastslash+1:]
print filenameOnly

fileExtension = filename[-3:]
print fileExtension
