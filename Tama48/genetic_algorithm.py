import needs
import state
import random
import building_types as bt
import building_types
import util
import math

# TODO: Naama: Should it be a user value and it it only temporarily as a magic number??
MUTATION_PROB = 0.03
TYPE = 0
BUILDINGS = 1


# """
# creates a random state
# """
# # TODO rony: does min_conf need it??
# # TODO: Naama: I don't understand what is the reason for that here. please talk to me- I'll implement it inside state!!
# def get_additional_public_floors(buildings_data, additional_floors, all_needs):
#     return 1

def generate_random_state(buildings_data, add_housing_units, all_needs_dict):  # TODO rony: does min_conf need it??

    residential_buildings = bt.find_buildings_in_type(bt.RESIDENTIAL, buildings_data)

    added_floors_resd = [0]*len(residential_buildings)
    units_added = 0

    while units_added < add_housing_units:
        building_to_rise = random.randint(0, add_housing_units)
        added_floors_resd[building_to_rise] += 1
        units_added += util.get_units_added_to_one_building(residential_buildings[building_to_rise], 1)

    new_state = state.State(buildings_data, added_floors_resd, all_needs_dict)

    return new_state

# generates the first set of states
# TODO: TO CHECK IMPLEMENTATION
def generate_random_population(pop_size, buildings_data, add_housing_unit, all_needs):
    population = []
    for i in range(pop_size):
        population.append(generate_random_state(buildings_data, add_housing_unit, all_needs))
    return population

"""
selects the top 25% of states, according to their score
"""
#TODO: to implement. don't forget to return at least 2 individuals
def get_top_individuals(population):
    scores = []
    top_individuals = []
    for individual in population:
        scores.append((individual.get_score(), individual))
    scores = sorted(scores, key=lambda score: score[0])
    scores = scores[::-1]

    for i in range(math.ceil(len(population)/4)):
        top_individuals.append(scores[i][1])

    return top_individuals



"""
"""
# TODO: TO CHECK IMPLEMENTATION
def reduce_units(units_added, residential_buildings, additional_floors, add_housing_unit):
    new_add_floors = additional_floors
    raised_buildings = set()
    for i in range(len(new_add_floors)):
        if new_add_floors[i] > 0:
            raised_buildings.add(i)

    # adds floors at random buildings, so that we will meet the housing units requirements
    while units_added > add_housing_unit:
        building_to_shrink = random.sample(raised_buildings, 1)[0]
        new_add_floors[building_to_shrink] -= 1

        if new_add_floors[building_to_shrink] == 0:
            raised_buildings.remove(building_to_shrink)

        units_added -= int(residential_buildings[building_to_shrink].get_area()/needs.METERS_PER_UNIT)

    return new_add_floors

"""
"""
# TODO: TO CHECK IMPLEMENTATION
def add_units(units_added, residential_buildings, additional_floors, add_housing_unit):
    new_add_floors = additional_floors

    # adds floors at random buildings, so that we will meet the housing units requirements
    while units_added < add_housing_unit:
        building_to_enlarge = random.randint(0, len(residential_buildings) - 1)
        new_add_floors[building_to_enlarge] += 1
        units_added += int(residential_buildings[building_to_enlarge].get_area()/needs.METERS_PER_UNIT)

    return new_add_floors

"""
"""
# TODO: TO CHECK IMPLEMENTATION
def merge_elite(pair, add_housing_unit, all_needs, residential_buildings):
    parent1 = pair[0]
    parent2 = pair[1]
    buildings_data = parent1.get_building_data()

    parent2_heights = parent2.get_heights_to_add()

    additional_floors = parent1.get_heights_to_add()
    for i in range(len(additional_floors)):
        #why 0.5??
        if random.random() > 0.5:
            additional_floors[i] = parent2_heights[i]
    # when merging, we need to make sure that the additional housing units is as required
    units_added = util.get_units_added(residential_buildings, additional_floors)

    # because we randomly combine the different states, we might end up with more or less housing units than
    # we need, so here we cover for that
    # units_added = util.get_units_added(additional_floors, add_housing_unit)

    if units_added > add_housing_unit:
        additional_floors = reduce_units(units_added, residential_buildings, additional_floors, add_housing_unit)
    if units_added < add_housing_unit:
        additional_floors = add_units(units_added, residential_buildings, additional_floors, add_housing_unit)
    # get_additional_public_floors(buildings_data, additional_floors, all_needs)
    new_state = state.State(buildings_data, additional_floors, all_needs)

    return new_state

"""
"""
# TODO: TO CHECK IMPLEMENTATION
def get_pair(elite):
    first = elite[random.randint(0,len(elite)-1)]
    second = elite[random.randint(0,len(elite)-1)]
    while first == second:
        second = elite[random.randint(0,len(elite)-1)]
    return (first, second)


"""
creates a new set of states, by reproducing the top states in the population
"""
# TODO: TO CHECK IMPLEMENTATION
def reproduce(population, buildings_data, add_housing_unit, all_needs):
    new_pop = []
    residential_buildings = bt.find_buildings_in_type(bt.RESIDENTIAL, buildings_data)
    elite = get_top_individuals(population)
    while (len(new_pop) < len(population)):
        new_individual = merge_elite(get_pair(elite), add_housing_unit, all_needs, residential_buildings)
        if (random.random() < MUTATION_PROB):
            new_individual = generate_random_state(buildings_data, add_housing_unit, all_needs)
        new_pop.append(new_individual)
    return new_pop


"""
returns the best state of a group of states
"""
# TODO: TO CHECK IMPLEMENTATION
def get_best_state(population):
    best_state = population[0]
    for individual in population:
        if individual.get_score() > best_state.get_score():
            best_state = individual
    return best_state


################################################################

"""
the main algorithm structure

@:param buildings_data- List<(string, List<Building>> string:building_type (from building_types.py file)
@:param all_needs_dict- dict<string, int>, string:building_type, int:num_of_units
@:param add_housing_units- int:(user request) num of units to add
@:param k- int:num of children in each iterations??
@:param num_iterations- int: not of iteration of the algorithm.
"""
# TODO: TO CHECK IMPLEMENTATION
def genetic_solution(buildings_data, all_needs_dict, add_housing_units, k=16, num_iterations=20):

    population = generate_random_population(k, buildings_data, add_housing_units, all_needs_dict)

    for it in range(num_iterations):
        reproduce(population, buildings_data, add_housing_units, all_needs_dict)

    return get_best_state(population)
