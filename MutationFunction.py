# Mutation 
import numpy as np
import random

def mutation(crossover_population, mute_rate): 
    '''
    Mutate one random feature in every gene of every child in the population. 

    Tempo:
        - random tempo value. Integer 30-200
    Key:
        - random key. Create a dictionary of all key types. Randomize on that dictionary 
    Velocity_mean:
        - Velocity_mean. random between 0-127
        - need to handle boundary conditions  
    Instrument_ID: leave for now, might get complex 
    '''
    
    key_list = [f"{i}{letter}" for i in range(1, 13) for letter in ['A', 'B']]

    # Tempo Mutation
    def tempo_manipulation(value) -> int:
        new_tempo = np.random.randint(30, 201)
        return new_tempo

    # Mean_Velocity Mutation
    def velocity_mean_manipulation(value) -> int:
        new_velocity_mean = np.random.randint(30, 101)
        return new_velocity_mean 

    # Key Mutation 
    def key_manipulation(value) -> str:
        new_key = random.choice(key_list)
        return new_key

    # Takes the children of the crossover, mutates the genes, then gives back the same children with the gene mutation update 
    for child in crossover_population:
        gene = np.random.randint(0,4)
        index = np.random.randint(0, 3)
        if index == 0:
            child[gene][11] = tempo_manipulation(child[gene][11])  # Replace 'tempo' with the correct index/key
        elif index == 1:
            child[gene][7] = velocity_mean_manipulation(child[gene][7])  # Replace 'velocity_mean' with the correct index/key
        elif index == 2:
            child[gene][13]  = key_manipulation(child[gene][13])  # Replace 'key' with the correct index/key

    mutated_population = crossover_population

    return mutated_population 