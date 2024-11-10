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

def main():
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
    # # Initialize genetic algorithm
    # ga = GeneticAlgorithm(population_size=50, mutation_rate=0.1)
    
    # # Generate multiple versions
    # num_versions = 5
    # versions = generate_multiple_versions(ga, features, num_versions, generations=20)
    
    # # Analyze and save each version
    # for i, version in enumerate(versions):
    #     analysis = analyze_version(version, features, ga)
        
    #     print(f"\nAnalysis of Version {i+1}:")
    #     print(f"Number of instruments: {analysis['num_instruments']}")
    #     print(f"Tempo: {analysis['tempo']} BPM")
    #     print(f"Total duration: {analysis['total_duration']:.2f} seconds")
    #     print("Instrument breakdown:")
    #     for inst, count in analysis['instrument_breakdown'].items():
    #         print(f"  {inst}: {count}")
    #     print("Feature similarity to original MIDI files:")
    #     for filename, similarity in analysis['feature_similarity'].items():
    #         print(f"  {filename}: {similarity:.2f}")
        
    #     # Generate new MIDI file from the version
    #     new_midi = create_midi_from_features(version)
    #     output_file = os.path.join(output_directory, f'generated_music_v{i+1}.mid')
    #     new_midi.write(output_file)
    #     print(f"Generated MIDI file: {output_file}")

if __name__ == "__main__":
    main()