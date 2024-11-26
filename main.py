import os
import random
import pretty_midi
import numpy as np
from genetic_algorithm import GeneticAlgorithm
from midi_parser import load_midi_files
from feature_extractor import extract_advanced_features, get_binned_data
import time 



def main():

    generations = 200

    ga = GeneticAlgorithm()
    ga.load_data()
    # 0th generation 
    ga.generate_random_population("./binned_data_features.json")
    ga.fitness_population()
    # ga.test()
    # print("Hello ", ga.population[2])
    for i in range(1,generations):
        ga.generation_builder()
        print(1)
        ga.fitness_population()
        # if i % 100 == 0 :
        #     print(ga.population)

if __name__ == "__main__":
    main()