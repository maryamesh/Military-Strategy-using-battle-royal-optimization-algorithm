import pandas as pd
import random
import numpy as np

# Load the dataset
dataset_path = r"C:\Users\dell\Desktop\8V280L8VQ-clash-royale-da.csv"
data = pd.read_csv(dataset_path)

# Extract the necessary columns from the dataset
my_results = data['my_result']
my_scores = data['my_score']
points = data['points']
opponent_scores = data['opponent_score']

# Set the maximum number of iterations and the shrink parameter
MaxXicle = 100
shrink = int(np.ceil(np.log10(MaxXicle)))

# Calculate the delta value for updating the shrink parameter
delta = int(round(MaxXicle / shrink))

# Set the initial bounds
lb_d = np.zeros(len(my_results))
ub_d = np.ones(len(my_results))

# Function to calculate fitness
def calculate_fitness(individual):
    fitness = 0
    for i in range(len(individual)):
        if individual[i] == 1:
            fitness += my_scores[i] - opponent_scores[i]
    return fitness
# BRO algorithm implementation
def bro_algorithm():
    # Generate initial population randomly
    population_size = 500
    population = np.random.randint(2, size=(population_size, len(my_results)))

    iter_count = 0
    delta = 0  # Define delta here
    while iter_count < delta:
        iter_count += 1

        # Calculate fitness for each individual in the population
        fitness_values = [calculate_fitness(individual) for individual in population]

        for i in range(population_size):
            # Compare the ith soldier with the nearest one (jth)
            j = random.randint(0, population_size - 1)
            dam = j
            vici = i
            if fitness_values[i] < fitness_values[j]:
                dam = i
                vici = j

            if fitness_values[dam] < Threshold:
                # Update the position of damaged soldier
                best = np.argmax(fitness_values)
                for d in range(len(my_results)):
                    population[dam][d] = random.uniform(
                        max(population[dam][d], population[best][d]),
                        min(population[dam][d], population[best][d])
                    )

                fitness_values[dam] = fitness_values[i] + 1
                fitness_values[vici] = 0
            else:
                # Reset the position of the damaged soldier to a random value within bounds
                for d in range(len(my_results)):
                    population[dam][d] = random.uniform(lb_d[d], ub_d[d])

                # Update fitness for the damaged soldier
                fitness_values[dam] = 0

        if iter_count >= delta:
            # Update bounds
            lb_d = lb_d - (ub_d - lb_d) * (fitness_values / population_size)
            ub_d = ub_d + (ub_d - lb_d) * (fitness_values / population_size)

            delta += int(round(delta / 2))

        # Set lb_d or ub_d to the original bounds if exceeded
        lb_d = np.where(lb_d < 0, 0, lb_d)
        ub_d = np.where(ub_d > 1, 1, ub_d)

    # Calculate fitness for the final population
    fitness_values = [calculate_fitness(individual) for individual in population]

    # Find the best individual in the final population
    best_individual_index = np.argmax(fitness_values)
    best_individual = population[best_individual_index]

    return best_individual, fitness_values[best_individual_index]

# Set the number of iterations and population size
num_iterations = shrink
population_size = 500

# Set the threshold value
Threshold = 0

# Run the BRO algorithm
best_individual, best_fitness = bro_algorithm()

# Convert binary representation to a list of selected indices
selected_indices = [i for i, bit in enumerate(best_individual) if bit == 1]

# Print the selected indices and the fitness value
print("Selected Indices:", selected_indices)
print("Best Fitness:", best_fitness)
