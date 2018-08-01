import copy
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
    for tuple in building_data:
        if tuple[0] == b_type:
            return tuple[1]
    #return [building[1] for building in building_data if building[0] == b_type][0]


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
def get_building_by_type_id(b_type, buildingID, building_data):
    building_in_type = find_buildings_in_type(b_type, building_data)
    for building in building_in_type:
        if building.get_id() == buildingID:
            return building
    return None

"""
@:param plan_floors_state is of the form []

The use of this function-
First step: plan_floors_state has values only of additional floors of residential buildings
Second step: plan_floors_state has values of all floors: residential and public buildings.
Make sure each time to send the init_buildings_data (as extracted from files) and not the init + step1)
"""
def update_building_data_with_floors_plan(init_buildings_resd, additional_floors_resd):
    update_building_data_resd = copy.deepcopy(init_buildings_resd)
    idx = 0
    for building in update_building_data_resd:
        building.set_extra_height(additional_floors_resd[idx])
        idx += 1
    return update_building_data_resd
