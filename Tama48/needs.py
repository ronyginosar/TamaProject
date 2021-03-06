import math
import building_types as bt

PERCENTAGE = 100

# recommended class size (num of student in class)
CLASS_SIZE = 27

# number of grades in group
KINDERGARDEN_NUM_GRADES = 3
PRIMARY_NUM_GRADES = 6
HS_NUM_GRADES = 6

KINDERGATDEN_NUM_GRADES = 5

AVG_FAMILY_SIZE = 3.32

AGE_GROUP18_PRCTG = 2.0

RELIGION_PRCTG = 20.0

# square meters per housing unit
# METER_PER_UNIT = 90
SQ_METER_PER_PERSON = 30
METERS_PER_UNIT = SQ_METER_PER_PERSON * AVG_FAMILY_SIZE

def one_unit_in_meter_square(b_type):
    # implemented according to document of excel.
    if b_type == bt.CLINIC:
        return 100
    elif b_type == bt.COMMUNITY_CNTR:
        return 100
    elif b_type == bt.ELDERLY_CNTR:
        return 100
    elif b_type == bt.HIGH_SCHOOL:
        return 130
    elif b_type == bt.HOSPITAL:
        return 300
    elif b_type == bt.KINDERGARDEN:
        return 130
    elif b_type == bt.MIKVE:
        return 65
    elif b_type == bt.POLICE:
        return 200
    elif b_type == bt.PRIMARY_SCHOOL:
        return 130
    elif b_type == bt.RESIDENTIAL:
        return 90
    elif b_type == bt.SPORT:
        return 100
    elif b_type == bt.SYNAGOUGE:
        return 200


def get_residential_sum_area(building_data):
    resd_buildings = bt.find_buildings_in_type(bt.RESIDENTIAL, building_data)
    all_areas = [resd_building.get_area() for resd_building in resd_buildings]
    return sum(all_areas)

# elderly_percentage=10, avg_family_size = 3.2, but we didn't use it!
def calc_needs(buildings_data, add_housing_units):

    add_population = math.ceil(add_housing_units * AVG_FAMILY_SIZE)
    original_population = math.ceil(get_residential_sum_area(buildings_data) / METERS_PER_UNIT * AVG_FAMILY_SIZE)

    type_importance_dict = {}
    avg_imp = 1/(len(bt.ALL_BUILDING_TYPES)-1) # -1 for not considering the residential
    for building in bt.ALL_BUILDING_TYPES:
        type_importance_dict[str(building)] = avg_imp

    # number of kids in a certain age (for ex. 102 kids in the age of 10 yo)
    # grade_size = age_percentage18 * population_increase / PERCENTAGE
    grade_size = AGE_GROUP18_PRCTG * add_population / PERCENTAGE

    # add units of public services
    kindergarden_needs = (grade_size * KINDERGARDEN_NUM_GRADES)/ CLASS_SIZE
    primary_needs = (grade_size * PRIMARY_NUM_GRADES)/ CLASS_SIZE
    highschool_needs = (grade_size * HS_NUM_GRADES)/ CLASS_SIZE

    synagogue_needs = math.ceil(((add_population*RELIGION_PRCTG/PERCENTAGE)*0.49)*1.1)/one_unit_in_meter_square(bt.SYNAGOUGE)
    mikve_needs = math.ceil(((add_population * RELIGION_PRCTG/PERCENTAGE)/22.5)*0.35)/one_unit_in_meter_square(bt.MIKVE) # 0.35 instead of 0.007

    # POLICE
    previous_police = 0
    for building in bt.find_buildings_in_type(bt.POLICE, buildings_data):
        previous_police += building.get_area()

    if add_population + original_population < 7000:
        police_needs = max(100 - previous_police, 0)
    elif add_population + original_population <15000:
        police_needs = max(500 - previous_police, 0)
    elif add_population + original_population <40000:
        police_needs = max(1500 - previous_police, 0)
    elif add_population + original_population <100000:
        police_needs = max(3600 - previous_police, 0)
    else:
        police_needs = max(4400 - previous_police, 0)
    police_needs /= math.ceil(one_unit_in_meter_square(bt.POLICE))

    # COMMUNITY CENTER
    previous_community = 0
    for building in bt.find_buildings_in_type(bt.COMMUNITY_CNTR, buildings_data):
        previous_community += building.get_area()
    if add_population + original_population <300:
        community_center_needs = max(250 - previous_community, 0)
    elif add_population + original_population <600:
        community_center_needs = max(400 - previous_community, 0)
    else:
        community_center_needs = max(750 - previous_community, 0)
    community_center_needs /= one_unit_in_meter_square(bt.COMMUNITY_CNTR)

    # ELDERLY CENTER
    elderly_center_needs = 0

    # CLINIC
    previous_health_clinic = 0
    for building in bt.find_buildings_in_type(bt.CLINIC, buildings_data):
        previous_health_clinic += building.get_area()

    if add_population + original_population <300:
        health_clinic_needs = max(300 - previous_health_clinic, 0)
    elif add_population + original_population <600:
        health_clinic_needs = max(500 - previous_health_clinic, 0)
    else:
        health_clinic_needs = max(1000 - previous_health_clinic, 0)
    health_clinic_needs /= one_unit_in_meter_square(bt.CLINIC)

    # HOSPITAL
    hospital_needs = 0

    # SPORT
    sport_needs = 0

    all_needs_dict = dict()
    # All needs are in area (square meters)
    for b_type in bt.ALL_BUILDING_TYPES:
        if b_type == bt.KINDERGARDEN:
            all_needs_dict[b_type] = kindergarden_needs
        elif b_type == bt.PRIMARY_SCHOOL:
            all_needs_dict[b_type] = primary_needs
        elif b_type == bt.HIGH_SCHOOL:
            all_needs_dict[b_type] = highschool_needs
        elif b_type == bt.SYNAGOUGE:
            all_needs_dict[b_type] = synagogue_needs
        elif b_type == bt.MIKVE:
            all_needs_dict[b_type] = mikve_needs
        elif b_type == bt.POLICE:
            all_needs_dict[b_type] = police_needs
        elif b_type == bt.COMMUNITY_CNTR:
            all_needs_dict[b_type] = community_center_needs
        elif b_type == bt.ELDERLY_CNTR:
            all_needs_dict[b_type] = elderly_center_needs
        elif b_type == bt.CLINIC:
            all_needs_dict[b_type] = health_clinic_needs
        elif b_type == bt.HOSPITAL:
            all_needs_dict[b_type] = hospital_needs
        elif b_type == bt.SPORT:
            all_needs_dict[b_type] = sport_needs
        elif b_type == bt.RESIDENTIAL:
            all_needs_dict[b_type] = add_housing_units
    return all_needs_dict
