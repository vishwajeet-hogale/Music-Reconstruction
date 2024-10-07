import mido

def extract_music_gene(midi_file_path):
    midi_file = mido.MidiFile(midi_file_path)
    gene = []

    for track in midi_file.tracks:
        time = 0  # Keep track of accumulated time
        for message in track:
            # Track the time as delta times accumulate
            time += message.time
            if message.type == 'note_on' and message.velocity > 0:
                # Capture note (pitch), start time, velocity, and duration info
                pitch = message.note
                velocity = message.velocity

                # Find duration by looking for the corresponding note_off
                duration = 0
                for msg in track[track.index(message)+1:]:
                    duration += msg.time
                    if msg.type == 'note_off' and msg.note == pitch:
                        break

                # Append this information as part of the gene
                gene.append((pitch, time, velocity, duration))

    return gene

# Example usage
gene = extract_music_gene("./piratesofc.mid")
print("Extracted Gene for Music Reconstruction:")
for note_info in gene:
    print(note_info)


