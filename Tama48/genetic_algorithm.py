import evaluate_plan
import needs
import state
import random

MUTATION_PROB = 0.03

TYPE = 0
BUILDINGS = 1

# creates a random state
def get_additional_public_floors(buildings_data, additional_floors, all_needs):
    pass #TODO implement


def generate_random_state(buildings_data, add_housing_unit, all_needs):
    residential_buildings = []
    additional_floors = []

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

    units_added = get_units_added(residential_buildings, additional_floors)
    if units_added < add_housing_unit:
        additional_floors = add_units(units_added, residential_buildings, additional_floors, add_housing_unit)

    new_state = state.State(buildings_data, additional_floors, get_additional_public_floors(buildings_data, additional_floors, all_needs))

    return new_state


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
def get_units_added(residential_buildings, additional_floors):
    units_added = 0
    for i in range(len(residential_buildings)):
        units_added += int(additional_floors[i]*residential_buildings[i].get_area()/needs.METERS_PER_UNIT)
    return units_added


def reduce_units(units_added, residential_buildings, additional_floors, add_housing_unit):
    new_add_floors = additional_floors

    # adds floors at random buildings, so that we will meet the housing units requirements
    while units_added > add_housing_unit:
        building_to_shrink = random.randint(len(residential_buildings) - 1)
        if new_add_floors[building_to_shrink] > 0:
            new_add_floors[building_to_shrink] -= 1
            units_added -= int(residential_buildings[building_to_shrink].get_area()/needs.METERS_PER_UNIT)

    return new_add_floors


def add_units(units_added, residential_buildings, additional_floors, add_housing_unit):
    new_add_floors = additional_floors

    # adds floors at random buildings, so that we will meet the housing units requirements
    while units_added < add_housing_unit:
        building_to_enlarge = random.randint(len(residential_buildings) - 1)
        new_add_floors[building_to_enlarge] += 1
        units_added += int(residential_buildings[building_to_enlarge].get_area()/needs.METERS_PER_UNIT)

    return new_add_floors

def merge(pair, add_housing_unit, all_needs):
    parent1 = pair[0]
    parent2 = pair[1]
    buildings_data = parent1.get_building_data()

    parent2_heights = parent2.get_heights_to_add()

    additional_floors = parent1.get_heights_to_add()
    for i in range(len(additional_floors)):
        if random.random() > 0.5:
            additional_floors[i] = parent2_heights[i]

    units_added = get_units_added(additional_floors)
    if units_added > add_housing_unit:
        additional_floors = reduce_units(additional_floors, add_housing_unit)
    if units_added < add_housing_unit:
        additional_floors = add_units(additional_floors, add_housing_unit)

    new_state = state.State(buildings_data, additional_floors, get_additional_public_floors(buildings_data, additional_floors, all_needs))

    return new_state


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
        new_individual = merge(get_pair(elite), add_housing_unit, all_needs)
        if (random.random() < MUTATION_PROB):
            new_individual = generate_random_state(buildings_data, add_housing_unit, all_needs)
        new_pop.append(new_individual)
    return new_pop


# returns the best state of a group of states
def get_best_state(population):
    best_state = population[0]
    for individual in population:
        if individual.get_score() > best_state.get_score():
            best_state = individual
    return best_state



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