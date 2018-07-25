import math
import building_types

PERCENTAGE = 100
# recommended class size
CLASS_SIZE = 30

# recommended area for public buldings
SHUL_AREA = 200
MIKVE_AREA = 65
CLASSROOM_AREA = 130

# number of grades in group
KINDERGARDEN_NUM_GRADES = 3
PRIMARY_NUM_GRADES = 6
HS_NUM_GRADES = 4

# square meters per housing unit
# TODO: Naama: which unit??? I think it is different from building types... to check!
METERS_PER_UNIT = 90

class Needs(object):
    def __init__(self, buildings_types,  add_housing_units, avg_family_size = 3.2, age_percentage18 = 2.0, religious_percentage= 20.0):
        self.all_needs_dict = dict()
        self.buildings_types = buildings_types
        self.add_housing_units = add_housing_units
        self.avg_family_size = avg_family_size
        self.age_percentage18 = age_percentage18
        self.religious_percentage = religious_percentage

        # overall population in average to add given the housing unit we add
        self.add_population = self.add_housing_units * self.avg_family_size
        # number of kids in a certain age (for ex. 102 kids in the age of 10 yo)
        self.grade_size = age_percentage18 * self.add_population / PERCENTAGE

        # naama: just so it won't fail..
        #self.elderly_size =
        self.age_size = self.grade_size
        #####

        # number of classes per age to add
        self.class_rooms_per_age = math.ceil(self.age_size / CLASS_SIZE)  # naama: age_size or grade size?

        self.all_building_types = [building[0] for building in self.buildings_types]
        avg_imp = 1/(len(self.all_building_types)-1) # -1 for not considering the residential
        self.type_importance_dict = {}
        for building in self.buildings_types:
            self.type_importance_dict[str(building)] = avg_imp

        # add units of public services
        self.kindergarden_needs = (self.grade_size * KINDERGARDEN_NUM_GRADES)/ CLASS_SIZE * CLASSROOM_AREA
        self.primary_needs = (self.grade_size * PRIMARY_NUM_GRADES)/ CLASS_SIZE * CLASSROOM_AREA
        self.hs_needs = (self.grade_size * HS_NUM_GRADES)/ CLASS_SIZE * CLASSROOM_AREA
        self.shul_needs =  ((self.add_population*self.religious_percentage/PERCENTAGE)*0.49)*1.1 * SHUL_AREA
        self.mikve_needs = ((self.add_population*self.religious_percentage/PERCENTAGE)/22.5)*0.007 * MIKVE_AREA
        self.cc_needs = 0
        self.ec_needs = 0
        #self.police =

        # claculate once
        self.calc_all_needs()

    def calc_all_needs(self):
        for building in self.buildings_types:
            # TODO: finish all needs
            if building[0] == building_types.KINDERGARDEN:
                self.all_needs_dict[building[0]] = self.kindergarden_needs
            elif building[0] == building_types.PRIMARY_SCHOOL:
                self.all_needs_dict[building[0]] = self.primary_needs
            elif building[0] == building_types.HIGH_SCHOOL:
                self.all_needs_dict[building[0]] = self.hs_needs
            elif building[0] == building_types.SYNAGOUGE:
                self.all_needs_dict[building[0]] = self.shul_needs
            elif building[0] == building_types.COMMUNITY_CNTR:
                self.all_needs_dict[building[0]] = self.cc_needs
            elif building[0] == building_types.ELDERLY_CNTR:
                self.all_needs_dict[building[0]] = self.ec_needs

        return self.all_needs_dict

    # get values
    def get_needs_for_type(self, building_type):
        for building in self.buildings_types:
            if building[0] == building_type:
                return self.all_needs_dict[building[0]]

    def get_all_needs(self, building_type):
        return self.all_needs_dict
