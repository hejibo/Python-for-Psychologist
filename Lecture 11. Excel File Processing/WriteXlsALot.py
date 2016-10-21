import xlwt
book = xlwt.Workbook(encoding="utf-8")

sheet1 = book.add_sheet("ShowMeThePower")
for row in xrange(1,10):
    for col in xrange(1,10):
        sheet1.write(row-1, col-1, "%s * %s = %s"%(row,col,row*col))

book.save("WriteAlot.xls")
print '-_-!'