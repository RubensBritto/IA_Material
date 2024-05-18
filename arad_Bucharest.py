import random

# New Romania map format
romania_map = {
    'Arad': {'Zerind': 75, 'Sibiu': 140, 'Timisoara': 118},
    'Zerind': {'Arad': 75, 'Oradea': 71},
    'Oradea': {'Zerind': 71, 'Sibiu': 151},
    'Sibiu': {'Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'Rimnicu Vilcea': 80},
    'Timisoara': {'Arad': 118, 'Lugoj': 111},
    'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
    'Mehadia': {'Lugoj': 70, 'Drobeta': 75},
    'Drobeta': {'Mehadia': 75, 'Craiova': 120},
    'Craiova': {'Drobeta': 120, 'Rimnicu Vilcea': 146, 'Pitesti': 138},
    'Rimnicu Vilcea': {'Sibiu': 80, 'Craiova': 146, 'Pitesti': 97},
    'Fagaras': {'Sibiu': 99, 'Bucharest': 211},
    'Pitesti': {'Rimnicu Vilcea': 97, 'Craiova': 138, 'Bucharest': 101},
    'Bucharest': {'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85},
    'Giurgiu': {'Bucharest': 90},
    'Urziceni': {'Bucharest': 85, 'Vaslui': 142, 'Hirsova': 98},
    'Vaslui': {'Urziceni': 142, 'Iasi': 92},
    'Iasi': {'Vaslui': 92, 'Neamt': 87},
    'Neamt': {'Iasi': 87},
    'Hirsova': {'Urziceni': 98, 'Eforie': 86},
    'Eforie': {'Hirsova': 86}
}

def get_distance(path):
    distance = 0
    i = 0
    while i < len(path) - 1:
        current_city = path[i]
        next_city = path[i + 1]
        if current_city in romania_map and next_city in romania_map[current_city]:
            distance += romania_map[current_city][next_city]
            i += 1
        else:
            # Remove the monster element of the chromosome list
            del path[i + 1]
    return distance

def generate_random_path(start, goal):
    path = [start]
    while path[-1] != goal:
        current_city = path[-1]
        neighbors = [neighbor for neighbor in romania_map[current_city] if neighbor not in path]
        if not neighbors:
            return generate_random_path(start, goal)
        next_city = random.choice(neighbors)
        path.append(next_city)
    return path

def generate_initial_population(size, start, goal):
    return [generate_random_path(start, goal) for _ in range(size)]

def fitness(path):
    return 1 / get_distance(path)

def select_parents(population, fitnesses):
    total_fitness = sum(fitnesses)
    selection_probs = [f / total_fitness for f in fitnesses]
    parents = random.choices(population, weights=selection_probs, k=2)
    return parents

def crossover(parent1, parent2):
    min_length = min(len(parent1), len(parent2))
    if min_length < 3:
        return parent1, parent2

    crossover_point = random.randint(1, min_length - 2)
    child1 = parent1[:crossover_point] + [city for city in parent2 if city not in parent1[:crossover_point]]
    child2 = parent2[:crossover_point] + [city for city in parent1 if city not in parent2[:crossover_point]]
    return child1, child2


def mutate(path, mutation_rate=0.1):
    if len(path) < 3:
        return path

    k = min(len(path) - 1, 2)  
    if k <= 0:
        return path  

    if random.random() < mutation_rate:
        try:
            idx1, idx2 = random.sample(range(1, len(path) - 1), k)
            path[idx1], path[idx2] = path[idx2], path[idx1]
        except ValueError as e:
            print("Error:", e)
            print("Population size:", len(path) - 1)
            print("Desired sample size (k):", k)
            return path

    return path

def eliteSelection(population, fitnesses, elite_size):
    combined = list(zip(population, fitnesses))
    # Sort by fitness in descending order
    combined.sort(key=lambda x: x[1], reverse=True)
    # Extract the elite individuals and their fitness values
    elite_population = [individual for individual, _ in combined[:elite_size]]
    elite_fitnesses = [fitness for _, fitness in combined[:elite_size]]

    return elite_population, elite_fitnesses

def genetic_algorithm(start, goal, population_size=200, generations=10000, mutation_rate=0.1):
    population = generate_initial_population(population_size, start, goal)
    for generation in range(generations):
        fitnesses = [fitness(path) for path in population]
        new_population = []

        for _ in range(population_size // 2):
            parent1, parent2 = select_parents(population, fitnesses)
            child1, child2 = crossover(parent1, parent2)
            new_population.extend([mutate(child1, mutation_rate), mutate(child2, mutation_rate)])
            fitnessesNewpop = [fitness(path) for path in new_population]
            population.extend(new_population)
            fitnesses.extend(fitnessesNewpop)

        population, fitnesses = eliteSelection(population, fitnesses, 200)

        if generation % 10 == 0:
            best_path = max(population, key=get_distance)


    best_path = max(population, key=get_distance)
    best_path = ensure_valid_path(best_path, initial_state, goal_state)
    print(f"Generation {generation}: Best Distance = {get_distance(best_path)}")
    return best_path

def ensure_valid_path(best_path, initial_state, goal_state):
    if initial_state not in best_path:
        best_path.insert(0, initial_state)
    if goal_state not in best_path:
        best_path.append(goal_state)

    valid_cities = set(best_path)
    for city in romania_map.keys():
        if city not in valid_cities:
            idx = best_path.index(goal_state)
            best_path.insert(idx, city)
    return best_path

initial_state = "Arad"
goal_state = "Bucharest"

print(romania_map.keys())

# Run the Genetic Algorithm
best_path = genetic_algorithm(initial_state, goal_state)
print("Best path found:", " --> ".join(best_path))
print("Total distance:", get_distance(best_path), "km")


# Best path found: Arad --> Zerind --> Oradea --> Sibiu --> Rimnicu Vilcea --> Pitesti --> Bucharest
# Total distance: 575 km
