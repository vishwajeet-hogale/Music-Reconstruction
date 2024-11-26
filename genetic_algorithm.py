import random
import numpy as np
import os
from midi_parser import load_midi_files
from feature_extractor import extract_advanced_features, get_binned_data
import json
class GeneticAlgorithm:
    def __init__(self, population_size, mutation_rate):
        self.population_size = population_size
        self.mutation_rate = mutation_rate
        self.chord_progressions = [
            ['I', 'V', 'vi', 'IV'],
            ['I', 'IV', 'V'],
            ['ii', 'V', 'I'],
            ['I', 'vi', 'IV', 'V']
        ]
        self.compatible_instruments = {
            'Piano': ['Acoustic Guitar', 'Violin', 'Cello', 'Flute'],
            'Acoustic Guitar': ['Piano', 'Bass', 'Drums'],
            'Electric Guitar': ['Bass', 'Drums', 'Synthesizer'],
            'Bass': ['Drums', 'Piano', 'Guitar'],
            'Drums': ['Bass', 'Guitar', 'Piano'],
            'Violin': ['Viola', 'Cello', 'Piano'],
            'Flute': ['Clarinet', 'Oboe', 'Piano']
        }

    def load_data(self):
        midi_directory = './clean_midi'
        output_directory = './output'
        
        # Ensure output directory exists
        os.makedirs(output_directory, exist_ok=True)
        
        # Load MIDI files and extract features
        midi_data = load_midi_files(midi_directory)
        
        if not midi_data:
            print("No MIDI files were loaded. Please check the directory and file permissions.")
            return

        print(f"Processing {len(midi_data)} MIDI files.")
        
        features = []
        for filename, data in midi_data.items():
            midi_file = data['midi']
            extracted_features = extract_advanced_features(midi_file,data['song_name'])
            if extracted_features:
                print(extracted_features)
                # time.sleep(4)
                features.extend(extracted_features)
            else:
                print(f"Warning: Failed to extract features from {filename}")

        print(f"Extracted features from {len(features)} MIDI files.")

        if not features:
            print("No features were extracted. Cannot proceed with genetic algorithm.")
            return
        get_binned_data()
    def extract_json_data(self,file):
        extracted_genes = json.load(open(file))
        return extracted_genes
    def extract_json_data(file):
        extracted_genes = json.load(open(file))
        return extracted_genes
    def generate_random_population(population_size, file):
        extracted_genes = self.extract_json_data(file)
        population = []
        curr = []
        for i in range(population_size):
            for gene in extracted_genes.keys():
                curr.append(random.sample(extracted_genes[gene], 1))
            population.append(curr)
            curr = []
        return population

    def crossover(self, parent1, parent2):
        child = {}
        for key in parent1.keys():
            if key == 'instruments':
                child[key] = self.crossover_instruments(parent1[key], parent2[key])
            elif isinstance(parent1[key], (int, float)):
                child[key] = random.choice([parent1[key], parent2[key]])
            elif isinstance(parent1[key], list):
                split = random.randint(0, min(len(parent1[key]), len(parent2[key])))
                child[key] = parent1[key][:split] + parent2[key][split:]
            elif isinstance(parent1[key], np.ndarray):
                child[key] = np.where(np.random.rand(*parent1[key].shape) < 0.5, parent1[key], parent2[key])
        return child

    def crossover_instruments(self, instruments1, instruments2):
        new_instruments = []
        for i in range(max(len(instruments1), len(instruments2))):
            if i < len(instruments1) and i < len(instruments2):
                new_inst = {}
                for key in instruments1[i].keys():
                    if isinstance(instruments1[i][key], list):
                        split = random.randint(0, min(len(instruments1[i][key]), len(instruments2[i][key])))
                        new_inst[key] = instruments1[i][key][:split] + instruments2[i][key][split:]
                    else:
                        new_inst[key] = random.choice([instruments1[i][key], instruments2[i][key]])
                new_instruments.append(new_inst)
            elif i < len(instruments1):
                new_instruments.append(instruments1[i])
            else:
                new_instruments.append(instruments2[i])
        return new_instruments

    def mutate(self, individual):
        for key in individual:
            if random.random() < self.mutation_rate:
                if key == 'instruments':
                    self.mutate_instruments(individual[key])
                elif isinstance(individual[key], (int, float)):
                    individual[key] *= random.uniform(0.9, 1.1)
                elif isinstance(individual[key], list):
                    if individual[key]:
                        index = random.randint(0, len(individual[key]) - 1)
                        individual[key][index] = random.randint(0, 127)  # MIDI range
                elif isinstance(individual[key], np.ndarray):
                    individual[key] *= np.random.uniform(0.9, 1.1, individual[key].shape)
        return individual

    def mutate_instruments(self, instruments):
        for instrument in instruments:
            if random.random() < self.mutation_rate:
                instrument['program'] = random.randint(0, 127)
            if instrument['notes']:
                index = random.randint(0, len(instrument['notes']) - 1)
                instrument['notes'][index]['pitch'] = random.randint(0, 127)
                instrument['notes'][index]['velocity'] = random.randint(0, 127)

    def fitness(self, individual):
        score = 0
        
        # Evaluate overall structure
        score += len(individual['instruments']) / 10  # Reward for more instruments
        score += 1 - abs(individual['tempo'] - 120) / 120  # Prefer tempos around 120 BPM
        
        # Harmonic consistency
        chord_progression = random.choice(self.chord_progressions)
        score += self.evaluate_harmony(individual, chord_progression)
        
        # Rhythmic coherence
        score += self.evaluate_rhythm(individual)
        
        # Instrument compatibility
        score += self.evaluate_instrument_compatibility(individual)
        
        # Evaluate each instrument
        for instrument in individual['instruments']:
            score += np.sum(instrument['pitch_classes'] > 0) / 12  # Reward diverse pitch classes
            score += 1 - abs(instrument['velocity_mean'] - 64) / 64  # Prefer moderate velocities
            score += min(instrument['duration_mean'], 2) / 2  # Reward reasonable note durations
            
            # Melodic structure
            score += self.evaluate_melody(instrument)
        
        # Dynamic range
        score += self.evaluate_dynamics(individual)
        
        return score / (len(individual['instruments']) + 5)  # Normalize score

    def evaluate_harmony(self, individual, chord_progression):
        harmony_score = 0
        for instrument in individual['instruments']:
            if not instrument['is_drum']:
                notes = [note['pitch'] % 12 for note in instrument['notes']]
                for chord in chord_progression:
                    chord_tones = self.get_chord_tones(chord)
                    harmony_score += sum(1 for note in notes if note in chord_tones) / len(notes)
        return harmony_score / len(individual['instruments'])

    def get_chord_tones(self, chord):
        # Simplified chord tone mapping
        chord_map = {
            'I': [0, 4, 7],
            'ii': [2, 5, 9],
            'IV': [5, 9, 0],
            'V': [7, 11, 2],
            'vi': [9, 0, 4]
        }
        return chord_map.get(chord, [])

    def evaluate_rhythm(self, individual):
        rhythm_score = 0
        for instrument in individual['instruments']:
            note_starts = [note['start'] for note in instrument['notes']]
            intervals = np.diff(sorted(note_starts))
            rhythm_score += 1 - np.std(intervals) / np.mean(intervals)  # Reward consistent rhythms
        return rhythm_score / len(individual['instruments'])

    def evaluate_instrument_compatibility(self, individual):
        compatibility_score = 0
        instruments = [self.get_instrument_name(inst['program']) for inst in individual['instruments']]
        for i, inst1 in enumerate(instruments):
            for inst2 in instruments[i+1:]:
                if inst2 in self.compatible_instruments.get(inst1, []):
                    compatibility_score += 1
        max_possible_score = (len(instruments) * (len(instruments) - 1)) / 2
        return compatibility_score / max_possible_score if max_possible_score > 0 else 0

    def get_instrument_name(self, program):
        # Simplified mapping of MIDI program numbers to instrument names
        if 0 <= program <= 7:
            return 'Piano'
        elif 24 <= program <= 31:
            return 'Guitar'
        elif 32 <= program <= 39:
            return 'Bass'
        elif program == 118:
            return 'Drums'
        else:
            return 'Other'

    def evaluate_melody(self, instrument):
        if len(instrument['notes']) < 2:
            return 0
        
        pitches = [note['pitch'] for note in instrument['notes']]
        intervals = np.diff(pitches)
        
        # Reward for a mix of steps and leaps
        step_ratio = sum(abs(i) <= 2 for i in intervals) / len(intervals)
        melody_score = 1 - abs(step_ratio - 0.6)  # Aim for about 60% steps
        
        # Penalize excessive repetition
        unique_pitches = len(set(pitches))
        melody_score += unique_pitches / len(pitches)
        
        return melody_score / 2

    def evaluate_dynamics(self, individual):
        velocities = [note['velocity'] for inst in individual['instruments'] for note in inst['notes']]
        if not velocities:
            return 0
        velocity_range = max(velocities) - min(velocities)
        return min(velocity_range / 64, 1)  # Reward dynamic range, max score at 64 (half the MIDI range)

    def evolve(self, population, generations):
        for _ in range(generations):
            fitness_scores = [self.fitness(ind) for ind in population]
            parents = random.choices(population, weights=fitness_scores, k=self.population_size)
            new_population = []
            for i in range(0, self.population_size, 2):
                parent1, parent2 = parents[i], parents[i+1]
                child1 = self.crossover(parent1, parent2)
                child2 = self.crossover(parent2, parent1)
                new_population.extend([self.mutate(child1), self.mutate(child2)])
            population = new_population
        return max(population, key=self.fitness)