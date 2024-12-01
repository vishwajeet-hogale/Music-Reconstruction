import os
import random
import pretty_midi
import numpy as np
from helper.genetic_algorithm import GeneticAlgorithm
from helper.midi_parser import load_midi_files
from helper.feature_extractor import extract_advanced_features



def main():

    generations = 300
    n = generations/5
    ga = GeneticAlgorithm()
    ga.load_data()
    ga.generate_random_population("./binned_data_features.json")
    ga.fitness_population()
    for i in range(1,generations+1):
        ga.generation_builder()
        ga.fitness_population()
        if i % n == 0 :
            ga.call_post_process()
    ga.convert_mid_to_mp3()

if __name__ == "__main__":
    main()