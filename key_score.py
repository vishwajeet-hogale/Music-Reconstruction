import numpy as np

def key_score_function(self, population):

    # Generate list of states
    states = [f"{i}{letter}" for i in range(1, 13) for letter in ["A", "B"]]
    n = len(states)

    # Initialize adjacency matrix
    key_adj_matrix = np.zeros((n, n), dtype=int)

    # Populate adjacency matrix
    for i, state1 in enumerate(states):
        num1, letter1 = int(state1[:-1]), state1[-1]
        for j, state2 in enumerate(states):
            num2, letter2 = int(state2[:-1]), state2[-1]
            
            # Rule 1: Same letter, adjacent numbers (wrap between 1 and 12)
            if letter1 == letter2 and (num1 == num2 or abs(num1 - num2) == 1 or {num1, num2} == {1, 12}):
                key_adj_matrix[i, j] = 1
            
            # Rule 2: Same number, different letters
            if num1 == num2 and letter1 != letter2:
                key_adj_matrix[i, j] = 1
            
            # Rule 3: Self-loops
            if state1 == state2:
                key_adj_matrix[i, j] = 1

    # Print the matrix
    # print("Adjacency Matrix:")
    # print(adj_matrix)

    '''camelot_system = {
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
    }'''

    compatibility_score = 0
    max_score = 20
    # Iterates through adjacency matrix values of each gene's key
    for child in population:
        for primary_gene in child:
            for secondary_gene in child:  # Include self-pairs
                index1 = states.index(states[primary_gene])
                index2 = states.index(states[secondary_gene])
                compatibility_score += key_adj_matrix[index1, index2]

    # Gives a score out of 100, a fractional value of the max possible key score
    key_score = (compatibility_score/max_score)*100

    return key_score
    
        


