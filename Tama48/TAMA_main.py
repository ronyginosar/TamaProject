"""
Created on July 2, 2018

@author: Naama
"""

import extract_GIS_data as ext_data
import genetic_algorithm
import min_conflict_algorithm
import needs
import copy
import random # for Rony


def generate_random_result_for_Rony(init_building_data):
    updated_random_building_data_for_rony = copy.deepcopy(init_building_data)

    for tuple in updated_random_building_data_for_rony:
        # b_type = tuple[0]
        for building in tuple[1]:
            if random.randint(0, 1) != 0:
                building.set_extra_height(random.randint(1,10))

    return updated_random_building_data_for_rony

if __name__ == '__main__':


    # dir_path = '..\\..\\data'
    # buildings_data - List < (string, List < Building>>, string:building_type
    init_building_data = ext_data.read_files()

    # updated_random_building_data_for_rony = generate_random_result_for_Rony(init_building_data)

    is_genetic = 1
    add_housing_units = 300

    # calculate needs
    all_needs_dict = needs.calc_needs(init_building_data, add_housing_units)

    # additional_heights = []
    # building_residential = []
    if is_genetic:
        (iter_score, lst_extra_heights) = genetic_algorithm.genetic_solution(init_building_data, all_needs_dict, add_housing_units)
    else:
        (iter_score, lst_extra_heights) = min_conflict_algorithm.min_conflict_solution(init_building_data, all_needs_dict, add_housing_units)
        # simulated_annealing.find_solution(buildings_data, add_housing_unit)
