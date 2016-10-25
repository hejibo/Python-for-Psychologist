'''
By Jibo He @ WSU
Sep 16,2014
load the data source for an experiment
'''
infile = open('datasource.csv','r')
datasource ={}
for line in infile.readlines()[1:]:
    trial,number = line.split(',')
    datasource[trial]=int(number.strip())

print datasource
infile.close()
print '-_-!'