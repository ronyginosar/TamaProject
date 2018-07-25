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


def find_buildings_in_type(b_type, building_data):
    return [building[1] for building in building_data if building[0] == b_type][0]


def find_buildings_public(b_type, building_data):
    return [building for building in building_data if building[0] != RESIDENTIAL]


def floors_given_buldingID_type(plan_floors_state, buildingID, b_type):
    # b_f_in_type: [(building_id = 1, floors = f1), (building_id = 2, floors = f2), ..], for specific building type
    b_f_in_type = find_buildings_in_type(b_type, plan_floors_state)
    return [building_floor[1] for building_floor in b_f_in_type if building_floor[0] == buildingID][0]

# def init_floors(building_data):
#     # b_f_in_type: [(building_id = 1, floors = f1), (building_id = 2, floors = f2), ..], for specific building type
#     b_f_in_type = find_buildings_in_type(b_type, plan_floors_state)
#     return [building_floor[1] for building_floor in b_f_in_type if building_floor[0] == buildingID][0]


def one_unit_in_meters(b_type):
    # TODO: for AJ or Adi: To implement according to document of excel.
    if b_type == CLINIC:
        return 100
    elif b_type == COMMUNITY_CNTR:
        return 100
    elif b_type == ELDERLY_CNTR:
        return 100
    elif b_type == HIGH_SCHOOL:
        return 100
    elif b_type == HOSPITAL:
        return 100
    elif b_type == KINDERGARDEN:
        return 100
    elif b_type == MIKVE:
        return 100
    elif b_type == POLICE:
        return 100
    elif b_type == PRIMARY_SCHOOL:
        return 100
    elif b_type == RESIDENTIAL:
        return 100
    elif b_type == SPORT:
        return 100
    elif b_type == SYNAGOUGE:
        return 100

