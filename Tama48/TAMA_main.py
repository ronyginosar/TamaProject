"""
Created on July 2, 2018

@author: Naama
"""

import extract_GIS_data as ext_data
import genetic_algorithm
import min_conflict_algorithm
import needs

if __name__ == '__main__':

    dir_path = '..\\data'
    buildings_data = ext_data.read_files(dir_path)

    is_genetic = 1
    add_area = 1000
    original_area = 0
    for building_item in buildings_data:
        if building_item[0]  == 'residential':
            for building in building_item[1]:
                original_area += building.area

    print(buildings_data.shape)

    # calculate needs
    additional_heights = []
    building_residential = []
    all_needs = needs.Needs(original_area, buildings_data. add_area)

    if is_genetic:
        new_plan = genetic_algorithm.find_solution(buildings_data, all_needs)
    else:
        new_plan = min_conflict_algorithm.min_conflict_solution(buildings_data, all_needs)
        # new_plan = simulated_annealing.find_solution(buildings_data, add_housing_unit)
