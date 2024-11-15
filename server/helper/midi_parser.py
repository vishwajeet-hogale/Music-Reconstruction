import os
import pretty_midi

def load_midi_files(directory):
    midi_data = {}
    print(f"Searching for MIDI files in: {os.path.abspath(directory)}")
    if not os.path.exists(directory):
        print(f"Error: Directory {directory} does not exist.")
        return midi_data

    # Walk through all subdirectories and files
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.mid') or filename.endswith('.midi'):
                file_path = os.path.join(root, filename)
                print(f"Attempting to load: {file_path}")
                try:
                    midi = pretty_midi.PrettyMIDI(file_path)
                    artist, title = parse_filename(filename)
                    midi_data[filename] = {
                        'midi': midi,
                        'artist': artist,
                        'title': title
                    }
                    print(f"Successfully loaded: {filename}")
                except Exception as e:
                    print(f"Error loading {filename}: {e}")
    
    if not midi_data:
        print("No MIDI files were successfully loaded.")
    return midi_data

def parse_filename(filename):
    # Implement parsing logic based on the file naming convention
    # For example: "Artist - Title.mid"
    parts = filename.split(' - ')
    artist = parts[0] if len(parts) > 1 else "Unknown"
    title = parts[1].rsplit('.', 1)[0] if len(parts) > 1 else filename
    return artist, title