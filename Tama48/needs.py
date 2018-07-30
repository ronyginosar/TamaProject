import math
import building_types as bt

PERCENTAGE = 100

# recommended class size (num of student in class)
CLASS_SIZE = 30

# number of grades in group
KINDERGARDEN_NUM_GRADES = 3
PRIMARY_NUM_GRADES = 6
HS_NUM_GRADES = 4

KINDERGATDEN_NUM_GRADES = 3

# square meters per housing unit
METERS_PER_UNIT = 90 # TODO: Naama: is it all for both private and ALL pubic units, Adi, AJ??
RESD_METER_PER_UNIT = 90 # TODO: Naama: Temp
SQMETER_PER_PERSON = 22 # TODO: Naama: it wasn't in the file of AJ. This is what I remember.. is it correct Adi, AJ??


def one_unit_in_meters(b_type):
    # TODO: for AJ or Adi: To implement according to document of excel.
    if b_type == bt.CLINIC:
        # TODO: to check
        return 100
    elif b_type == bt.COMMUNITY_CNTR:
        # TODO: to check
        return 100
    elif b_type == bt.ELDERLY_CNTR:
        # TODO: to check
        return 100
    elif b_type == bt.HIGH_SCHOOL:
        return 130
    elif b_type == bt.HOSPITAL:
        # TODO: to check department maybe?
        return 300
    elif b_type == bt.KINDERGARDEN:
        return 130
    elif b_type == bt.MIKVE:
        return 65
    elif b_type == bt.POLICE:
        #TODO: to check
        return 200
    elif b_type == bt.PRIMARY_SCHOOL:
        return 130
    elif b_type == bt.RESIDENTIAL:
        # TODO: to check
        return 100
    elif b_type == bt.SPORT:
        # TODO: to check
        return 100
    elif b_type == bt.SYNAGOUGE:
        return 200


def get_residential_sum_area(building_data):
    resd_buildings = bt.find_buildings_in_type(bt.RESIDENTIAL, building_data)
    all_areas = [resd_building.area for resd_building in resd_buildings]
    return sum(all_areas)

# elderly_percentage=10, avg_family_size = 3.2, but we didn't use it!
def calc_needs(buildings_data, add_housing_units, age_percentage18=2.0, religious_percentage=20.0):
    #TODO: Naama: all these default parameters should stay here or should it be constant variables like above Adi?
    add_population = math.ceil(add_housing_units * METERS_PER_UNIT / SQMETER_PER_PERSON)
    original_population = math.ceil(get_residential_sum_area(buildings_data) / SQMETER_PER_PERSON)

    # TODO: Naama: Not in use yet!!
    type_importance_dict = {}
    avg_imp = 1/(len(bt.all_building_types())-1) # -1 for not considering the residential
    for building in bt.all_building_types():
        type_importance_dict[str(building)] = avg_imp

    # number of kids in a certain age (for ex. 102 kids in the age of 10 yo)
    # TODO: I don't see population_increase, I guess it is add_population, I don't understand why it is perctg
    # grade_size = age_percentage18 * population_increase / PERCENTAGE
    grade_size = age_percentage18 * add_population

    # add units of public services
    kindergarten_needs = (grade_size * KINDERGATDEN_NUM_GRADES)/ CLASS_SIZE
    primary_needs = (grade_size * PRIMARY_NUM_GRADES)/ CLASS_SIZE
    highschool_needs = (grade_size * HS_NUM_GRADES)/ CLASS_SIZE

    synagogue_needs = math.ceil(((add_population*religious_percentage/PERCENTAGE)*0.49)*1.1)
    mikve_needs = math.ceil(((add_population * religious_percentage/PERCENTAGE)/22.5)*0.007)

    # POLICE
    previous_police = 0
    for building in bt.find_buildings_in_type(bt.POLICE, buildings_data):
        previous_police += building.area
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
    police_needs /= math.ceil(one_unit_in_meters(bt.POLICE))

    # COMMUNITY CENTER
    previous_community = 0
    for building in bt.find_buildings_in_type(bt.COMMUNITY_CNTR, buildings_data):
        previous_community += building.area
    if add_population + original_population <300:
        community_center_needs = max(250 - previous_community, 0)
    elif add_population + original_population <600:
        community_center_needs = max(400 - previous_community, 0)
    else:
        community_center_needs = max(750 - previous_community, 0)
    community_center_needs /= one_unit_in_meters(bt.COMMUNITY_CNTR)

    # ELDERLY CENTER
    # TODO: Naama: to add according to some percentage of the elderly popultion??
    elderly_center_needs = 0

    # CLINIC
    previous_health_clinic = 0
    for building in bt.find_buildings_in_type(bt.CLINIC, buildings_data):
        previous_health_clinic += building.area

    if add_population + original_population <300:
        health_clinic_needs = max(300 - previous_health_clinic, 0)
    elif add_population + original_population <600:
        health_clinic_needs = max(500 - previous_health_clinic, 0)
    else:
        health_clinic_needs = max(1000 - previous_health_clinic, 0)
    health_clinic_needs /= one_unit_in_meters(bt.CLINIC)

    # HOSPITAL
    hospital_needs = 0

    # SPORT
    sport_needs = 0

    all_needs_dict = dict()
    # All needs are in area (square meters)
    for b_type in bt.all_building_types():
        if b_type == bt.KINDERGARDEN:
            all_needs_dict[b_type] = kindergarten_needs
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
    return all_needs_dict
