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

class Needs(object):
    def __init__(self, buildings_data, add_units,
                 age_percentage18 = 2.0, religious_percentage= 20.0, elderly_percentage=10,
                 avg_family_size = 3.2):
        #TODO: Naama: all these default parameters should stay here or should it be constant variables like above Adi?
        self.all_needs_dict = dict()
        self.add_housing_units = add_units
        self.add_population = math.ceil(add_units * METERS_PER_UNIT / SQMETER_PER_PERSON)
        self.original_population = math.ceil(get_residential_sum_area(buildings_data) / SQMETER_PER_PERSON)
        self.buildings_data = buildings_data
        self.age_percentage18 = age_percentage18
        self.religious_percentage = religious_percentage
        self.elderly_percentage = elderly_percentage
        self.avg_family_size = avg_family_size

        # TODO: Naama: Not in use yet!!
        self.type_importance_dict = {}
        avg_imp = 1/(len(bt.all_building_types())-1) # -1 for not considering the residential
        for building in bt.all_building_types():
            self.type_importance_dict[str(building)] = avg_imp

        # number of kids in a certain age (for ex. 102 kids in the age of 10 yo)
        # TODO: I don't see self.population_increase, I guess it is add_population, I don't understand why it is perctg
        # self.grade_size = age_percentage18 * self.population_increase / PERCENTAGE
        self.grade_size = age_percentage18 * self.add_population

        # number of classes per age to add
        self.class_rooms_per_age = math.ceil(self.grade_size / CLASS_SIZE)

        # add units of public services
        self.kindergarten_needs = (self.grade_size * KINDERGATDEN_NUM_GRADES)/ CLASS_SIZE
        self.primary_needs = (self.grade_size * PRIMARY_NUM_GRADES)/ CLASS_SIZE
        self.highschool_needs = (self.grade_size * HS_NUM_GRADES)/ CLASS_SIZE

        self.synagogue_needs = math.ceil(((self.add_population*self.religious_percentage/PERCENTAGE)*0.49)*1.1)
        self.mikve_needs = math.ceil(((self.add_population * self.religious_percentage/PERCENTAGE)/22.5)*0.007)

        # POLICE
        previous_police = 0
        for building in bt.find_buildings_in_type(bt.POLICE, self.buildings_data):
            previous_police += building.area
        if(self.add_population + self.original_population < 7000):
            self.police_needs = max(100 - previous_police, 0)
        elif(self.add_population + self.original_population <15000):
            self.police_needs = max(500 - previous_police, 0)
        elif(self.add_population + self.original_population <40000):
            self.police_needs = max(1500 - previous_police, 0)
        elif(self.add_population + self.original_population <100000):
            self.police_needs = max(3600 - previous_police, 0)
        else:
            self.police_needs = max(4400 - previous_police, 0)
        self.police_needs /= math.ceil(one_unit_in_meters(bt.POLICE))

        # COMMUNITY CENTER
        previous_community = 0
        for building in bt.find_buildings_in_type(bt.COMMUNITY_CNTR, self.buildings_data):
            previous_community += building.area
        if(self.add_population + self.original_population <300):
            self.community_center_needs = max(250 - previous_community, 0)
        elif(self.add_population + self.original_population <600):
            self.community_center_needs = max(400 - previous_community, 0)
        else:
            self.community_center_needs = max(750 - previous_community, 0)
        self.community_center_needs /= one_unit_in_meters(bt.COMMUNITY_CNTR)

        #ELDERLY CENTER
        # TODO: Naama: to add according to some percentage of the elderly popultion??
        self.elderly_center_needs = 0

        # CLINIC
        previous_health_clinic = 0
        for building in bt.find_buildings_in_type(bt.CLINIC, self.buildings_data):
            previous_health_clinic += building.area

        if(self.add_population + self.original_population <300):
            self.health_clinic_needs = max(300 - previous_health_clinic, 0)
        elif(self.add_population + self.original_population <600):
            self.health_clinic_needs = max(500 - previous_health_clinic, 0)
        else:
            self.health_clinic_needs = max(1000 - previous_health_clinic, 0)
        self.health_clinic_needs /= one_unit_in_meters(bt.CLINIC)

        # HOSPITAL
        self.hospital_needs = 0

        # SPORT
        self.sport_needs = 0

        # All needs are in area (square meters)
        for b_type in bt.all_building_types():
            if b_type == bt.KINDERGARDEN:
                self.all_needs_dict[b_type] = self.kindergarten_needs
            elif b_type == bt.PRIMARY_SCHOOL:
                self.all_needs_dict[b_type] = self.primary_needs
            elif b_type == bt.HIGH_SCHOOL:
                self.all_needs_dict[b_type] = self.hospital_needs
            elif b_type == bt.SYNAGOUGE:
                self.all_needs_dict[b_type] = self.synagogue_needs
            elif b_type == bt.MIKVE:
                self.all_needs_dict[b_type] = self.mikve_needs
            elif b_type == bt.POLICE:
                self.all_needs_dict[b_type] = self.police_needs
            elif b_type == bt.COMMUNITY_CNTR:
                self.all_needs_dict[b_type] = self.community_center_needs
            elif b_type == bt.ELDERLY_CNTR:
                self.all_needs_dict[b_type] = self.elderly_center_needs
            elif b_type == bt.CLINIC:
                self.all_needs_dict[b_type] = self.health_clinic_needs
            elif b_type == bt.HOSPITAL:
                self.all_needs_dict[b_type] = self.hospital_needs
            elif b_type == bt.SPORT:
                self.all_needs_dict[b_type] = self.sport_needs

        return self.all_needs_dict

    # get values
    def get_needs_for_type(self, building_type):
        return self.all_needs_dict[building_type]

    def get_all_needs(self):
        return self.all_needs_dict
