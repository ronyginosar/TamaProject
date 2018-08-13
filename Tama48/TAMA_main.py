"""
Created on July 2, 2018

@author: Naama
"""

import extract_GIS_data as ext_data
import building_types as bt
import util
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

def link_public_private_buildings(building_data):
    for resd_building in bt.find_buildings_in_type(bt.RESIDENTIAL, building_data):
        for type in bt.all_public_building_types():
            public_buildings_in_type = bt.find_buildings_in_type(type, building_data)

            dist_lst = [(public_in_type, util.calc_distance_two_buildings(resd_building, public_in_type))
                     for public_in_type in public_buildings_in_type]
            dist_lst_sorted = sorted(dist_lst, key=lambda x: x[1])
            # closest public, take the first argument of the tuple (building, dist)
            closest_public = dist_lst_sorted[0][0]

            # link residential to public
            closest_public.add_user_buildings(resd_building)
            # link public to residential
            resd_building.add_used_public_building(closest_public)

    return building_data

if __name__ == '__main__':


    # dir_path = '..\\..\\data'
    # buildings_data - List < (string, List < Building>>, string:building_type
    init_building_data = ext_data.read_files()

    # updated_random_building_data_for_rony = generate_random_result_for_Rony(init_building_data)

    link_public_private_buildings(init_building_data)

    is_genetic = 1
    #add_housing_units =0
    add_housing_units = 100

    # calculate needs
    all_needs_dict = needs.calc_needs(init_building_data, add_housing_units)

    # additional_heights = []
    # building_residential = []
    if is_genetic:
        (iter_score, updated_building_data) = genetic_algorithm.genetic_solution(init_building_data, all_needs_dict, add_housing_units)
    else:
        (iter_score, updated_building_data) = min_conflict_algorithm.min_conflict_solution(init_building_data, all_needs_dict, add_housing_units)
        # simulated_annealing.find_solution(buildings_data, add_housing_unit)
        #new_state = min_conflict_algorithm.min_conflict_solution(init_building_data, all_needs_dict, add_housing_units)
        # new_plan = simulated_annealing.find_solution(buildings_data, add_housing_unit)
    print('the end!')
    print('score = ' + str(iter_score))
    #print(updated_building_data.get_heights_to_add())
