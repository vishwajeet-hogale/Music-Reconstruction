import mido

import mido

def extract_music_gene_with_instruments(midi_file_path):
    midi_file = mido.MidiFile(midi_file_path)
    gene = []

    # Dictionary to keep track of the current instrument (program) for each channel
    channel_instruments = {}

    for track in midi_file.tracks:
        time = 0  # Accumulated time for note timing
        for message in track:
            time += message.time

            if message.type == 'program_change':
                # Update the instrument for the channel
                channel_instruments[message.channel] = message.program

            elif message.type == 'note_on' and message.velocity > 0:
                # Extract note info
                pitch = message.note
                velocity = message.velocity
                channel = message.channel
                instrument = channel_instruments.get(channel, 0)  # Default to 0 if no program change

                # Find duration by looking for the corresponding note_off
                duration = 0
                for msg in track[track.index(message)+1:]:
                    duration += msg.time
                    if msg.type == 'note_off' and msg.note == pitch and msg.channel == channel:
                        break

                # Append pitch, time, velocity, duration, and instrument information
                gene.append((pitch, time, velocity, duration, instrument))

    return gene

# Example usage
gene = extract_music_gene_with_instruments("./piratesofc.mid")
print("Extracted Gene for Music Reconstruction (with Instruments):")
for note_info in gene:
    print(note_info)


# Example usage
gene = extract_music_gene_with_instruments("./piratesofc.mid")
print("Extracted Gene for Music Reconstruction:")
for note_info in gene:
    print(note_info)


