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
import json
import evaluate_personal_satisfaction as eps


def convert_to_json_and_save(state, satisfaction):
    all_buildings_list = []
    for i in range(len(state)):
        for j in range(len(state[i][1])):
            curr_building = (state[i][1])[j]
            all_buildings_list.append({
                    'building':
                        {'id': curr_building.get_id(),
                        'type':curr_building.get_type(),
                        'area': curr_building.get_area(),
                        'location': curr_building.get_location(),
                        'polygon': curr_building.get_polygon(),
                        'init_height': curr_building.get_init_height(),
                        'extra_height': curr_building.get_extra_height()}

            })
    satisfaction_list = []
    for k in range(len(satisfaction)):
        satisfaction_list.append({
            'person':
                {'person_type': satisfaction[k][0],
                'religious': satisfaction[k][1],
                'residence_id': satisfaction[k][2],
                'satisfaction': satisfaction[k][3]}
        })
    final_dict = {}
    final_dict['buildings'] = all_buildings_list
    final_dict['satisfaction_evaluation_results'] = satisfaction_list
    with open('static/data.json', 'w') as outfile:
        json.dump(final_dict, outfile)


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

            # closest_public = dist_lst_sorted[0]
            closest_public= dist_lst_sorted[0][0]
            dist = dist_lst_sorted[0][1]

            # link residential to public
            closest_public.add_user_buildings(resd_building)
            # link public to residential
            resd_building.add_used_public_building(closest_public, dist)

    return building_data

# if __name__ == '__main__':
def makeMyTama(alg,units):  # TODO changed by rony

    print("in MAIN with a " + alg + " algorithm with" ,units , "units") # TODO debugging
    # TODO changed by rony
    # add_units_lst = housingUnitsToAdd
    if alg == 'genetic':
        is_genetic = 1
    elif alg == 'minconflict':
        is_genetic = 0

    init_building_data = ext_data.read_files()

    link_public_private_buildings(init_building_data)

    k = 30
    iters = 30
    mut_prob = 0.3

    if is_genetic:
        all_needs_dict = needs.calc_needs(init_building_data, units)
        (iter_score, updated_building_data) = \
            genetic_algorithm.genetic_solution(init_building_data, all_needs_dict, units,
                                               k, iters, mut_prob, "5needs_4dist_1cost-new_public")
    else:
        print("in MAIN : in minconflict") # TODO debugging
        all_needs_dict = needs.calc_needs(init_building_data, units)
        (iter_score, updated_building_data) = min_conflict_algorithm.min_conflict_solution(init_building_data, all_needs_dict, add_units_lst[0])

    iter_score = round(iter_score,5)
    satisfaction = eps.evaluate_personal_satisfaction(updated_building_data)
    convert_to_json_and_save(updated_building_data, satisfaction)
    print('the end!')
    print('score = ' + str(iter_score))
    return iter_score


# def generate_random_result_for_Rony(init_building_data):
#     updated_random_building_data_for_rony = copy.deepcopy(init_building_data)
#
#     for tuple in updated_random_building_data_for_rony:
#         # b_type = tuple[0]
#         for building in tuple[1]:
#             if random.randint(0, 1) != 0:
#                 building.set_extra_height(random.randint(1,10))
#     return updated_random_building_data_for_rony