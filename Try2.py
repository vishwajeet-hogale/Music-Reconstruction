from midi2audio import FluidSynth

def conver_midi_to_mp3(midi_file_path, mp3_file_path, soundfont_path):
    try:
        fs = FluidSynth(soundfont_path)
        fs.midi_to_audio(midi_file_path, mp3_file_path)
        print(f"Conversion successful! MP3 file saved at : {mp3_file_path}")
    except Exception as e:
        print(f"Error during conversion : {e}")

midi_file = "#add path for midi file"
mp3_file = "#add path for where you wanna save the output file"
soundfont = "#add path to the soundfont file"