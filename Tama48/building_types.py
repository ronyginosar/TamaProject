
# TYPES and CONSTANTS
# including Util Function...

CLINIC = 'clinic'
COMMUNITY_CNTR = 'community_center'
ELDERLY_CNTR = 'elderly_center'
HIGH_SCHOOL = 'high_school'
HOSPITAL = 'hospital'
KINDERGARDEN = 'kindergarden'
MIKVE = 'mikve'
POLICE = 'police'
PRIMARY_SCHOOL = 'primary_school'
RESIDENTIAL = 'residential'
SPORT =  'sport'
SYNAGOUGE = 'synagogue'


def all_building_types():
    return [CLINIC, COMMUNITY_CNTR, ELDERLY_CNTR, HIGH_SCHOOL, HOSPITAL, KINDERGARDEN, MIKVE,
                              POLICE, PRIMARY_SCHOOL, RESIDENTIAL, SPORT, SYNAGOUGE]

def all_public_building_types():
    return [CLINIC, COMMUNITY_CNTR, ELDERLY_CNTR, HIGH_SCHOOL, HOSPITAL, KINDERGARDEN, MIKVE,
                              POLICE, PRIMARY_SCHOOL, SPORT, SYNAGOUGE]

def find_buildings_in_type(b_type, building_data):
    return [building[1] for building in building_data if building[0] == b_type][0]


def find_buildings_public(building_data):
    return [building for building in building_data if building[0] != RESIDENTIAL]

"""
plan_floors_state is a state [(building_id = 1, floors = f1), (building_id = 2, floors = f2), ..], of all building types
"""
def floors_given_buldingID_type(plan_floors_state, buildingID, b_type):
    # b_f_in_type = for specific building type
    b_f_in_type = find_buildings_in_type(b_type, plan_floors_state)
    return [building_floor[1] for building_floor in b_f_in_type if building_floor[0] == buildingID][0]

# TODO: TO CHECK INDEXING!!
def get_building_by_id(building_data, buildingID):
    # buildingID should start from 0.
    if buildingID >= len(building_data):
        return None
    return building_data[buildingID]