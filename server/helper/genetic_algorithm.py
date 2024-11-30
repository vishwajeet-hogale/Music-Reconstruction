import random
import numpy as np
import os
from helper.midi_parser import load_midi_files
from helper.feature_extractor import extract_advanced_features, get_binned_data
import json
import pretty_midi
from collections import Counter
import time
class GeneticAlgorithm:
    def __init__(self, population_size = 1000, mutation_rate = 0.2, crossover_rate = 0.1, best_fit_perc = 0.3, random_rate= 0.4):
        self.best_fit_perc = best_fit_perc
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.crossover_rate = crossover_rate
        self.random_rate = random_rate
        self.population = None
        self.extracted_genes = None
        

    def load_data(self):
        midi_directory = '../clean_midi'
        output_directory = '../output'
        
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
                    return -400
                
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
            diff = abs(individual[j].get('tempo',100)-tempo_mean)
            points.append(100-diff)

        return sum(points)/5
    def score_time_signature(self, individual):
        time_signatures = [ind.get('time_signature') for ind in individual[:5]]
        counts=Counter(time_signatures) # count occurences of each time signature
        max_freq = max(counts.values()) # get the highest frequency of time signature

        if max_freq==5:
            score=100
        elif max_freq==4:
            score = 80
        elif max_freq==3:
            score = 60
        elif max_freq==2:
            score = 40
        else:
            score = 20
        return score
    def key_score_function(self, individual):
        camelot_system = {
            "Db minor": "12A",
            "E major": "12B",
            "F# minor": "11A",
            "A major": "11B",
            "B minor": "10A",
            "D major": "10B",
            "E minor": "9A",
            "G major": "9B",
            "A minor": "8A",
            "C major": "8B",
            "D minor": "7A",
            "F major": "7B",
            "G minor": "6A",
            "Bb major": "6B",
            "C minor": "5A",
            "Eb major": "5B",
            "F minor": "4A",
            "Ab major": "4B",
            "Bb minor": "3A",
            "Db major": "3B",
            "Eb minor": "2A",
            "F# major": "2B",
            "Ab minor": "1A",
            "B major": "1B",
        }
        # Generate list of states
        states = [f"{i}{letter}" for i in range(1, 13) for letter in ["A", "B"]]
        n = len(states)

        # Initialize adjacency matrix
        key_adj_matrix = np.zeros((n, n), dtype=int)

        # Populate adjacency matrix
        for i, state1 in enumerate(states):
            num1, letter1 = int(state1[:-1]), state1[-1]
            for j, state2 in enumerate(states):
                num2, letter2 = int(state2[:-1]), state2[-1]
                
                # Rule 1: Same letter, adjacent numbers (wrap between 1 and 12)
                if letter1 == letter2 and (num1 == num2 or abs(num1 - num2) == 1 or {num1, num2} == {1, 12}):
                    key_adj_matrix[i, j] = 1
                
                # Rule 2: Same number, different letters
                if num1 == num2 and letter1 != letter2:
                    key_adj_matrix[i, j] = 1
                
                # Rule 3: Self-loops
                if state1 == state2:
                    key_adj_matrix[i, j] = 1

        # Print the matrix
        # print("Adjacency Matrix:")
        # print(adj_matrix)

        '''camelot_system = {
            "Db minor": "12A",
            "E major": "12B",
            "F# minor": "11A",
            "A major": "11B",
            "B minor": "10A",
            "D major": "10B",
            "E minor": "9A",
            "G major": "9B",
            "A minor": "8A",
            "C major": "8B",
            "D minor": "7A",
            "F major": "7B",
            "G minor": "6A",
            "Bb major": "6B",
            "C minor": "5A",
            "Eb major": "5B",
            "F minor": "4A",
            "Ab major": "4B",
            "Bb minor": "3A",
            "Db major": "3B",
            "Eb minor": "2A",
            "F# major": "2B",
            "Ab minor": "1A",
            "B major": "1B",
        }'''

        compatibility_score = 0
        max_score = 20
        # Iterates through adjacency matrix values of each gene's key

        for primary_gene in individual:
            for secondary_gene in individual:  # Include self-pairs
                index1 = states.index(primary_gene["camelot_key"])
                index2 = states.index(secondary_gene["camelot_key"])
                compatibility_score += key_adj_matrix[index1, index2]

        # Gives a score out of 100, a fractional value of the max possible key score
        key_score = (compatibility_score/max_score)*100

        return key_score
        
    def score_recombination(self, individual):
        track_IDs = [ind.get('song_name') for ind in individual[:5]]
        if len(track_IDs) != len(set(track_IDs)):
            recombination_score = -400
        else:
            recombination_score = 0
            
        return recombination_score

    def fitness(self, individual):
        score = 0
        
        # Evaluate velocity
        score += self.calculate_velocity_score(individual,tolerance=0.05)
        score += self.score_tempo(individual)
        score += self.score_time_signature(individual)
        score += self.key_score_function(individual)
        score += self.score_recombination(individual)
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

    def create_midi_from_section(self, section_data, filename):
        pm = pretty_midi.PrettyMIDI()

        found_instruments = {
            'Drum': False, 'Piano': False, 'Guitar': False, 
            'Bass': False, 'Other': False
        }

        instrument_notes = []
        max_end_time = 0

        # Create notes for each instrument, starting each instrument at zero
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

                # Find the earliest start time for this instrument
                instrument_start = float('inf')
                for note_data in instrument_data.get('notes', []):
                    note_start = float(note_data['start'])
                    instrument_start = min(instrument_start, note_start)

                # Create notes with timing relative to this instrument's start
                for note_data in instrument_data.get('notes', []):
                    note_start = float(note_data['start']) - instrument_start  # Shift to zero
                    note_end = float(note_data['end']) - instrument_start     # Keep relative duration
                    
                    note = pretty_midi.Note(
                        velocity=int(note_data['velocity']),
                        pitch=int(note_data['pitch']),
                        start=note_start,
                        end=note_end
                    )
                    instrument.notes.append(note)
                    max_end_time = max(max_end_time, note_end)

                instrument_notes.append(instrument)

        # Fill gaps for each instrument independently
        for instrument in instrument_notes:
            if instrument.notes:
                current_end = max(note.end for note in instrument.notes)
                pattern_start = 0  # Since we've already shifted to zero

                while current_end < max_end_time:
                    replicated_notes = []
                    for note in instrument.notes:
                        new_start = current_end + note.start  # Use zero-based timing
                        new_end = new_start + (note.end - note.start)

                        if new_start >= max_end_time:
                            break
                        if new_end > max_end_time:
                            new_end = max_end_time

                        replicated_notes.append(
                            pretty_midi.Note(
                                velocity=note.velocity,
                                pitch=note.pitch,
                                start=new_start,
                                end=new_end
                            )
                        )

                    instrument.notes.extend(replicated_notes)
                    current_end = max(note.end for note in instrument.notes)

        # Add instruments to MIDI
        for instrument in instrument_notes:
            print(f"Processing {instrument.name}")
            pm.instruments.append(instrument)

        # Check for missing instruments
        missing = [inst for inst, found in found_instruments.items() if not found]
        if missing:
            print(f"Warning: Missing instruments in section: {', '.join(missing)}")

        pm.write(filename)

    def process_json_to_midi(self, json_data, output_dir):
        """
        Process population data and create MIDI files
        """
        os.makedirs(output_dir, exist_ok=True)
        print("Starting MIDI processing...")
        
        # Debug print to understand data structure
        print(f"First element type: {type(json_data[0]) if json_data else 'No data'}")
        
        for i, section in enumerate(json_data):
            print(f"\nProcessing section {i+1}")
            instruments = []
            
            # Handle single instrument dictionary
            if isinstance(section, dict) and 'notes' in section:
                instruments.append(section)
            
            # Handle list of instruments
            elif isinstance(section, list):
                # If it's already a flat list of instruments
                if all(isinstance(item, dict) and 'notes' in item for item in section):
                    instruments.extend(section)
                # If it's a nested list
                else:
                    for group in section:
                        if isinstance(group, dict) and 'notes' in group:
                            instruments.append(group)
                        elif isinstance(group, list):
                            for item in group:
                                if isinstance(item, dict) and 'notes' in item:
                                    instruments.append(item)

            if instruments:
                print(f"Found {len(instruments)} instruments to process")
                filename = os.path.join(output_dir, f"section_{i+1}.mid")
                try:
                    self.create_midi_from_section(instruments, filename)
                    print(f"Successfully created: {filename}")
                except Exception as e:
                    print(f"Error creating MIDI file: {str(e)}")
            else:
                print(f"No valid instruments found in section {i+1}")

    def call_post_process(self):
        if not self.population or not isinstance(self.population, list):
            print("No data in population or invalid structure.")
            return

        print("\n=== Population Structure Analysis ===")
        print(f"Total population size: {len(self.population)}")
        
        # Analyze first individual in detail
        if self.population:
            first_individual = self.population[0]
            print("\nFirst Individual Structure:")
            print(f"Type: {type(first_individual)}")
            print(f"Length: {len(first_individual)}")
            print("\nDetailed content of first individual:")
            print(json.dumps(first_individual, indent=2))

        print("\n=== Processing for MIDI Generation ===")
        json_data = self.population[:5]  # Limit to first 5 groups for processing
        output_directory = "output"
        
        try:
            self.process_json_to_midi(json_data, output_directory)
            print(f"\nProcessing complete. Check {output_directory} directory")
        except Exception as e:
            print(f"Error during processing: {e}")
            import traceback
            traceback.print_exc()
