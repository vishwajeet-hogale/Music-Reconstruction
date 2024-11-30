import matplotlib.pyplot as plt
import numpy as np
from genetic_algorithm import GeneticAlgorithm

ga = GeneticAlgorithm()

def box_whisker(generation_samples, fitness_scores, generation):

    plt.figure(figsize=(10, 8))
    plt.boxplot(fitness_scores, vert=True, patch_artist=True, boxprops=dict(facecolor="lightblue"))

    # Add labels and title
    plt.title(f"Score Distribution: Mutation:{ga.mutation_rate*100}%, Crossover:{ga.crossover_rate*100}%, Random:{ga.random_rate*100}%, Best Fit:{ga.best_fit_perc*100}%", fontsize=14)
    #plt.suptitle(f"Mutation:{ga.mutation_rate*100}%, Crossover:{ga.crossover_rate*100}%, Random:{ga.random_rate*100}%, Best Fit:{ga.best_fit_perc*100}%", fontsize=12, y=3)
    plt.ylabel("Scores", fontsize=12)
    plt.xlabel(f"Generations: {generation}", fontsize=12)
    plt.xticks(ticks=range(1, len(generation_samples) + 1), labels=generation_samples)
    plt.grid(axis='y', linestyle='--', alpha=0.7)
    #plt.subplots_adjust(top=0.85)

    # Show the plot
    plt.show()

def scatterplot(generation_samples, fitness_scores, generation):
    average_fitness = [np.mean(sublist) for sublist in fitness_scores]
    minimum_value = [np.min(sublist) for sublist in fitness_scores]
    maximum_value = [np.max(sublist) for sublist in fitness_scores]
    
    plt.figure(figsize=(10,8))
    plt.scatter([generation_samples], [average_fitness], color="red", s=100, label="Mean")
    plt.scatter([generation_samples], [minimum_value], color="blue", s=100, label="Minimum Score")
    plt.scatter([generation_samples], [maximum_value], color="green", s=100, label="Maximum Score")

    # Add labels and title
    plt.title("Song Fitness vs Generation", fontsize=14)
    plt.suptitle(f'Mutation:{ga.mutation_rate*100}%, Crossover:{ga.crossover_rate*100}%, Random:{ga.random_rate*100}%, Best Fit:{ga.best_fit_perc*100}%', fontsize=10)
    plt.ylabel("Fitness", fontsize=12)
    plt.xlabel(f"Generation:{generation}", fontsize=12)
    plt.legend(loc="upper left", bbox_to_anchor=(1, 1), fontsize=12)
    
    # Show the plot
    plt.tight_layout()  # To ensure the plot and legend fit within the figure
    plt.show()

def plot(samples, generations):

    num_samples = 10

    sampling_interval = (generations - 1) // (num_samples - 1)
    sampling_generations = [i for i in range(0, generations, sampling_interval)]
    if len(sampling_generations) < num_samples:  # Ensure 5 samples if there is rounding
        sampling_generations.append(generations - 1)

    fitness_scores = []
    for i in sampling_generations:
        fitness_scores.append(samples[i])
    
    box_whisker(sampling_generations, fitness_scores, generations)
    scatterplot(sampling_generations,fitness_scores, generations)