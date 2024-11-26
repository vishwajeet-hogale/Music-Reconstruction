# Mutation 
import numpy as np
import random 
 

"""
population = list of lists of all children, their genes, and the gene's features


Mutate one random feature in every gene of every child in the population. 

Tempo:
    - random tempo value. Integer 30-200
Key:
    - random key. Create a dictionary of all key types. Randomize on that dictionary 
Velocity_mean:
    - Velocity_mean. random between 0-127
    - need to handle boundary conditions  
Instrument_ID: leave for now, might get complex 

"velocity_mean": 73.76086956521739,
"pitch_mean": 44.28260869565217,
"pitch_std": 3.076298195235849,
"duration_mean": 0.29790630434782633,
"song_name": "A_Campfire_Song.mid",
"tempo": 216.00021600021577,
"time_signature": "4/4",
"key": "D-1",
"maj_min": "major"

population
	child
  	genes
    	features
"""

# List of possible keys for mutation
key_list = [
    'B_major', 'Bb_major', 'A_major', 'Ab_major', 'G_major', 'Gb_major',
    'F#_major', 'F_major', 'E_major', 'Eb_major', 'D_major', 'Db_major',
    'C#_major', 'C_major', 'Cb_major', 'B_minor', 'Bb_minor', 'A#_minor',
    'A_minor', 'Ab_minor', 'G#_minor', 'G_minor', 'F#_minor', 'F_minor',
    'E_minor', 'Eb_minor', 'D#_minor', 'D_minor', 'C#_minor', 'C_minor'
]

# Tempo Mutation
def tempo_manipulation(value) -> int:
    new_tempo = np.random.randint(30, 201)
    return new_tempo

# Mean Velocity Mutation
def velocity_mean_manipulation(value) -> int:
    new_velocity_mean = np.random.randint(0, 128)  # Random value between 0 and 127 (MIDI velocity range)
    return new_velocity_mean

# Key Mutation
def key_manipulation(value) -> str:
    new_key = random.choice(key_list)
    return new_key

# Mutation Function
def mutation(crossover_population, percentage):
    """
    Mutates a random feature in every gene of every child in the population
    based on the specified mutation percentage.
    """
    mutated_pop = []

    for child in crossover_population:
        # Iterate over each gene in the child
        gene = np.random.randint(0,4) # random gene-> instrument
        index = np.random.randint(0,3) # random feature we choose to mutate
        if index == 0: 
            child[gene][11] = tempo_manipulation(child[gene][11]) #11-> tempo
        if index == 1:
            child[gene][7] = velocity_mean_manipulation(child[gene][7])  #7-> velocity
        if index == 2:
            child[gene][13] = key_manipulation(child[gene][13]) #13-> key
 
    percent_num= int(len(crossover_population)*(percentage/100))
    mutated_pop = random.sample(crossover_population, percent_num)

    return mutated_pop




  
  
  		
      
  	