import pretty_midi
import json
import os

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

def process_json_to_midi(json_data, output_dir):
    os.makedirs(output_dir, exist_ok=True)
    
    for i, section in enumerate(json_data):
        print(f"\nProcessing section {i+1}")
        instruments = []
        if isinstance(section, list):
            for group in section:
                if isinstance(group, list):
                    for item in group:
                        if isinstance(item, dict) and 'notes' in item:
                            instruments.append(item)
        
        if instruments:
            filename = os.path.join(output_dir, f"section_{i+1}.mid")
            create_midi_from_section(instruments, filename)

with open('initial_population.json', 'r') as f:
    json_data = json.load(f)

output_directory = "D:/Boston/Northeastern/Fall Sem-24/Foundations of AI/Project/Output"
process_json_to_midi(json_data, output_directory)