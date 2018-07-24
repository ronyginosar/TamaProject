"""
buildings_data: list of tuples, each tuple contains (buildings_type, list of all Building objects in this type)
additional_height: tuple of (building_id(int), additional_height(meters))
type_importance_dict:
"""

PERCENTAGE = 100
# recommended class size
CLASS_SIZE = 30
SHUL_AREA = 200
MIKVE_AREA = 65
CLASSROOM_AREA = 130
KINDERGARDEN_NUM_GRADES = 3
PRIMARY_NUM_GRADES = 6
HS_NUM_GRADES = 4

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
        self.elderly_size =
        # number of classes per age to add
        self.class_rooms_per_age = ceil(self.age_size / CLASS_SIZE)

        self.all_building_types = [building[0] for building in self.buildings_types]
        avg_imp = 1/(len(self.all_building_types)-1) # -1 for not considering the residential
        for building in self.buildings_types:
            self.type_importance_dict[building] = avg_imp

        # add units of public services
        self.kindergarden_needs = (self.grade_size * KINDERGARDEN_NUM_GRADES)/ CLASS_SIZE * CLASSROOM_AREA
        self.primary_needs = (self.grade_size * PRIMARY_NUM_GRADES)/ CLASS_SIZE * CLASSROOM_AREA
        self.hs_needs = (self.grade_size * HS_NUM_GRADES)/ CLASS_SIZE * CLASSROOM_AREA
        self.shul_needs =  ((self.add_population*self.religious_percentage/PERCENTAGE)*0.49)*1.1 * SHUL_AREA
        self.mikve_needs = ((self.add_population*self.religious_percentage/PERCENTAGE)/22.5)*0.007 * MIKVE_AREA
        self.cc_needs = 0
        self.ec_needs = 0
        if(self.add_population <7000):
            self.police = 100
        elif(self.add_population <15000):
            self.police = 500

        elif(self.add_population <40000):
            self.police = 500
        elif(self.add_population <100000):
            self.police = 500


    #TODO all needs need to be in area
    def calc_all_needs(self):
        for building in self.buildings_types:
            if building[0] == 'kindergarden':
                self.all_needs_dict[building[0]] = self.kindergarden_needs
            elif building[0] == 'primary_school':
                self.all_needs_dict[building[0]] = self.primary_needs
            elif building[0] == 'high_school':
                self.all_needs_dict[building[0]] = self.hs_needs
            elif building[0] == 'synagogue':
                self.all_needs_dict[building[0]] = self.shul_needs
            elif building[0] == 'community_center':
                self.all_needs_dict[building[0]] = self.cc_needs
            elif building[0] == 'elderly_center':
                self.all_needs_dict[building[0]] = self.ec_needs

    # TODO calc for genetic iterations..
    # def calc_plan_evaluation(additional_height):
    #     plan_grade = 0.0
    #     for building_type in self.buildings_data:
    #         imp = self.type_importance_dict[building_type]
    #         plan_grade += self.calc_specific_plan_evaluation(building_type)*imp
    #
    #     return plan_grade
