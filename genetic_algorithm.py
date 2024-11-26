import random
import numpy as np
import os
from midi_parser import load_midi_files
from feature_extractor import extract_advanced_features, get_binned_data
import json
import pretty_midi

class GeneticAlgorithm:
    def __init__(self, population_size = 10000, mutation_rate = 0.25, crossover_rate = 0.25, best_fit_perc = 0.25, random_rate= 0.25):
        self.best_fit_perc = best_fit_perc
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.random_rate = random_rate
        self.population = None
        

    def load_data(self):
        midi_directory = './clean_midi'
        output_directory = './output'
        
        os.makedirs(output_directory, exist_ok=True)
        midi_data = load_midi_files(midi_directory)
        
        if not midi_data:
            print("No MIDI files were loaded.")
            return

        print(f"Processing {len(midi_data)} MIDI files.")
        
        features = []
        for filename, data in midi_data.items():
            midi_file = data['midi']
            extracted_features = extract_advanced_features(midi_file, data['song_name'])
            if extracted_features:
                features.extend(extracted_features)
            else:
                print(f"Warning: Failed to extract features from {filename}")

        if not features:
            print("No features were extracted.")
            return

        self.extracted_genes = get_binned_data()
        print(f"Extracted genes: {len(self.extracted_genes)} categories loaded.")

    def generate_random_population(self, file):
        population = []
        curr = []
        for i in range(self.population_size):
            for gene in self.extracted_genes.keys():
                curr.append(random.sample(self.extracted_genes[gene], 1)[0])
            population.append(curr)
            curr = []
        if self.population is None : 
            self.population = population
        # return population
    def generate_random_population_gen(self, num):
        population = []
        curr = []
        for i in range(num):
            for gene in self.extracted_genes.keys():
                curr.append(random.sample(self.extracted_genes[gene], 1)[0])
            population.append(curr)
            curr = []
        return population
    def ordered_crossover(self,parent1, parent2):
        """
        Perform crossover while maintaining instrument order (Drum, Piano, Guitar, Bass)
        """
        if len(parent1) != len(parent2):
            raise ValueError("Both parents must have the same number of instruments")
        
        # Pick a random point to swap (1, 2, or 3)
        crossover_point = random.randint(1, len(parent1) - 1)
        
        # Create children by swapping instruments after the crossover point
        child1 = parent1[:crossover_point] + parent2[crossover_point:]
        child2 = parent2[:crossover_point] + parent1[crossover_point:]
        
        return child1, child2

    def crossover(self,parents):
        """
        Generate children from multiple parents in input file
        """
        # Initialize list for children
        children = []
        
        # Process pairs of parents
        for i in range(0, len(parents) - 1, 2):
            parent1 = parents[i]
            parent2 = parents[i + 1]
            child1, child2 = self.ordered_crossover(parent1, parent2)
            children.extend([child1, child2])
        
        # Handle odd number of parents by pairing last parent with first child
        if len(parents) % 2 != 0 and children:
            last_parent = parents[-1]
            extra_child1, extra_child2 = self.ordered_crossover(last_parent, children[0])
            children.extend([extra_child1, extra_child2])

        percent_num= int(len(children)*(self.crossover_rate))
        children = random.sample(children, percent_num)
        return children


    def mutation(self, crossover_population): 
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
                child[gene][11] = tempo_manipulation(child[gene]["tempo"])  # Replace 'tempo' with the correct index/key
            elif index == 1:
                child[gene][7] = velocity_mean_manipulation(child[gene]["velocity_mean"])  # Replace 'velocity_mean' with the correct index/key
            elif index == 2:
                child[gene][13]  = key_manipulation(child[gene]["key"])  # Replace 'key' with the correct index/key


        percent_num= int(len(crossover_population)*(self.mutation_rate))
        mutated_pop = random.sample(crossover_population, percent_num)
        return mutated_pop
    
    def calculate_velocity_score(self, individual, tolerance=0.05):
            def calculate_distance_score(velocity, avg_velocity):
                if avg_velocity == 0 or velocity == 0:
                    return 1
                
                difference = abs(velocity - avg_velocity) / avg_velocity
                
                if difference <= 0.05:
                    return 20
                elif difference <= 0.10:
                    return 15
                elif difference <= 0.15:
                    return 10
                elif difference <= 0.20:
                    return 5
                else:
                    return 1

            instruments = []
            total_velocity = 0
            active_instruments = 0

            for i in range(5):
                        velocity_mean = individual[i].get('velocity_mean', 0)
                        instruments.append({'velocity': velocity_mean})
                        if velocity_mean > 0:
                            total_velocity += velocity_mean
                            active_instruments += 1


            v_avg = total_velocity / active_instruments if active_instruments > 0 else 0

            total_score = 0
            for instrument in instruments:
                score = calculate_distance_score(instrument['velocity'], v_avg)
                total_score += score
            # print(total_score)
            return total_score
    def score_tempo(self, individual):
        gene=0
        points=[]
        tempo_sum = 0
        for i in range(0,5):
            tempo_sum += individual[i].get('tempo', 100)

        tempo_mean = tempo_sum/5
        gene=0
        for j in range(0,5):
            diff = individual[j].get('tempo',100)-tempo_mean
            points.append(100-diff)

        return sum(points)/5
    def fitness(self, individual):
        score = 0
        
        # Evaluate velocity
        score += self.calculate_velocity_score(individual,tolerance=0.05)
        score += self.score_tempo(individual)
        print(score)
        return score   # Normalize score
    
    def fitness_population(self):
        scored_population = []
        for chrome in self.population:
            scored_population.append([chrome,self.fitness(chrome)])
        self.population = [i[0] for i in sorted(scored_population, key = lambda x : -x[1])]
        # print(self.population[0])
    def generation_builder(self):

        '''
        Takes the output populations from the random child generator, crossover child generator, mutated child generator, and 
        the best fit children population, and combines them into single population to be used for the next generation. Percentages 
        define the % composition of the combined population.
        '''
        # Choosing top percentage of best fit children for next gen
        num_to_pick = int(self.population_size * (self.best_fit_perc ))
        best_population = self.population[0:num_to_pick]
        crossover_population = self.crossover(self.population)
        mutated_population = self.mutation(self.population)
        random_population = self.generate_random_population_gen(int(self.population_size*self.random_rate))
        self.population = best_population + crossover_population + mutated_population + random_population

    def create_midi_from_section(section_data, filename):
        pm = pretty_midi.PrettyMIDI()
        
        # Track the instruments we've found
        found_instruments = {
            'Drum': False,
            'Piano': False,
            'Guitar': False,
            'Bass': False,
            'Other': False
        }
        
        for instrument_data in section_data:
            instrument_category = instrument_data.get('instrument_category', '')
            program = instrument_data.get('program', 0)
            is_drum = instrument_data.get('is_drum', False)
            
            if instrument_category in found_instruments:
                found_instruments[instrument_category] = True
                
                instrument = pretty_midi.Instrument(
                    program=program,
                    name=instrument_category,
                    is_drum=is_drum
                )
                
                for note_data in instrument_data.get('notes', []):
                    note = pretty_midi.Note(
                        velocity=int(note_data['velocity']),
                        pitch=int(note_data['pitch']),
                        start=float(note_data['start']),
                        end=float(note_data['end'])
                    )
                    instrument.notes.append(note)
                
                if instrument.notes:
                    print(f"Processing {instrument_category}")
                    pm.instruments.append(instrument)
        
        # Check if we found all 5 instruments
        missing = [inst for inst, found in found_instruments.items() if not found]
        if missing:
            print(f"Warning: Missing instruments in section: {', '.join(missing)}")
        
        pm.write(filename)

    def test(self):
        print(self.score_tempo(self.population[:1]))


    