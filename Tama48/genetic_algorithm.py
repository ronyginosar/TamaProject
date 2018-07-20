import evaluate_plan
import needs
import random

MUTATION_PROB = 0.03

# creates a random state
def get_random_state(buildings_data, add_housing_unit, all_needs):
    pass #TODO implement

# generates the first set of states
def generate_random_population(pop_size, buildings_data, add_housing_unit, all_needs):
    population = []
    for i in range(pop_size):
        population.append(get_random_state(buildings_data, add_housing_unit, all_needs))
    return population


# selects the top 25% of states, according to their score
def get_top_individuals(population):
    pass #TODO implement

# returns all the possible pairs within a group
def get_pairs(elite):
    pass #TODO implement

# creates a random merge of a pair
def merge(pair):
    pass #TODO implement

# creates a new set of states, by reproducing the top states in the population
def reproduce(population, buildings_data, add_housing_unit, all_needs):
    new_pop = []
    elite = get_top_individuals(population)
    pairs = get_pairs(elite)
    next_pair_idx = 0
    while (len(new_pop) < len(population)):
        new_individual = merge(pairs[next_pair_idx])
        if (random.random() < MUTATION_PROB):
            new_individual = get_random_state(buildings_data, add_housing_unit, all_needs)
        next_pair_idx = (next_pair_idx + 1)%len(pairs)
        new_pop.append(new_individual)
    return new_pop

# returns the best state of a group
def get_best_state(population):
    pass #TODO implement



################################################################

# the main algorithm structure
def find_solution(buildings_data, add_housing_unit, k=16, num_iterations=20):
    our_needs = needs.Needs(buildings_data, add_housing_unit)
    all_needs = our_needs.calc_all_needs()

    population = generate_random_population(k, buildings_data, add_housing_unit, all_needs)

    for it in range(num_iterations):
        reproduce(population, buildings_data, add_housing_unit, all_needs)

    best_state = get_best_state(population)


    return best_state.get_heights_to_add()