import os
import random
import pretty_midi
import numpy as np
from genetic_algorithm import GeneticAlgorithm
from midi_parser import load_midi_files
from feature_extractor import extract_advanced_features, get_binned_data
import time 

def create_midi_from_features(features):
    midi = pretty_midi.PrettyMIDI(initial_tempo=features['tempo'])
    
    for inst_features in features['instruments']:
        instrument = pretty_midi.Instrument(program=inst_features['program'], is_drum=inst_features['is_drum'])
        for note in inst_features['notes']:
            instrument.notes.append(
                pretty_midi.Note(
                    velocity=int(note['velocity']),
                    pitch=int(note['pitch']),
                    start=float(note['start']),
                    end=float(note['end'])
                )
            )
        midi.instruments.append(instrument)
    
    return midi

def generate_multiple_versions(ga, features, num_versions=5, generations=20):
    versions = []
    for i in range(num_versions):
        print(f"Generating version {i+1}...")
        
        # Randomly select a subset of features for each version
        subset_size = random.randint(max(2, len(features) // 2), len(features))
        feature_subset = random.sample(features, subset_size)
        
        # Initialize population with the subset
        population = ga.initialize_population(feature_subset)
        
        # Evolve and get the best individual
        best_individual = ga.evolve(population, generations)
        
        versions.append(best_individual)
        
        print(f"Version {i+1} generated.")
    
    return versions

def analyze_version(version, original_features, ga):
    analysis = {
        "num_instruments": len(version['instruments']),
        "tempo": version['tempo'],
        "total_duration": version['total_duration'],
        "instrument_breakdown": {},
        "feature_similarity": {}
    }
    
    for inst in version['instruments']:
        inst_name = ga.get_instrument_name(inst['program'])
        if inst_name in analysis["instrument_breakdown"]:
            analysis["instrument_breakdown"][inst_name] += 1
        else:
            analysis["instrument_breakdown"][inst_name] = 1
    
    # Calculate feature similarity
    for i, features in enumerate(original_features):
        similarity = calculate_similarity(version, features)
        analysis["feature_similarity"][f"Original_{i+1}"] = similarity
    
    return analysis

def calculate_similarity(version, original):
    similarity = 0
    total_features = 0
    
    for key in version.keys():
        if key in original and key != 'instruments':
            if isinstance(version[key], (int, float)):
                max_value = max(abs(version[key]), abs(original[key]))
                if max_value != 0:
                    similarity += 1 - abs(version[key] - original[key]) / max_value
                else:
                    similarity += 1  # If both are zero, consider them identical
                total_features += 1
    
    if total_features > 0:
        return similarity / total_features
    else:
        return 0
def load_data():
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


def main():
    pass
    

if __name__ == "__main__":
    main()