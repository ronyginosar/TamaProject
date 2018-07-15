"""
buildings_data: list of tuples, each tuple contains (buildings_type, list of all Building objects in this type)
additional_height: tuple of (building_id(int), additional_height(meters))
type_importance_dict:
"""

PERCENTAGE = 100
# recommended class size
CLASS_SIZE = 27
#KINDERGARDEN_M2 = 130
KINDERGARDEN_NUM_GROUPS = 3

class Needs(object):
    def __init__(self, buildings_data,  add_housing_units, avg_family_size = 3.2, age_percentage18 = 2.0, religious_percentage= 20.0):
        self.buildings_data = buildings_data
        self.add_housing_units = add_housing_units
        self.avg_family_size = avg_family_size
        self.age_percentage18 = age_percentage18
        self.religious_percentage = religious_percentage

        # overall population in avarge to add given the housing unit we add
        self.add_population = self.add_housing_units * self.avg_family_size
        # number of kids in a certain age (for ex. 102 kids in the age of 10 yo)
        self.age_size = self.add_population / PERCENTAGE
        # number of classes per age to add
        self.class_rooms_per_age = self.age_size/ CLASS_SIZE

        self.all_building_types = [building[0] for building in self.buildings_data]
        avg_imp = 1/(len(self.all_building_types)-1) # -1 for not considering the residential
        for building in self.buildings_data:
            self.type_importance_dict[building] = avg_imp

        # add units of public services
        self.kindergarden_num = (self.age_size * KINDERGARDEN_NUM_GROUPS)/ CLASS_SIZE

    def calc_all_needs(self):
        all_needs_dict = dict()
        for building in self.buildings_data:
            if building[0] == 'kindergarden':
                all_needs_dict[building[0]] = self.kindergarden_num
            # if ....

        return all_needs_dict

    # TODO calc for genetic iterations..
    # def calc_plan_evaluation(additional_height):
    #     plan_grade = 0.0
    #     for building_type in self.buildings_data:
    #         imp = self.type_importance_dict[building_type]
    #         plan_grade += self.calc_specific_plan_evaluation(building_type)*imp
    #
    #     return plan_grade
