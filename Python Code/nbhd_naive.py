#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul 15 16:52:06 2025
"""

# example of neighborhood naïve random search
import numpy as np
from numpy import arange
from matplotlib import pyplot

# objective function
def f(x):
	#return x**2.0
    return 1-np.exp( -0.2*x**2) * np.cos( 4*x )

# the feasible domain Omega is an interval [r_min,r_max]
r_min, r_max = -5.0, 5.0
# size of neighborhood:  [x_k-eps,x_k+eps]
eps = 1.4;
#  stopping crterion: number of iterations
n_iter = 100
#   create a list of sample points fpr plotting
sample_points=np.zeros( n_iter ) 
# specify initial point x_0 by random
#x_0  =  r_min + rand() * (r_max - r_min)
# specify initial point x_0
x_0=4.0
#
# locate the best solution within sample_eval
x_k = x_0
for k in range( n_iter ):
    # uniform distribution in [x_k-eps,x_k+eps]
    #z_k = x_k +(  - eps + np.random.rand() * 2*eps )
    #  or normal distribution with mean x_k, sd=scale 
    z_k = np.random.normal( loc=x_k, scale=0.5 ) 
    #  test wheter z_k is outside the feasable domain:
    if  (z_k < r_min):
          z_k = r_min
    if  (z_k > r_max ):
          z_k = r_max;
    if f(z_k) < f(x_k):             # we have found a better point
         x_k = z_k
    sample_points[ k ] = x_k
        
#
# summarize best solution
print('Starting point: x_0=%.5f' % x_0 )
print('Best: f(%.5f) = %.5f' % ( x_k, f(x_k) ) )


# get ready to plot
# create a fine grid with 0.1 increments on Omega
inputs = arange(r_min, r_max, 0.1)
# compute the values of the objective function at the fine grid points
results = f(inputs)
# create a line plot of input vs result
pyplot.plot(inputs, results)
# plot the sample points over all iterations of the algorithm
sample_eval = f( sample_points  )
pyplot.scatter(sample_points, sample_eval)
# draw a vertical line at the best input
pyplot.axvline(x=x_k, ls='--', color='red')
pyplot.show()
#
#  print the list of sample points x_k
print(np.array_str( sample_points , precision=5, suppress_small=True))

