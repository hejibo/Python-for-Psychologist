'''
__author__ = 'hejibo'
demostrate how to read excel using python
'''
import xlrd

from xlrd import open_workbook
wb = open_workbook('simple.xls')
for s in wb.sheets():
    print 'Sheet:',s.name

    for row in range(s.nrows):
        for col in range(s.ncols):
            print s.cell(row,col).value

