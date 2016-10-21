import numpy
a = numpy.array([[1,2,3],
          [4,5,6],
          [7,8,9]])
print a.shape

print 'numpy array slicing'
print a[1]
print a[1,2]
print a[1,:]
print a[1,1:]

print 'numpy statistics'
print numpy.min(a),numpy.max(a),numpy.mean(a),numpy.median(a),numpy.std(a),numpy.sum(a)

# calculate rooted mean square error (RMSE)
#http://stackoverflow.com/questions/5613244/root-mean-square-in-numpy-and-complications-of-matrix-and-arrays-of-numpy

from numpy import mean, sqrt, square, arange
rms = sqrt(mean(square(a)))
print rms

# assign values
a[1,2]=99
print a

# search values
print 99 in a
print 99 not in a

# find data meets a certain criteria
print a>3
print a[a>3]

