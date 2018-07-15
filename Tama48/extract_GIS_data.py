from building import Building
import os
from os import listdir
from os.path import isfile, join
from os.path import basename


def read_files(buildings_fullpath = 'C:\\Users\\Naama\\Documents\\Academy\\Courses\\AI\\Tama48\\all_building_files'):
    prev_id = 0
    buildings_data = []

    type_idx = 0
    all_types_dirs = [x[1] for x in os.walk(buildings_fullpath)][0]
    for subdir in all_types_dirs:
        location_lst = []
        height_lst = []
        area_lst = []
        all_building_onetype = []

        buildings_dirpath = os.path.join(buildings_fullpath, subdir)
        type_idx += 1

        onlyfiles = [f for f in listdir(buildings_dirpath) if isfile(join(buildings_dirpath, f))]
        if not onlyfiles:
            continue
        num_of_buildings = 0
        for file in onlyfiles:
            file_full_path = join(buildings_dirpath, file)
            f = open(file_full_path, 'r')
            lines = f.readlines()
            f.close()
            num_of_lines = len(lines)

            file_name = os.path.splitext(basename(file))[0]
            if file_name == 'height':
                lines_cor = lines[1:num_of_lines]
                for line in lines_cor:
                    height_lst.append(float(line.split('.')[0]+'.' + line.split('.')[1][0:-2]))

            elif file_name == 'area':
                lines_cor = lines[1:num_of_lines]
                for line in lines_cor:
                    area_lst.append(float(line.split('.')[0] + '.' + line.split('.')[1][0:-2]))
                # for line in it_lines:
                #     data = line.split('.')[0] + '.' + line.split('.')[1]
                #     float_data = [s for s in ff.split() if s.isdigit()]
                #     str_data = data + float_data[0]
                #     val_data = float(str_data)
            elif file_name == 'location': # triple values?
                lines_cor = lines[1:num_of_lines]
                for line in lines_cor:
                    [x, y, alt] = line.split(', ')
                    x = x[1:len(x)]
                    alt = float(alt.split('.')[0] + '.' + alt.split('.')[1][0:-3])
                    location_lst.append((float(x), float(y), float(alt)))

        for idx in range(num_of_lines-1):
            # (building_id, building_type, area, location, init_height)
            building = Building(prev_id + idx, subdir, area_lst[idx], location_lst[idx], height_lst[idx])
            all_building_onetype.append(building)
        buildings_data.append((subdir, all_building_onetype))
        prev_id = prev_id + num_of_lines-1

    return buildings_data

# def create_files():
#     dist_building_data = create_csp_files()
#
#     domain_str = "propositions: ["
#     problem_str = "init_state: ["
#
#     for building in dist_building_data:
#          problem_str += str(building) + " "
#     problem_str += "]\n"
#
#     list_of_volumes = [ for (id, building) in dist_building_data]
#
#     return
