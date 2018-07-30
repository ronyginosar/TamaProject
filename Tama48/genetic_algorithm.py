import needs
import state
import random
<<<<<<< HEAD
import building_types as bt
=======
import building_types
import util
>>>>>>> 6afc155f11c541c8fd4d2d5d90c83d66ae00b69b

# TODO: Naama: Should it be a user value and it it only temporarily as a magic number??
MUTATION_PROB = 0.03
TYPE = 0
BUILDINGS = 1


"""
creates a random state
"""
# TODO rony: does min_conf need it??
# TODO: Naama: I don't understand what is the reason for that here. please talk to me- I'll implement it inside state!!
def get_additional_public_floors(buildings_data, additional_floors, all_needs):
    return 1

# TODO: TO CHECK IMPLEMENTATION, Naama: some comments!
def generate_random_state(buildings_data, add_housing_units, all_needs_dict):  # TODO rony: does min_conf need it??
    additional_floors_resd = []

    residential_buildings = bt.find_buildings_in_type(bt.RESIDENTIAL, buildings_data)

    # an array of division indexes to divide the housing units between the residential(?) buildings
    random_division = []
    for i in range(len(residential_buildings)):
        random_division.append(random.randint(0, add_housing_units))
    sorted(random_division)

    prev_apartments = 0
    for i in range(len(residential_buildings)):
        num_units = random_division[i] - prev_apartments
        prev_apartments = random_division[i]
        floor_size = residential_buildings[i].get_area()
        needed_area = needs.METERS_PER_UNIT*num_units
        floors_to_add = int(needed_area/floor_size)
        additional_floors_resd.append(floors_to_add)

    # because we add each time only the integer number of floors, we might end up with less housing units than
    # we need, so here we cover for that
    units_added = util.get_units_added(residential_buildings, additional_floors_resd)
    if units_added < add_housing_units:
        # TODO: Naama: are you sure you want to assign additional_floors_resd again? but I didn't follow it actually..
        additional_floors_resd = add_units(units_added, residential_buildings, additional_floors_resd, add_housing_units)

    new_state = state.State(buildings_data, additional_floors_resd, all_needs_dict)
    # TODO: Naama: do not assign additional_public_floors, it will be during the calculation of the state's score.
    # TODO: Naama: if you need this value please use: new_state.calc_public_state()
    #    additional_public_floors = get_additional_public_floors(buildings_data, additional_floors, all_needs)
    #new_state = state.State(buildings_data, additional_floors, additional_public_floors, all_needs)

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
    pass


"""
"""
# TODO: TO CHECK IMPLEMENTATION
def reduce_units(units_added, residential_buildings, additional_floors, add_housing_unit):
    new_add_floors = additional_floors

    # adds floors at random buildings, so that we will meet the housing units requirements
    while units_added > add_housing_unit:
        building_to_shrink = random.randint(len(residential_buildings) - 1)
        if new_add_floors[building_to_shrink] > 0:
            new_add_floors[building_to_shrink] -= 1
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
def merge(pair, add_housing_unit, all_needs, residential_buildings):
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
    units_added = util.get_units_added(additional_floors)

    # because we randomly combine the different states, we might end up with more or less housing units than
    # we need, so here we cover for that
    units_added = util.get_units_added(additional_floors, add_housing_unit)

    if units_added > add_housing_unit:
        additional_floors = reduce_units(units_added, residential_buildings, additional_floors, add_housing_unit)
    if units_added < add_housing_unit:
        additional_floors = add_units(units_added, residential_buildings, additional_floors, add_housing_unit)

    new_state = state.State(buildings_data, additional_floors, get_additional_public_floors(buildings_data, additional_floors, all_needs))

    return new_state

"""
"""
# TODO: TO CHECK IMPLEMENTATION
def get_pair(elite):
    first, second = elite[random.randint(0,len(elite)-1)]
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
        new_individual = merge(get_pair(elite), add_housing_unit, all_needs, residential_buildings)
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

    best_state = get_best_state(population)
    return 0
    # return best_state.get_heights_to_add()