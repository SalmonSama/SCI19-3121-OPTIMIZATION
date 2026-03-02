#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Genetic algorithm: maximize f(x)=(x-10)^2 on 0..63
"""

import random
import sys

POP_SIZE = 12           # N=10  nuber of chromosomes
NO_PARENTS = 4          # Number of parents ( 2*NO_PARENTS <= POP_SIZE !!)
MUT_RATE = 0.01         # p_m constant
CHROMO_LEN = 6          # chromosome CHROMO_LEN  L
ALPHABET = '01'
MAXITER = 50     # number of iterations
#
# a chromosome is a string of length CHROMO_LEN
# 
def integer_to_chromo( number ):
    ### returns a binary string of length  CHROMO_LEN , representing 'number'
    if (0 <= number) and (number < 2**CHROMO_LEN ):
        myformat = "0" + str( CHROMO_LEN ) + "b"
        return format( number, myformat )
    else: 
        print("-- integer_to_chromo --- variable named 'number' is out of bounds: ", number )
        sys.exit(1)
    
def chromo_to_integer( chromo ):
    ### converts a binary number (in string format) to an integer
    return int(chromo, 2)

def f(x):           # objective function, values are >=0
    return (x-10)**2
#
def fitness_cal( chromo ):
    #  computes the fitness value of an individual chromosome chromosome
    #  returns a list of 2:  chromosome + fitness of the chromosome (as int)
    return( [ chromo, f( chromo_to_integer( chromo ) ) ] )
#
def initialize_pop(  ):     
    # initialize the poplulation by random
    # returns the chromosomes in the population as a list
    population = []         # P(0) is a list

    for i in range(POP_SIZE):
        temp = list()
        for j in range(CHROMO_LEN ):
            temp.append(random.choice(ALPHABET))
        temp1 = ''.join( temp  )    # write as asingel string
        population.append(temp1)
    return population
#
def crossover(parent_1, parent_2  ):
    #performs a crososver of a selected chromosome pair
    #offspring_cross = []
    crossover_point = random.randint(1, CHROMO_LEN-1)
    child_1 =  parent_2[:crossover_point] + parent_1[crossover_point:]
    child_2 =  parent_1[:crossover_point] + parent_2[crossover_point:]
    return child_1, child_2

def mutate( offspring ):
    mutated_offspring = []

    for arr in offspring:
        mut_arr = []
        for i in range(len(arr)):
            char = arr[i]
            if random.random() < MUT_RATE:
                if char == '0':
                     char= '1'
                else:
                     char='0'
            mut_arr.append( char )
        newchromo = ''.join( mut_arr )          # convert list of symbols to a string
        mutated_offspring.append( newchromo )
    return mutated_offspring

####################
### main program ###

# 1) initialize population
current_population = initialize_pop(   )
best = current_population[0]            # this will be the best chromosome throughout

for k in range(MAXITER):
    
      population = []                   # list that contains: [ chomosome, fitness ]

# 2) Calculating the fitness for the current population
      for _ in range( len(current_population) ):
            population.append( fitness_cal(  current_population[_]) )
       # now population has 2 things, [chromosome, fitness]
       # 
# 3.1) select the mating pool
          # We implement the mating pool selection by roulette-wheel
      fitness_list = [ item[1] for item in population ]        ## fitness values
      selected = random.choices( population, weights = fitness_list ,  k=POP_SIZE )  # this implements roulette wheel
           
# 3.2) mate parents to make new generation
      selected_chromosomes = [item[0] for item in selected ]    # select only the chromosome part, not the fitness
      selected_sorted = random.sample( selected_chromosomes, k=POP_SIZE )   # randomly order selected_random
      crossovered = []                     #will be P(k+1) at the end
      it = iter( selected_sorted )            # make an iterator
      for kk in range( NO_PARENTS ):          # perform crossover on the first 2*NO_PARENTS chromosomes
          parent_1 = next( it ) 
          parent_2 = next( it )
          child_1, child_2 = crossover( parent_1, parent_2  )
          crossovered.append( child_1 )
          crossovered.append( child_2 )
      for kk in range(2*NO_PARENTS, POP_SIZE ):
          chromo = next( it )
          crossovered.append( chromo )
                      
# 3.3) mutating the childeren to diversfy the new generation
      current_population = mutate( crossovered  )

      # now find the best solution among the POP_SIZE cromosomes

      population=[]
      for _ in range( len(current_population) ):
            population.append( fitness_cal(  current_population[_]) )
            
      largest_entry = population[0]  # Assume the first element is the largest initially
      for item in population:
           if item[1] > largest_entry[1]:
              largest_entry = item
              
      x_value = chromo_to_integer( largest_entry[0] )
      y_value = largest_entry[1]
      print(k,"th iteration.  max at x=", x_value , "the max value  is", y_value )      
      # now we update best
      if y_value > f( chromo_to_integer(best)  ):
          best = largest_entry[0]
      current_population[-1] = best          # include the best chromosome in the population
          
print("***** f has its max at x=", chromo_to_integer( best ) , ", the max value is", f( chromo_to_integer(best)  ) )     
          

