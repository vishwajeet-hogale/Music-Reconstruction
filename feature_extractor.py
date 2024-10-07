import numpy as np
import pretty_midi

def extract_advanced_features(midi):
    if midi is None:
        return None
    
    features = {
        'tempo': midi.estimate_tempo(),
        'time_signature': midi.time_signature_changes[0].numerator if midi.time_signature_changes else 4,
        'key': midi.key_signature_changes[0].key_number if midi.key_signature_changes else 0,
        'instruments': [],
        'total_duration': midi.get_end_time()
    }
    
    for instrument in midi.instruments:
        inst_features = {
            'program': instrument.program,
            'is_drum': instrument.is_drum,
            'notes': [],
            'pitch_classes': np.zeros(12),
            'velocity_mean': 0,
            'pitch_mean': 0,
            'pitch_std': 0,
            'duration_mean': 0
        }
        
        if len(instrument.notes) > 0:
            pitches = [note.pitch for note in instrument.notes]
            velocities = [note.velocity for note in instrument.notes]
            durations = [note.end - note.start for note in instrument.notes]
            
            inst_features['pitch_mean'] = np.mean(pitches)
            inst_features['pitch_std'] = np.std(pitches)
            inst_features['velocity_mean'] = np.mean(velocities)
            inst_features['duration_mean'] = np.mean(durations)
            
            for note in instrument.notes:
                inst_features['pitch_classes'][note.pitch % 12] += 1
                inst_features['notes'].append({
                    'start': note.start,
                    'end': note.end,
                    'pitch': note.pitch,
                    'velocity': note.velocity
                })
        
        features['instruments'].append(inst_features)
    
    return features