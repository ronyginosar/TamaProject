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
    add_housing_unit = 100

    # calculate needs
    additional_heights = []
    building_types = [building[0] for building in buildings_data]
    building_residential = []
    all_needs = needs.Needs(buildings_data, add_housing_unit)

    if is_genetic:
        new_plan = genetic_algorithm.genetic_solution(buildings_data, all_needs)
    else:
        new_plan = min_conflict_algorithm.min_conflict_solution(buildings_data, all_needs)
        # new_plan = simulated_annealing.find_solution(buildings_data, add_housing_unit)