__author__ = 'hejibo'

SalaryList =[10000,7000,60000,50000,88888,1000000]

TaxRatio = 0

for aSalary in SalaryList:
    if aSalary<10000:
        TaxRatio=0
    elif aSalary>100000:
        TaxRatio=0.30
    else:
        TaxRatio=0.20

    print "The tax ratio for ", aSalary, " is :", TaxRatio


