<<<<<<< HEAD
#import needs

def calc_distance_two_building(residential_building, public_building):
    loc1 = residential_building.get_location()
    loc2 = residential_building.get_location()

    euclid_dist = pow(pow(loc1.x - loc2.x, 2) + pow(loc1.y - loc2.y, 2), 0.5)
    return euclid_dist

def evaluate_by_distance_all(residential_buildings, extra_heights_state, public_buildings_sametype):
    # given all residential building, the new plan for heights, and a list of specific type of public building
    # we return a probability vector over the public building from this type, which is the weighted sum of
    # all residential building' new area (of the new state) * all distances of them to this specific building
    # normalized to 0-1, for probability preferences.

    svg_dist_lst = []
    for public_building in public_buildings_sametype:
        svg_dist = 0.0
        for resi_building in residential_buildings:
            extra_area = extra_heights_state[resi_building.id]*resi_building.area
            svg_dist += calc_distance_two_building(resi_building, public_building)*extra_area
        svg_dist_lst.append(svg_dist)
    sum_svg_dist_lst = sum(svg_dist_lst)
    sum_svg_dist_lst_prob = [avg_dist/sum_svg_dist_lst for avg_dist in svg_dist_lst]

    # finally, duplicate the probability (importance) of the PUBLIC buildings with its extra height
    i = 0
    ret_val = 0.0
    for public_building in public_buildings_sametype:
        sum_area_public_building = extra_heights_state[public_building.id] \
                                   * public_building.area * extra_heights_state[public_building.id]
        ret_val += sum_svg_dist_lst_prob[i] * sum_area_public_building
    return ret_val

=======
<<<<<<< HEAD
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
=======
import needs
>>>>>>> c8a6fb715332993335778700ced2325a05ec7648

class EvaluatePlan(object):
    """
    init_state: includes all values of Building as object i.e
    [(kindergarden, [B1, B2, ..]), ((hospital, [B7, B8, ..])), ...]

    plan_hights_state: includes all values of ONLY heights as object i.e
    [(kindergarden, [h1, h2, ..]), ((hospital, [h7, h8, ..])), ...]

    needs is an object of Needs. it's a "singleton" for one run,
    i.e for onerequest of additional population, we create this object only once.
    """
    def __init__(self, building_data, plan_heights_state, all_needs):

        self.building_data = building_data
        self.plan_heights_state = plan_heights_state
        self.all_needs = all_needs
        self.buildings_types = self.all_needs.buildings_types

    def check_plan(self):
        evaluate_plan = 1
        for b_type in self.buildings_types:
            needs_for_type = 10  #self.all_needs.get_needs_for_type(b_type)  #  temporarily = 10
            evaluated_for_type = self.evaluate_plan_for_type(b_type, needs_for_type)

            # in case of better conditions than what is needed, still having 1 as rank
            evaluate_plan *= max(evaluated_for_type/needs_for_type, 1)

    """
    needs_for_type are in units of m^2.
    needs_for_type=10 just because Needs is not finished yet.
    """
    def evaluate_plan_for_type(self, b_type, all_residentials, needs_for_type=10):
        buildings_in_type = [building[1] for building in self.building_data if building[0] == b_type][0]

        sum_m2 = 0
        if b_type != 'residential':
            for building in buildings_in_type:
                sum_m2 += building.area * self.plan_heights_state[building.get_id()]

        # for now, the requested needs are mandatory!!!
        if sum_m2 < needs_for_type:
            return 0

        # weighted values according to areas vs distances..
        evaluate_plan_rank = evaluate_by_distance_all(all_residentials, self.plan_heights_state, buildings_in_type)
        # more? is there some another function between 0-1??

<<<<<<< HEAD
        return evaluate_plan_rank
=======
                idx += 1
        else:
            # maybe to check something else, in this case, it is mandatory to have number of meters per person...
            pass
>>>>>>> 8187f35ab78e029891a8ed0c74c415c8d917ae0e
>>>>>>> c8a6fb715332993335778700ced2325a05ec7648
