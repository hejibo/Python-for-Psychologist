import xlwt
book = xlwt.Workbook(encoding="utf-8")

sheet1 = book.add_sheet("ShowMeThePower")

sheet1.write(0, 0, "Python is Great!")
sheet1.write(1, 0, "Dominance")
sheet1.write(2, 0, "Test")
book.save("trial.xls")
print '-_-!'