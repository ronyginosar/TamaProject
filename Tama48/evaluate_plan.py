"""
buildings_data: list of tuples, each tuple contains (buildings_type, list of all Building objects in this type)
additional_height: tuple of (building_id(int), additional_height(meters))
type_importance_dict:
"""

PERCENTAGE = 100
SQMETER_PER_PERSON = 22
# recommended class size
CLASS_SIZE = 30
SHUL_AREA = 200
MIKVE_AREA = 65
CLASSROOM_AREA = 130
KINDERGARTEN_NUM_GRADES = 3
PRIMARY_NUM_GRADES = 6
HS_NUM_GRADES = 4

class Needs(object):
    def __init__(self, original_area, buildings_data, add_area,
                 age_percentage18 = 2.0, religious_percentage= 20.0, elderly_percentage=10,
                 avg_family_size = 3.2):

        self.all_needs_dict = dict()
        self.add_population = add_area * SQMETER_PER_PERSON
        self.original_population = original_area / SQMETER_PER_PERSON
        self.original_state = original_population
        self.buildings_data = buildings_data
        self.age_percentage18 = age_percentage18
        self.religious_percentage = religious_percentage
        self.elderly_percentage = elderly_percentage
        self.avg_family_size = avg_family_size

        self.building_types = [building[0] for building in buildings_data]

        avg_imp = 1/(len(self.building_types)-1) # -1 for not considering the residential
        for building in self.buildings_types:
            self.type_importance_dict[building] = avg_imp


        # overall population in average to add given the housing unit we add
        self.add_population = self.add_housing_units * self.avg_family_size

        # number of kids in a certain age (for ex. 102 kids in the age of 10 yo)
        self.grade_size = age_percentage18 * self.population_increase / PERCENTAGE

        # number of classes per age to add
        self.class_rooms_per_age = ceil(self.age_size / CLASS_SIZE)


        # add units of public services
        self.kindergarten_needs = (self.grade_size * KINDERGATDEN_NUM_GRADES)/ CLASS_SIZE * CLASSROOM_AREA
        self.primaryschool_needs = (self.grade_size * PRIMARY_NUM_GRADES)/ CLASS_SIZE * CLASSROOM_AREA
        self.highschool_needs = (self.grade_size * HS_NUM_GRADES)/ CLASS_SIZE * CLASSROOM_AREA

        self.synagogue_needs =  ((self.add_population*self.religious_percentage/PERCENTAGE)*0.49)*1.1 * SHUL_AREA
        self.mikve_needs = ((self.add_population*self.religious_percentage/PERCENTAGE)/22.5)*0.007 * MIKVE_AREA

        previous_police = 0
        for building_item in self.buildings_data:
            if building_item[0]  == 'police':
                for building in building_item[1]:
                    previous_police += building.area

        if(self.add_population + original_population <7000):
            self.police_needs = 100 - previous_police
        elif(self.self.add_population + original_population <15000):
            self.police_needs = 500 - previous_police
        elif(self.self.add_population + original_population <40000):
            self.police_needs = 1500 - previous_police
        elif(self.self.add_population + original_population <100000):
            self.police_needs = 3600 - previous_police
        else:
            self.police_needs = 4400 - previous_police


        previous_community = 0
        for building_item in self.buildings_data:
            if building_item[0]  == 'community_center':
                for building in building_item[1]:
                    previous_community += building.area

        if(self.add_population + original_population <300):
            self.community_center_needs = 250 - previous_community
        elif(self.self.add_population + original_population <600):
            self.community_center_needs = 400 - previous_community
        else:
            self.community_center_needs = 750 - previous_community

        self.elderly_center_needs = 0

        previous_health_clinic = 0
        for building_item in self.buildings_data:
            if building_item[0]  == 'health_clinic':
                for building in building_item[1]:
                    previous_health_clinic += building.area

        if(self.add_population + original_population <300):
            self.health_clinic_needs = 300 - previous_health_clinic
        elif(self.self.add_population + original_population <600):
            self.health_clinic_needs = 500 - previous_health_clinic
        else:
            self.health_clinic_needs = 1000 - previous_health_clinic

        self.hospital_needs = 0
        self.sport_needs = 0

        #all needs are in area (square meters)
        for building in self.buildings_types:
            if building[0] == 'kindergarten':
                self.all_needs_dict[building[0]] = self.kindergarten_needs
            elif building[0] == 'primary_school':
                self.all_needs_dict[building[0]] = self.primary_needs
            elif building[0] == 'high_school':
                self.all_needs_dict[building[0]] = self.hs_needs
            elif building[0] == 'synagogue':
                self.all_needs_dict[building[0]] = self.synagogue_needs
            elif building[0] == 'mikve':
                self.all_needs_dict[building[0]] = self.mikve_needs
            elif building[0] == 'police':
                self.all_needs_dict[building[0]] = self.police_needs
            elif building[0] == 'community_center':
                self.all_needs_dict[building[0]] = self.community_center_needs
            elif building[0] == 'elderly_center':
                self.all_needs_dict[building[0]] = self.elderly_center_needs
            elif building[0] == 'health_clinic':
                self.all_needs_dict[building[0]] = self.health_clinic_needs
            elif building[0] == 'hospital':
                self.all_needs_dict[building[0]] = self.hospital_needs
            elif building[0] == 'sport':
                self.all_needs_dict[building[0]] = self.sport_needs



    # TODO calc for genetic iterations..
    # def calc_plan_evaluation(additional_height):
    #     plan_grade = 0.0
    #     for building_type in self.buildings_data:
    #         imp = self.type_importance_dict[building_type]
    #         plan_grade += self.calc_specific_plan_evaluation(building_type)*imp
    #
    #     return plan_grade
import needs

class EvaluatePlan(object):
    """
    init_state: includes all values of Building as object i.e
    [(kindergarden, [B1, B2, ..]), ((hospital, [B7, B8, ..])), ...]

    plan_hights_state: includes all values of ONLY heights as object i.e
    [(kindergarden, [h1, h2, ..]), ((hospital, [h7, h8, ..])), ...]

    needs is an object of Needs. it's a "singleton" for one run,
    i.e for onerequest of additional population, we create this object only once.
    """
    def __init__(self, init_state, plan_heights_state, needs):

        self.init_state = init_state
        self.plan_heights_state = plan_heights_state
        self.needs = needs
        self.buildings_types = self.needs.buildings_types

    def check_plan(self):
        # all_needs = needs.get_all_needs

        evaluate_plan = 1
        for b_type in self.buildings_types:
            needs_for_type = needs.get_needs_for_type(b_type)
            evaluated_for_type = self.evaluate_plan_for_type(b_type, needs_for_type)

            # in  case of better conditions than needs, still having 1 as rank
            evaluate_plan *= max(evaluated_for_type/needs_for_type)
            # evaluate_plan *= (evaluated_for_type/needs_for_type)

    """
    needs_for_type are in units of m^2.
    """
    def evaluate_plan_for_type(self, b_type, needs_for_type):
        buildings_in_type = [building[1] for building in self.init_state if building[0] == b_type][0]

        sum_m2 = 0
        idx = 0
        if b_type != 'residential':
            for building in buildings_in_type:
                sum_m2 += building.area * self.plan_heights_state[idx]

                # add another function between 0-1 related to the distances..

                # more??

                idx += 1
        else:
            # maybe to check something else, in this case, it is mandatory to have number of meters per person...
            pass