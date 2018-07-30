"""
Created on July 2, 2018

@author: Naama
"""

import extract_GIS_data as ext_data
import genetic_algorithm
import min_conflict_algorithm
import needs

if __name__ == '__main__':


    # dir_path = '..\\..\\data'
    # buildings_data - List < (string, List < Building >>, string:building_type
    buildings_data = ext_data.read_files()

    is_genetic = 1
    add_housing_units = 100

    # calculate needs
    all_needs_dict = needs.calc_needs(buildings_data, add_housing_units)

    # additional_heights = []
    # building_residential = []
    if is_genetic:
        new_plan = genetic_algorithm.genetic_solution(buildings_data, all_needs_dict, add_housing_units)
    else:
        new_plan = min_conflict_algorithm.min_conflict_solution(buildings_data, all_needs_dict, add_housing_units)
        # new_plan = simulated_annealing.find_solution(buildings_data, add_housing_unit)
