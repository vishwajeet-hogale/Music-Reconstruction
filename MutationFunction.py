# Mutation 
import numpy as np
import random

def mutation(crossover_population): 
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
    
    key_list = [ 
        'B_major', 'Bb_major', 'A_major', 'Ab_major', 'G_major', 'Gb_major', 'F#_major', 
        'F_major', 'E_major', 'Eb_major', 'D_major', 'Db_major', 'C#_major', 'C_major', 
        'Cb_major', 'B_minor', 'Bb_minor', 'A#_minor', 'A_minor', 'Ab_minor', 'G#_minor', 
        'G_minor', 'F#_minor', 'F_minor', 'E_minor', 'Eb_minor', 'D#_minor', 'D_minor', 
        'C#_minor', 'C_minor'
    ]

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
        for gene in child:
            index = np.random.randint(0, 3)
            if index == 0:
                val = tempo_manipulation(gene['tempo'])  # Replace 'tempo' with the correct index/key
                gene['tempo'] = val
            elif index == 1:
                val = velocity_mean_manipulation(gene['velocity_mean'])  # Replace 'velocity_mean' with the correct index/key
                gene['velocity_mean'] = val
            elif index == 2:
                val = key_manipulation(gene['key'])  # Replace 'key' with the correct index/key
                gene['key'] = val

    return crossover_population