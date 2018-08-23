import needs
import state
import random
import building_types as bt
import util
import math

#MUTATION_PROB = 0.1
TYPE = 0
BUILDINGS = 1


def generate_random_state(buildings_data, add_housing_units, all_needs_dict):

    residential_buildings = bt.find_buildings_in_type(bt.RESIDENTIAL, buildings_data)

    added_floors_resd = [0]*len(residential_buildings)
    units_added = 0

    while units_added < add_housing_units:
        building_to_rise = random.randint(0, len(residential_buildings)-1)
        added_floors_resd[building_to_rise] += 1
        units_added += util.get_units_added_to_one_building(residential_buildings[building_to_rise], 1)

    new_state = state.State(buildings_data, added_floors_resd, all_needs_dict)

    return new_state

# generates the first set of states
def generate_random_population(pop_size, buildings_data, add_housing_unit, all_needs):
    population = []
    for i in range(pop_size):
        population.append(generate_random_state(buildings_data, add_housing_unit, all_needs))
    return population


"""
selects the top 25% of states, according to their score
"""
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


def calibrate_num_units(units_added, residential_buildings, additional_floors, add_housing_unit, comparator,
                        max_min_floor_value):

    untouched_buildings = set()
    for i in range(len(max_min_floor_value)):
        untouched_buildings.add(i)

    while comparator(add_housing_unit, units_added):
        building_to_manipulate = untouched_buildings.pop()
        additional_floors[building_to_manipulate] = max_min_floor_value[building_to_manipulate]
        units_added += int(residential_buildings[building_to_manipulate].get_area()/needs.METERS_PER_UNIT)
    return


def merge_elite(pair, add_housing_unit, all_needs, residential_buildings):
    parent1 = pair[0]
    parent2 = pair[1]
    buildings_data = parent1.get_building_data()
    parent2_heights = parent2.get_heights_to_add()
    additional_floors = parent1.get_heights_to_add()

    # the max value between parent_1 and parent_2
    max_floor_value = [0]*len(additional_floors)
    # the min value between parent_1 and parent_2
    min_floor_value = [0]*len(additional_floors)

    for i in range(len(additional_floors)):

        max_floor_value[i] = max(additional_floors[i], parent2_heights[i])
        min_floor_value[i] = min(additional_floors[i], parent2_heights[i])

        if random.random() > 0.5:
            additional_floors[i] = parent2_heights[i]
    # when merging, we need to make sure that the additional housing units is as required
    units_added = util.get_units_added(residential_buildings, additional_floors)

    # because we randomly combine the different states, we might end up with more or less housing units than
    # we need, so here we cover for that
    if units_added < add_housing_unit:
        comparator = lambda x,y: x < y
        calibrate_num_units(units_added, residential_buildings, additional_floors, add_housing_unit, comparator, max_floor_value)
    if units_added > add_housing_unit:
        comparator = lambda x,y: x > y
        calibrate_num_units(units_added, residential_buildings, additional_floors, add_housing_unit, comparator, min_floor_value)
    new_state = state.State(buildings_data, additional_floors, all_needs)

    return new_state


def get_pair(elite):
    first = elite[random.randint(0,len(elite)-1)]
    second = elite[random.randint(0,len(elite)-1)]
    while first == second:
        second = elite[random.randint(0,len(elite)-1)]
    return (first, second)


def reproduce(population, buildings_data, add_housing_unit, all_needs, mutatio_prob):
    residential_buildings = bt.find_buildings_in_type(bt.RESIDENTIAL, buildings_data)
    elite = get_top_individuals(population)
    new_pop = elite
    while (len(new_pop) < len(population)*4):
        random_val = random.random()
        if (random_val < mutatio_prob):
            new_individual = generate_random_state(buildings_data, add_housing_unit, all_needs)
        else:
            new_individual = merge_elite(get_pair(elite), add_housing_unit, all_needs, residential_buildings)
        new_pop.append(new_individual)
    new_pop = get_top_individuals(new_pop)
    return new_pop


def get_best_state(population):
    best_state = population[0]
    for individual in population:
        if individual.get_score() > best_state.get_score():
            best_state = individual
    return best_state


################################################################

def write_to_file(file, idx, iter_score, lst_extra_heights):
    file.write(str(idx) + "\t")
    file.write(str(iter_score)+"\t")
    for item in lst_extra_heights:
        file.write(str(item) + "\t")
    file.write("\n")

"""
the main algorithm structure

@:param buildings_data- List<(string, List<Building>> string:building_type (from building_types.py file)
@:param all_needs_dict- dict<string, int>, string:building_type, int:num_of_units
@:param add_housing_units- int:(user request) num of units to add
@:param k- int:num of children in each iterations??
@:param num_iterations- int: not of iteration of the algorithm.
"""
def genetic_solution(buildings_data, all_needs_dict, add_housing_units , k, num_iterations, mutatio_prob , folder_type):
    population = generate_random_population(k, buildings_data, add_housing_units, all_needs_dict)

    idx = 1
    try_name = str(add_housing_units) + "units" + str(k)+"k" + str(num_iterations) + "iters" + str(mutatio_prob) + "mut-prob"
    result_file_path = '../results/' + folder_type + '/' + try_name + ".txt" # ToAdd: time_folder + "/"
    file = open(result_file_path, "w")
    file.write("iter-idx\titer-score\t")
    for building_in_type in buildings_data:
        for building in building_in_type[1]:
            file.write(str(building) + "\t")
    file.write("\n")
    all_iter_state_results = []

    for it in range(num_iterations):
        new_population = reproduce(population, buildings_data, add_housing_units, all_needs_dict, mutatio_prob)
        iter_state_result = get_best_state(new_population)
        iter_score = iter_state_result.get_score()

        all_iter_state_results.append((iter_score, iter_state_result))

        lst_extra_heights = iter_state_result.get_only_floor_lst()
        file.write(str(idx) + "\t" + str(iter_score) + "\t")
        for item in lst_extra_heights:
            file.write(str(item) + "\t")
        file.write("\n")

        population = new_population
        idx += 1
        print('iteration ' + str(it) + ', score: ' + str(iter_score))
    file.close()

    best_iter = sorted(all_iter_state_results, key=lambda x: x[0])[::-1][0]
    updated_building_data = best_iter[1].get_updated_building_data()

    return (best_iter[0], updated_building_data)
