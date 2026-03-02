#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# simulated annealing search of a one-dimensional objective function
from numpy import array
from numpy import exp, cos
from numpy.random import randn
from numpy.random import normal
from numpy.random import rand
from numpy.random import uniform
 
# objective function
def objective(x):
	#return x**2.0
    return 1-exp( -0.2*x**2) * cos( 4*x )
 

def simulated_annealing(f, bounds, n_iter, eps, temp, x_0):
    ###  simulated annealing algorithm of a one-dimensional problem
    ###
    ##   f         --> objective function
    ##   bounds    --> bounds of the interval Omega. a 1-dimensional numpy.array
    ##   eps       --> search neighborhood size  [ x_k-epsilon,x_k+epsilon ]
    ##   temp      --> initial Temperatute T_0
    ##   initial   --> intioal point x_0
    ##
    ##   returns:  [ x_best, f( x_best ) ]
    ##
	# evaluate the initial point x_best
    x_best = x_0                   
    f_x_best = f(x_best)
    # current working solution
    x_k, f_x_k  =  x_best, f_x_best
	# run the algorithm
    for k in range(n_iter):
		# take a step, using normal distribution, mean=x_k, sd=epsilon
        z_k = x_k + randn() * eps
        # alternative:   z_k = normal( loc=x_k, scale=eps ) 
		# evaluate candidate point
        f_z_k = f( z_k )
		# check for new best solution
        if f_z_k < f_x_best:
			# we have a new best point
            x_best, f_x_best = z_k, f_z_k
			# report progress
            print('>%d %.5f = %.5f' % (k, x_best, f_x_best ) )    
		# difference between candidate and curren]t point evaluation
        diff = f_z_k - f_x_k
		# calculate temperature for current epoch
        t = temp / ( float(k) + 1 ) 
		#t = temp / log( float(i + 2) ) 
		# calculate the toin-coss probability
        prob = exp(-diff / t)
		# check if we should keep the new point
        if diff < 0 or rand() < prob:
			# store the new current point
            x_k, f_x_k = z_k, f_z_k
    return [x_best, f_x_best]
 
    
# define range for input
bounds = array([-5.0, 5.0])
# define the total number iterations, this algorithm requies LARGE n_iter
n_iter = 100
# define the maximum neighborhood size / sd of normal distribution
epsilon = 0.5
# initial temperature
temperature = 1000
# perform the simulated annealing search
# generate an initial point x_0 by random
#x_0 =  uniform( low=bounds[:, 0], high=bounds[:, 1 ] )
# or specify the initial x_0
#x_0  = array([4.0]) 
x_0=4.0
best, score = simulated_annealing(objective, bounds, n_iter, epsilon, temperature, x_0 )
print('Done! The min. value is')
print('%f = %f' % ( best, score ))

