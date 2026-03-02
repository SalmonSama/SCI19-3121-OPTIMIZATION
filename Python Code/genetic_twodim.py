#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genetic algorithm: maximize f(x,y) on Omega=[-3,3] x [-3,3] with the
'discrete' genetic algorithm
"""
import numpy
import random
import sys

## parameters that can be modified
POP_SIZE = 20           # number of chromosomes
NO_PARENTS = 8          # Number of parents ( 2*NO_PARENTS <= POP_SIZE !!)
MUT_RATE = 0.01         # p_m constant
HALF_CHROMO_LEN = 16    # length of half a chromosome (represents on coordinate) 
ALPHABET = '01'
MAXITER = 200     # number of iterations
#
#    don't change
CHROMO_LEN = 2 * HALF_CHROMO_LEN
# 
def integer_to_chromo( number ):
    ### returns a binary string of length  CHROMO_LEN , representing 'number'
    if (0 <= number) and (number < 2**HALF_CHROMO_LEN ):
        myformat = "0" + str( HALF_CHROMO_LEN ) + "b"
        return format( number, myformat )
    else: 
        print("-- integer_to_chromo --- variable named 'number' is out of bounds: ", number )
        sys.exit(1)
    
def chromo_to_integer( chromo ):
    ### converts a binary number (in string format) as an integer
    return int(chromo, 2)

def f(x,y):           # objective function
    term_1 = 3*(1-x)**2 * numpy.exp( -x**2 - (y+1)**2 )
    term_2 = 10 * ( 0.2*x - x**3 - y**5 ) * numpy.exp( -(x**2+y**2)  )
    term_3 = numpy.exp( -(x+1)**2 - y**2 )/3.0 
    return  term_1 - term_2 - term_3

def fitness_value( x, y ):
    #  the algorithm requires positive fitness
    value = f( x, y )
    if ( value < 0 ):                       # we must return a positive value
        value = 0 
    return value

def shift_back( tilde_x, tilde_y ):
    #  change (tilde x, tilde y) back to (x,y)
    div = float( 2**16 - 1 )
    x =  6.0 / div * tilde_x - 3.0
    y =  6.0 / div * tilde_y - 3.0
    return  x, y
#
def chromo_to_xy( chromo ):
    #  translates chromsome back to (x,y) values
    chromo_x = chromo[ :HALF_CHROMO_LEN ]
    chromo_y = chromo[ HALF_CHROMO_LEN: ]
    tilde_x = chromo_to_integer( chromo_x )
    tilde_y = chromo_to_integer( chromo_y )
    x, y = shift_back( tilde_x, tilde_y )
    return [x,y] 
    
def fitness_cal( chromo ):
    #  computes the fitness value of an individual chromosome chromosome
    #  returns a list of 2:  chromosome + fitness of the chromosome (as int)
    [ x, y ] = chromo_to_xy( chromo )
    return( [ chromo, fitness_value( x, y ) ] )
#
def initialize_pop(  ):     
    # initialize the poplulation by random
    # returns the chromosomes in the population as a list
    population = []         # P(0) is a list
    for i in range(POP_SIZE):
        temp = list()
        for j in range(CHROMO_LEN ):
            temp.append(random.choice(ALPHABET))
        temp1 = ''.join( temp  )    # write as a single string, not a list
        population.append(temp1)
    return population
#
def crossover(parent_1, parent_2 ):
    #performs a crososver to a selected chromosome pair
    #offspring_cross = []
    crossover_point = random.randint(1, CHROMO_LEN-1)
    child_1 =  parent_2[:crossover_point] + parent_1[crossover_point:]
    child_2 =  parent_1[:crossover_point] + parent_2[crossover_point:]
    return child_1, child_2

def mutate( offspring ):
    # apply mutation to the chromosome pool
    mutated_offspring = []

    for chromo in offspring:
        mut_chromo = []
        for i in range(len(chromo)):            # extract individual symbols from chromosome
            char = chromo[i]
            if random.random() < MUT_RATE:
                if char == '0':
                     char= '1'
                else:
                     char='0'
            mut_chromo.append( char )
        newchromo = ''.join( mut_chromo )       # convert the list of symbols to one singel string
        mutated_offspring.append( newchromo )
    return mutated_offspring

####################
### main program ###

# 1) initialize population
current_population = initialize_pop(  )
best = current_population[0]            # this will be the best chromosome throughout

for k in range(MAXITER):
    
      population = []                   # list that contains: [ chomosome, fitness ]

# 2) Calculating the fitness for the current population
      for _ in range( len(current_population) ):
            population.append( fitness_cal(  current_population[_] ) )
       # now population has 2 things, [chromosome, fitness]
       # 
# 3.1) select the mating pool
          # We implement the mating pool selection by roulette-wheel
      fitness_list = [ item[1] for item in population ]        ## fitness values
      selected = random.choices( population, weights = fitness_list ,  k=POP_SIZE )  # this implements roulette wheel to create the mating pool
           
# 3.2) mate parents to make new generation
      selected_chromosomes = [item[0] for item in selected ]    # select only the chromosome part, not the fitness
      selected_sorted = random.sample( selected_chromosomes, k=POP_SIZE )   # randomly order selected_random
      crossovered = []                     #will be P(k+1) at the end
      it = iter( selected_sorted )            # make an iterator
      for kk in range( NO_PARENTS ):          # perform crossover on the first 2*NO_PARENTS chromosomes
          parent_1 = next( it ) 
          parent_2 = next( it )
          child_1, child_2 = crossover( parent_1, parent_2 )
          crossovered.append( child_1 )
          crossovered.append( child_2 )
      for kk in range(2*NO_PARENTS, POP_SIZE ):         # append the remaining chromosomes of the mating pool
          chromo = next( it )
          crossovered.append( chromo )
                      
# 3.3) mutating the childeren to diversfy the new generation
      current_population = mutate( crossovered )

      # now find the best solution among the POP_SIZE cromosomes

      population=[]
      for _ in range( len(current_population) ):
            population.append( fitness_cal(  current_population[_]  ) )
            
      largest_entry = population[0]  # Assume the first element is the largest initially
      for item in population:
           if item[1] > largest_entry[1]:
              largest_entry = item
              
      [ x_value, y_value ]  = chromo_to_xy( largest_entry[0] )
      f_value = largest_entry[1]
      print("%2d -th iteration.  max at (x,y)=(%.4f,%.4f), the max value  is %.4f" %( k, x_value, y_value, f_value ) )
      # now we update best
      [x, y] = chromo_to_xy( best )
      if f_value > fitness_value( x, y ) :          # modify best ?
          best = largest_entry[0]
      current_population[-1] = best        # keep best as one of the chromosomes

[x_best, y_best ] = chromo_to_xy( best )
print("***** f has its max at ((x,y)=(%.4f,%.4f), the max value  is %.4f" %( x_best, y_best , f( x_best, y_best ) )     )
          

