
def key_processing(self, individual):

    camelot_system = {
        "Db minor": "12A",
        "E major": "12B",
        "F# minor": "11A",
        "A major": "11B",
        "B minor": "10A",
        "D major": "10B",
        "E minor": "9A",
        "G major": "9B",
        "A minor": "8A",
        "C major": "8B",
        "D minor": "7A",
        "F major": "7B",
        "G minor": "6A",
        "Bb major": "6B",
        "C minor": "5A",
        "Eb major": "5B",
        "F minor": "4A",
        "Ab major": "4B",
        "Bb minor": "3A",
        "Db major": "3B",
        "Eb minor": "2A",
        "F# major": "2B",
        "Ab minor": "1A",
        "B major": "1B",
    }
    
    key_semitone_mapping = {
        "Db minor": 1,
        "E major": 4,
        "F# minor": 6,
        "A major": 9,
        "B minor": 11,
        "D major": 14,
        "E minor": 16,
        "G major": 19,
        "A minor": 21,
        "C major": 24,  # Reference point (0 semitones difference)
        "D minor": 26,
        "F major": 29,
        "G minor": 31,
        "Bb major": 34,
        "C minor": 36,
        "Eb major": 39,
        "F minor": 41,
        "Ab major": 44,
        "Bb minor": 46,
        "Db major": 49,
        "Eb minor": 51,
        "F# major": 54,
        "Ab minor": 56,
        "B major": 59,
    }

    note_alteration = []

    for gene in individual:
        original_key = individual[gene].get['key'] + individual[gene].get['maj_min'] # Key is the original key in letter form. Maj_min is the major/minor characteristic 
        new_key = camelot_system[individual[gene].get['camelot_key']] # New_key is just whatever the mutated key has become 

        # Creates a length(5) array, one index per gene, of the number of semitones that notes need to be altered
        note_alteration.append(key_semitone_mapping[original_key] - key_semitone_mapping[new_key]) 

    for gene in individual:
        for notes in gene['notes']:
            notes['pitch'] = notes['pitch'] + note_alteration[gene]

    return individual 

