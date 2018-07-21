import evaluate_plan
import needs
import random

MUTATION_PROB = 0.03

TYPE = 0
BUILDINGS = 1

# creates a random state
def generate_random_state(buildings_data, add_housing_unit, all_needs):
    residential_buildings = []
    additional_floors = []
    units_added = 0

    for type in buildings_data:
        if type[TYPE] == 'residential':
            residential_buildings = buildings_data[TYPE][BUILDINGS]

    # an array of division indexes to divide the housing units between the buildings
    random_division = []
    for i in range(len(residential_buildings)):
        random_division.append(random.randint(add_housing_unit))
    sorted(random_division)

    prev_apartments = 0
    for i in range(len(residential_buildings)):
        num_units = random_division[i] - prev_apartments
        prev_apartments = random_division[i]
        floor_size = residential_buildings[i].get_area()
        needed_area = needs.METERS_PER_UNIT*num_units
        floors_to_add = int(needed_area/floor_size)
        additional_floors.append(floors_to_add)
        units_added += int(floors_to_add*floor_size/needs.METERS_PER_UNIT)

    # adds floors at random buildings, so that we will meet the housing units requirements 
    while units_added < add_housing_unit:
        building_to_enlarge = random.randint(len(residential_buildings) - 1)
        additional_floors[building_to_enlarge] += 1
        units_added += int(residential_buildings[building_to_enlarge].get_area()/needs.METERS_PER_UNIT)

    return additional_floors


# generates the first set of states
def generate_random_population(pop_size, buildings_data, add_housing_unit, all_needs):
    population = []
    for i in range(pop_size):
        population.append(generate_random_state(buildings_data, add_housing_unit, all_needs))
    return population


# selects the top 25% of states, according to their score
def get_top_individuals(population):
    pass #TODO implement


# creates a random merge of a pair
def merge(pair):
    pass #TODO implement


def get_pair(elite):
    first, second = elite[random.randint(0,len(elite)-1)]
    while first == second:
        second = elite[random.randint(0,len(elite)-1)]
    return (first, second)

# creates a new set of states, by reproducing the top states in the population
def reproduce(population, buildings_data, add_housing_unit, all_needs):
    new_pop = []
    elite = get_top_individuals(population)
    while (len(new_pop) < len(population)):
        new_individual = merge(get_pair(elite))
        if (random.random() < MUTATION_PROB):
            new_individual = generate_random_state(buildings_data, add_housing_unit, all_needs)
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