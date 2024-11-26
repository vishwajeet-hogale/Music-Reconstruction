
import json
import random

def ordered_crossover(parent1, parent2):
    """
    Perform crossover while maintaining instrument order (Drum, Piano, Guitar, Bass)
    """
    if len(parent1) != len(parent2):
        raise ValueError("Both parents must have the same number of instruments")
    
    # Pick a random point to swap (1, 2, or 3)
    crossover_point = random.randint(1, len(parent1) - 1)
    
    # Create children by swapping instruments after the crossover point
    child1 = parent1[:crossover_point] + parent2[crossover_point:]
    child2 = parent2[:crossover_point] + parent1[crossover_point:]
    
    return child1, child2

def generate_children_from_file(input_file, output_file, percentage):
    """
    Generate children from multiple parents in input file
    """
    # Load parents from input file
    with open(input_file, 'r') as f:
        parents = json.load(f)
    
    # Initialize list for children
    children = []
    
    # Process pairs of parents
    for i in range(0, len(parents) - 1, 2):
        parent1 = parents[i]
        parent2 = parents[i + 1]
        child1, child2 = ordered_crossover(parent1, parent2)
        children.extend([child1, child2])
    
    # Handle odd number of parents by pairing last parent with first child
    if len(parents) % 2 != 0 and children:
        last_parent = parents[-1]
        extra_child1, extra_child2 = ordered_crossover(last_parent, children[0])
        children.extend([extra_child1, extra_child2])
    
    # Write children to output file
    with open(output_file, 'w') as f:
        json.dump(children, f, indent=4)

    percent_num= int(len(children)*(percentage/100))
    children = random.sample(children, percent_num)
    return children


if __name__ == "__main__":
    # Example usage
    input_file = 'initial_population.json'
    output_file = 'children_population.json'
    generate_children_from_file(input_file, output_file)
    print(f"Generated children have been written to {output_file}")