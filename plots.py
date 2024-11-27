import matplotlib as plt
import numpy as np

def box_whisker(best_fit_scores, generation):

    plt.figure(figsize=(8, 6))
    plt.boxplot(best_fit_scores, vert=True, patch_artist=True, boxprops=dict(facecolor="lightblue"))

    # Add labels and title
    plt.title(f"Score Distribution: Generation {generation}", fontsize=14)
    plt.ylabel("Scores", fontsize=12)
    plt.xlabel(f"Generation {generation}", fontsize=12)
    plt.xticks([1], ["Array"])  # Since we only have one dataset
    plt.grid(axis='y', linestyle='--', alpha=0.7)

    # Show the plot
    plt.show()

def scatterplot(best_fit_scores, generation):
    for i in best_fit_scores:
        average_fitness = np.mean(best_fit_scores[i])
    
    plt.scatter([generation], [average_fitness], color="red", s=100, label="Mean")
    plt.axhline(average_fitness, color="blue", linestyle="--", alpha=0.7, label="Mean Line")  # Horizontal line for mean

    # Add labels and title
    plt.title(f"Average Song Fitness vs Generation", fontsize=14)
    plt.ylabel("Fitness", fontsize=12)
    plt.xlabel("Generation", fontsize=12)
    plt.legend(loc="upper right")

    # Show the plot
    plt.show()