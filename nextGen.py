

import numpy as np
import random
import generate_random_population 
import crossover 
import MutationFunction
import fitness

def generation_builder(percentage_rand, percentage_cross, percentage_mute, percentage_best, 
                       random_population, crossover_population, mutated_population, fitness_population):

    '''
    Takes the output populations from the random child generator, crossover child generator, mutated child generator, and 
    the best fit children population, and combines them into single population to be used for the next generation. Percentages 
    define the % composition of the combined population.
    '''
    # Choosing top percentage of best fit children for next gen
    num_to_pick = int(len(fitness_population) * (percentage_best / 100))
    best_population = best_population[0:num_to_pick]

    # Choosing random percentage of crossover children for next gen
    num_to_sample = int(len(crossover_population) * (percentage_cross / 100))
    random_indices = np.random.choice(len(crossover_population), num_to_sample, replace=False)
    crossover_population = crossover_population[random_indices]

    # Choosing random percentage of mutated children for next gen
    num_to_sample = int(len(mutated_population) * (percentage_mute / 100))
    random_indices = np.random.choice(len(mutated_population), num_to_sample, replace=False)
    mutated_population = mutated_population[random_indices]

    # Choosing random percentage of random children for next gen

    num_to_sample = int(len(random_population) * (percentage_rand / 100))
    random_indices = np.random.choice(len(random_population), num_to_sample, replace=False)
    mutated_population = random_population[random_indices]
