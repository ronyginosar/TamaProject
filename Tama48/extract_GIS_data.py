from building import Building
import os
from os import listdir
from os.path import isfile, join
from os.path import basename

HEIGHT = 'height'
AREA = 'area'
LOCATION = 'location'

def read_files(buildings_fullpath = '../data'):
    prev_id = 0
    buildings_data = []

    type_idx = 0

    all_types_dirs = []

    for i in os.listdir(buildings_fullpath):
        if i != '.DS_Store':
            all_types_dirs.append(i)

    if all_types_dirs == []:
        exit() # something went wrong with the directories

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
        #print(subdir)

        for file in onlyfiles:
            if file != '.DS_Store':
                file_full_path = join(buildings_dirpath, file)
                f = open(file_full_path, 'r')
                lines = f.readlines()
                f.close()
                num_of_lines = len(lines)

            file_name = os.path.splitext(basename(file))[0]
            lines_cor = lines[1:num_of_lines]
            if file_name == HEIGHT:
                for line in lines_cor:
                    height_lst.append(float(line.split('.')[0]+'.' + line.split('.')[1][0:-2]))
                #print(HEIGHT + " ")

            elif file_name == AREA:
                for line in lines_cor:
                    area_lst.append(float(line.split('.')[0] + '.' + line.split('.')[1][0:-2]))
                #print(AREA + " ")

            elif file_name == LOCATION:
                for line in lines_cor:
                    [x, y, alt] = line.split(', ')
                    x = x[1:len(x)]
                    alt = float(alt.split('.')[0] + '.' + alt.split('.')[1][0:-3])
                    location_lst.append((float(x), float(y), float(alt)))
                #print(LOCATION + "\n")

        for idx in range(num_of_lines-1):
            # (building_id, building_type, area, location, init_height)
            building = Building(prev_id + idx, subdir, area_lst[idx], location_lst[idx], height_lst[idx], all_types_dirs)
            all_building_onetype.append(building)
        buildings_data.append((subdir, all_building_onetype))
        prev_id = prev_id + num_of_lines-1

        buildings_data = sorted(buildings_data, key=lambda type: type[0])

    return buildings_data
