#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genetic algorithm: maximize f(x,y) on Omega=[-3,3] x [-3,3] with the
'continuous' genetic algorithm
"""

import numpy 
import random


POP_SIZE = 20           # mumber N of chromosomes
NO_PARENTS = 8          # Number of parents ( 2*NO_PARENTS <= POP_SIZE !!)
MUT_RATE = 0.01         # mutatin rat = p_m constant
MAXITER = 200           # number of iterations
# describe Omega as a rectangle [x_min, x_max] x [y_min , y_max]
X_MIN=-3.0
X_MAX=3.0
Y_MIN=-3.0
Y_MAX=3.0

# 
def f(x,y):           # objective function, adjusted to return a non-negative value
    term_1 = 3*(1-x)**2 * numpy.exp( -x**2 - (y+1)**2 )
    term_2 = 10 * ( 0.2*x - x**3 - y**5 ) * numpy.exp( -(x**2+y**2)  )
    term_3 = numpy.exp( -(x+1)**2 - y**2 )/3.0 
    return term_1 - term_2 - term_3
 
    
def fitness_cal( x, y  ):
    #  computes the fitness value of an individual chromosome 
    #  if fitness is different from f(x,y)
    #  fitness function must have values >=0 in this algorithm
    value = f( x, y )
    if ( value < 0. ):                    # we must return a positive value
        value = 0. 
    return value
#
def initialize_pop(  ):     
    # initialize the poplulation by random
    # returns the chromosome population as a numpy array   population[ POP_SIZE, 3 ]
    # each list consists of x and y-coordinates and fitness of (x,y)
    population = numpy.zeros( (POP_SIZE, 3) )

    for i in range(POP_SIZE):         # choose random positions
        x = numpy.random.uniform( X_MIN, X_MAX )
        y = numpy.random.uniform( Y_MIN, Y_MAX )
        population[i,0]= x    
        population[i,1]= y
        population[i,2]= fitness_cal( x ,y )
    return population
#
def fix( chromo ):          
    # make sure that (x,y) lies within Omega.
    # If it falls outsie of Omega, move it to the boundary of Omega
    fixed = chromo
    if fixed[0] < X_MIN:
        fixed[0] = X_MIN
    if fixed[0] > X_MAX:
        fixed[0] = X_MAX    
    if fixed[1] < Y_MIN:
        fixed[1] = Y_MIN
    if fixed[1] > Y_MAX:
        fixed[1] = Y_MAX  
    return fixed
#
def crossover(parent_1, parent_2 ):
    #performs a 'crososver' of a selected chromosome pair
    #offspring_cross = []
    alpha = random.random()     # random number in [0,1]
    # create random locations with normal distributed components
    w_1 = numpy.array( [ numpy.random.randn(), numpy.random.randn() ] )
    w_2 = numpy.array( [ numpy.random.randn(), numpy.random.randn() ] )
    child_1 = alpha*parent_1 + (1.0-alpha)*parent_2 + w_1
    child_2 = alpha*parent_2 + (1.0-alpha)*parent_1 + w_2
    child_1 = fix( child_1 )
    child_2 = fix( child_2 )
    return child_1, child_2

def mutate(chromo): 
    # mutates a single chromosome randomly
    mutated = chromo
    if random.random() < MUT_RATE:          # do we mutate ?
               alpha = random.random()
               w_x = numpy.random.uniform( X_MIN, X_MAX )
               w_y = numpy.random.uniform( Y_MIN, Y_MAX )
               w = numpy.array( [ w_x, w_y ] )
               mutated = alpha * chromo + (1.0-alpha) * w            
    return mutated

####################
### main program ###

# 1) initialize population
population = initialize_pop(  )
best = numpy.array( [ 0, 0, 0 ] )         # this will be the best chromosome throughout

for k in range(MAXITER):
    
# 2) Calculating the fitness for the current population
      for i in range( POP_SIZE ):
            population[ i, 2 ] = fitness_cal(  population[ i, 0 ], population[ i, 1 ]  ) 
# 
# 3.1) select the mating pool
      # We implement the mating pool selection by roulette-wheel
      indices = numpy.arange( 0, POP_SIZE )
      weights = population[:, 2]            # these are the fitness values
      selected = random.choices( indices, weights = weights ,  k=POP_SIZE )  # this implements roulette wheel, with replacement
      random.shuffle( selected )                 # re-arrange order. not really needed 
# 3.2) mate parents to make new generation
      selected_chromosomes = numpy.zeros( (POP_SIZE, 3) )
      for i in range( POP_SIZE ):
          selected_chromosomes[i,:] = population[ selected[i] , :]

      crossovered = selected_chromosomes                #
      for kk in range( NO_PARENTS ):                    # perform pairwise crossover on the first 2*NO_PARENTS chromosomes
          parent_1 = selected_chromosomes[2*kk,0:2] 
          parent_2 = selected_chromosomes[2*kk+1,0:2]
          child_1, child_2 = crossover( parent_1, parent_2 )
          crossovered[2*kk,0:2]   = child_1
          crossovered[2*kk+1,0:2] = child_2
                      
# 3.3) mutate all chromosomes to diversfy the new generation
      for i in range( POP_SIZE ):
             population[i,0:2]  = mutate( crossovered[i,0:2]  )

      # now find the best solution among the POP_SIZE cromosomes
      # compute fitness
      for i in range( POP_SIZE ):
            population[i,2]  =  fitness_cal( population[i,0], population[i,1] )
            
                #  the following loop could be streamelined with  
                #  largest_entry = population[ numpy.argmax( population[:,2] )  ]
      largest_entry = population[0]  # Assume the first element is the largest initially
      for i in range( POP_SIZE ):
           if population[i,2] > largest_entry[2]:
              largest_entry = population[i]
              
      x_value = largest_entry[0]
      y_value = largest_entry[1] 
      f_value = largest_entry[2]
      print("%2d -th iteration.  max at (x,y)=(%.4f,%.4f), the max value  is %.4f" %( k, x_value, y_value, f_value ) )
      # now we update best
      if f_value > best[ 2 ]:
          best = numpy.copy( largest_entry )
      population[-1] = numpy.copy( best )             # keep best as an active chromsome

x_best = best[0]
y_best = best[1] 
f_best = best[2]
print("***** f has its max at ((x,y)=(%.4f,%.4f), the max value  is %.4f" %( x_best, y_best , f( x_best, y_best ) )     )
          

