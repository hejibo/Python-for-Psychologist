__author__ = 'hejibo'

ScoreDataBase = {"Jibo":100,"jasmine":101, "Mike":99,"Python":98,"Drop Table":59}

for name,score in ScoreDataBase.items():
    fhand = open('score report for %s.txt'%name,'w')
    print >>fhand,'''Dear %s,

    Your final score is %s. You did an amazing job.

    Congratulations!

    Dr. He
    '''%(name,score)
    fhand.close()
