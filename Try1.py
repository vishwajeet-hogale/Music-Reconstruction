from midi2audio import FluidSynth
from pydub import AudioSegment
import os

def midi_to_mp3(midi_file, output_file, soundfont_path="GeneralUser.sf2" ):
    try:
        if not os.path.exists(soundfont_path):
            raise FileNotFoundError(f"SoundFont file '{soundfont_path}' not found.")
        
        fs = FluidSynth(soundfont_path)
        wav_file = output_file.replace('.mp3','.wav')
        fs.midi_to_audio(midi_file, wav_file)

        audio = AudioSegment.from_file(wav_file, format="wav")
        audio.export(output_file, format="mp3")

        os.remove(wav_file)

        print(f"mp3 file saved at: {output_file}")

    except Exception as e:
        print(f"error during conversion: {e}")
