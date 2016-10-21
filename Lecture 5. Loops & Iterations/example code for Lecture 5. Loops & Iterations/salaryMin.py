__author__ = 'hejibo'

salaryList = [10000, 3000, 7000, 9000]
MinSalary = 700000
for salary in salaryList:
    if salary<MinSalary:
        MinSalary=salary
print MinSalary