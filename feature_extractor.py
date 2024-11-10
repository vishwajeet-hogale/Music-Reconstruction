import numpy as np
import pretty_midi
import os
import json
from midi_parser import load_midi_files

binned_data = {
    "Drum" : [],
    "Piano" : [],
    "Guitar" : [],
    "Bass" : [],
    "Other" : []
}

def estimate_key(pitch_classes):
    major_template = [0, 2, 4, 5, 7, 9, 11]
    minor_template = [0, 2, 3, 5, 7, 8, 10]
    
    best_key = None
    max_score = 0
    
    for tonic in range(12):
        major_score = sum([pitch_classes[(note + tonic) % 12] for note in major_template])
        minor_score = sum([pitch_classes[(note + tonic) % 12] for note in minor_template])
        
        if major_score > max_score:
            best_key = f"{pretty_midi.note_number_to_name(tonic)} major"
            max_score = major_score
        if minor_score > max_score:
            best_key = f"{pretty_midi.note_number_to_name(tonic)} minor"
            max_score = minor_score
            
    return str(best_key)

def get_instrument_category(program, is_drum):
    if is_drum:
        return "Drum"
    elif 0 <= program <= 7:
        return "Piano"
    elif 24 <= program <= 31:
        return "Guitar"
    elif 32 <= program <= 39:
        return "Bass"
    else:
        return "Other"

def extract_advanced_features(midi, song_name="unknown"):
    if midi is None:
        return None
    
    tempo = midi.estimate_tempo()
    beat_length = 60.0 / tempo
    bar_length = 4 * beat_length
    section_duration = 20 * bar_length
    time_signature = "4/4"
    
    if midi.time_signature_changes:
        first_time_signature = midi.time_signature_changes[0]
        time_signature = f"{first_time_signature.numerator}/{first_time_signature.denominator}"

    total_duration = midi.get_end_time()
    start_times = [
        0,
        max(0, (total_duration - section_duration) / 2),
        max(0, total_duration - section_duration)
    ]
    
    all_section_features = []

    for start_time in start_times:
        end_time = min(total_duration, start_time + section_duration)
        
        for i, instrument in enumerate(midi.instruments):
            inst_features = {
                'instrument_no': i,
                'instrument_category': get_instrument_category(instrument.program, instrument.is_drum),
                'program': int(instrument.program),
                'is_drum': instrument.is_drum,
                'section_start': float(start_time),
                'section_end': float(end_time),
                'notes': [],
                'pitch_classes': [int(x) for x in np.zeros(12)],  # Ensure JSON serializable
                'velocity_mean': 0,
                'pitch_mean': 0,
                'pitch_std': 0,
                'duration_mean': 0,
                'song_name': song_name,
                'tempo': tempo,
                'time_signature': time_signature,
                'key': None
            }
            
            notes_in_section = [
                note for note in instrument.notes
                if start_time <= note.start < end_time
            ]
            
            if len(notes_in_section) > 0:
                pitches = [note.pitch for note in notes_in_section]
                velocities = [note.velocity for note in notes_in_section]
                durations = [note.end - note.start for note in notes_in_section]
                
                inst_features['pitch_mean'] = float(np.mean(pitches))
                inst_features['pitch_std'] = float(np.std(pitches))
                inst_features['velocity_mean'] = float(np.mean(velocities))
                inst_features['duration_mean'] = float(np.mean(durations))
                
                for note in notes_in_section:
                    inst_features['pitch_classes'][note.pitch % 12] += 1
                    inst_features['notes'].append({
                        'start': float(note.start),
                        'end': float(note.end),
                        'pitch': int(note.pitch),
                        'velocity': int(note.velocity)
                    })
            key = estimate_key(inst_features['pitch_classes'])
            if len(key.split()) > 1:
                inst_features['key'] = key.split()[0]
                inst_features['maj_min'] = key.split()[1]
            else:
                inst_features['key'] = key.split()[0]
                inst_features['maj_min'] = ''
                
            binned_data[inst_features['instrument_category']].append(inst_features)
            all_section_features.append(inst_features)
    
    return all_section_features

def get_binned_data():
    json_filename = "binned_data_features.json"
    with open(json_filename, 'w') as json_file:
        json.dump(binned_data, json_file, indent=4)
