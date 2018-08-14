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
import random
import datetime
import json


def convert_to_json_and_save(state):
    state_dict = {}
    for i in range(len(state)):
        buildings_list = []
        for j in range(len(state[i][1])):
            curr_building = state[i][1][j]
            buildings_list.append([{
                'building': {
                    'id': curr_building.get_id(),
                    'area': curr_building.get_area(),
                    'location': curr_building.get_location(),
                    'polygon': curr_building.get_polygon(),
                    'init_height': curr_building.get_init_height(),
                    'extra_height': curr_building.get_extra_height(),
                }
            }])

        state_dict[state[i][0]] = buildings_list
    with open('data.json', 'w') as outfile:
        json.dump(state_dict, outfile)


# def generate_random_result_for_Rony(init_building_data):
#     updated_random_building_data_for_rony = copy.deepcopy(init_building_data)
#
#     for tuple in updated_random_building_data_for_rony:
#         # b_type = tuple[0]
#         for building in tuple[1]:
#             if random.randint(0, 1) != 0:
#                 building.set_extra_height(random.randint(1,10))
#     return updated_random_building_data_for_rony

def link_public_private_buildings(building_data):
    for resd_building in bt.find_buildings_in_type(bt.RESIDENTIAL, building_data):
        for type in bt.ALL_PUBLIC_BUILDING_TYPES:
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
    #time_folder = '{:%Y-%m-%d_%H-%M-%S}'.format(datetime.datetime.now())
    folder_types = ["only_cost", "only_distance", "only_needs"]

    add_units_lst = [10000] #, 1000]
    k_lst = [16] #, 40]
    iters_lst = [30] #, 25]
    mut_prob_lst = [0.3] #, 0.03]
    is_genetic = 1
    time_folder = '{:%Y-%m-%d_%H-%M-%S}'.format(datetime.datetime.now())

    add_units_lst = [10] #, 1000]
    k_lst = [16] #, 40]
    iters_lst = [30] #, 20]
    mut_prob_lst = [0.05]#, 0.1]

    if is_genetic:
        for add_housing_units in add_units_lst:
            # calculate needs
            all_needs_dict = needs.calc_needs(init_building_data, add_housing_units)
            for k in k_lst:
                for iters in iters_lst:
                    for mut_prob in mut_prob_lst:
                        (iter_score, updated_building_data) =\
                            genetic_algorithm.genetic_solution(init_building_data, all_needs_dict, add_housing_units,
                                                                   k, iters, mut_prob, "5needs_4dist_1cost-new_public")
    else:
        all_needs_dict = needs.calc_needs(init_building_data, add_units_lst[0])
        (iter_score, updated_building_data) = min_conflict_algorithm.min_conflict_solution(init_building_data, all_needs_dict, add_units_lst[0])
    print('the end!')
    print('score = ' + str(iter_score))
    #print(updated_building_data.get_heights_to_add())
