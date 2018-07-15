import extract_GIS_data as ext_data
import genetic_algorithm
import simulated_annealing


if __name__ == '__main__':

    dir_path = '..\\data'
    buildings_data = ext_data.read_files(dir_path)

    is_genetic = 1
    add_housing_unit = 100

    if is_genetic:
        new_plan = genetic_algorithm.find_solution(buildings_data, add_housing_unit)
    else:
        new_plan = simulated_annealing.find_solution(buildings_data, add_housing_unit)