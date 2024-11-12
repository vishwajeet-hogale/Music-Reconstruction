import json
import random
def extract_json_data(file):
    extracted_genes = json.load(open(file))
    return extracted_genes


#parameters:
    #population_size(int): the number of new individuals you need to generate
    #file: the json file with your list of genes.
    #function extracts the list of genes from json file, takes a random gene from each list of available genes--
    #-- and returns a list of individuals. Each individual is an array of 5 randomly selected genes.
def generate_random_population(population_size, file):
    extracted_genes = extract_json_data(file)
    population = []
    curr = []
    for i in range(population_size):
        for gene in extracted_genes.keys():
            curr.append(random.sample(extracted_genes[gene], 1))
        population.append(curr)
    return population