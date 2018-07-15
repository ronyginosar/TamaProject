import extract_GIS_data as ext_data
import genetic_algorithm
import simulated_annealing


if __name__ == '__main__':

    dir_path = 'C:\\Users\\Naama\\Documents\\Academy\\Courses\\AI\\Tama48\\all_building_files';
    buildings_data = ext_data.read_files(dir_path)

    is_genetic = 1
    additional_population = 100

    if is_genetic:
        new_plan = genetic_algorithm.find_solution(buildings_data, additional_population)
    else:
        new_plan = simulated_annealing.find_solution(buildings_data, additional_population)