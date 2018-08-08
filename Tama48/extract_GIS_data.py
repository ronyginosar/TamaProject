#from building import Building
import public_building as pb
import building_residential as br
import building_types as bt

import os
from os import listdir
from os.path import isfile, join
from os.path import basename

HEIGHT = 'height'
AREA = 'area'
LOCATION = 'location'

def find_polygon_from_points(start_lst, end_lst):

    num_of_pts = len(start_lst)
    polygon_lst = [start_lst[0]]

    search_in_end = True
    next_idx = 0
    for t in range(num_of_pts - 1):
        if search_in_end:
            next_pt = end_lst[next_idx]
            next_idx = start_lst.index(next_pt)
            search_in_end = False
        else:
            next_pt = start_lst[next_idx]
            next_idx = end_lst.index(next_pt)
            search_in_end = True
        polygon_lst.append(next_pt)

    return polygon_lst


# creates building according to it's type.
def create_building(id, b_type, area, location, height):
    if b_type == bt.RESIDENTIAL:
        return br.Residential(id, area, location, height)
    elif b_type == bt.CLINIC:
        return pb.Clinic(id, area, location, height)
    elif b_type == bt.COMMUNITY_CNTR:
        return pb.CommunityCenter(id, area, location, height)
    elif b_type == bt.ELDERLY_CNTR:
        return pb.ElderlyCenter(id, area, location, height)
    elif b_type == bt.HIGH_SCHOOL:
        return pb.HighSchool(id, area, location, height)
    elif b_type == bt.KINDERGARDEN:
        return pb.Kindergarden(id, area, location, height)
    elif b_type == bt.HIGH_SCHOOL:
        return pb.HighSchool(id, area, location, height)
    elif b_type == bt.PRIMARY_SCHOOL:
        return pb.PrimarySchool(id, area, location, height)
    elif b_type == bt.MIKVE:
        return pb.Mikve(id, area, location, height)
    elif b_type == bt.HOSPITAL:
        return pb.Hospital(id, area, location, height)
    elif b_type == bt.SYNAGOUGE:
        return pb.Synagogue(id, area, location, height)
    elif b_type == bt.SPORT:
        return pb.Sport(id, area, location, height)
    elif b_type == bt.POLICE:
        return pb.Police(id, area, location, height)


def read_files(buildings_fullpath = '../data'):
    prev_id = 0
    type_idx = 0
    buildings_data = []
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

        for file in onlyfiles:
            if file != '.DS_Store':
                file_full_path = join(buildings_dirpath, file)
                f = open(file_full_path, 'r')
                lines = f.readlines()
                f.close()

            file_name = os.path.splitext(basename(file))[0]
            lines_cor = lines[1:len(lines)]
            if file_name == HEIGHT:
                num_of_buildings = len(lines) - 1
                for line in lines_cor:
                    height_lst.append(float(line.split('.')[0]+'.' + line.split('.')[1][0:-2]))
            elif file_name == AREA:
                for line in lines_cor:
                    area_lst.append(float(line.split('.')[0] + '.' + line.split('.')[1][0:-2]))
            elif file_name == LOCATION:
                for line in lines_cor:
                    [x, y, alt] = line.split(', ')
                    x = x[1:len(x)]
                    alt = float(alt.split('.')[0] + '.' + alt.split('.')[1][0:-3])
                    location_lst.append((float(x), float(y), float(alt)))
            else: # point 1, point2
                continue

        for idx in range(num_of_buildings):
            # (building_id, building_type, area, location, init_height)
            building = create_building(prev_id + idx, subdir, area_lst[idx], location_lst[idx], height_lst[idx])
            all_building_onetype.append(building)
        buildings_data.append((subdir, all_building_onetype))
        prev_id = prev_id + num_of_buildings

        buildings_data = sorted(buildings_data, key=lambda type: type[0])

    return buildings_data
