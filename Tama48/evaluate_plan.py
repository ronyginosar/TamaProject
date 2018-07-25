import building_types

"""
3 main evaluations methods:

cost                    : more than 20% of the height is more expensive in x*money.
                          more than 12 floors- more expensive by y*money
distance                :
ratio to optimum needs  :
"""

NEEDS_PRCTG = 0.5
DISTANCE_PERCTG = 0.25
COST_PRCTG = 0.25

# for extra floors we reduce the score according to cost..
PERCENTAGE = 100

FLOORS_PRCTG = 0.2
FLOORS_NUM = 12
COST_MORE_PRSTG = 0.9
COST_MORE_NUM_FLOORS = 0.1

"""
:param buildings_data- initial param data.
:param additional_floors_resd
:param b_type, public building type to add units
:param all_needs
return: List<int, int>, first int: building_id, second int:number of floors to add.
is a solution for public public from type b_type
"""
# TODO: to implement
def calc_public_floors(buildings_data, additional_floors_resd, b_type, all_needs):
    pass

# TODO: to implement
def get_additional_public_floors(buildings_data, additional_floors, all_needs):
    pass

########################### DISTANCE ##############################
"""
Done!
distance between centers of two buildings
usually for one public, one residential
"""
# TODO: TO CHECK IMPLEMENTATION
def calc_distance_two_buildings(buildings_resd, building_public):
    loc1 = buildings_resd.get_location()
    loc2 = building_public.get_location()

    euclid_dist = pow(pow(loc1.x - loc2.x, 2) + pow(loc1.y - loc2.y, 2), 0.5)
    return euclid_dist


"""
evaluate distance of all buildings from all public buildings from one building_type.
the result is a weighted value

given all residential building, the new plan for heights, and a list of specific type of public building
we return a probability vector over the public building from this type, which is the weighted sum of
all residential building' new area (of the new state) * all distances of them to this specific building
normalized to 0-1, for probability preferences.
"""
# TODO: TO CHECK IMPLEMENTATION
def evaluate_buildings_distances_for_type(data_buildings_resd, extra_floors_state, public_buildings_sametype):
    svg_dist_lst = []
    for public_building in public_buildings_sametype:
        svg_dist = 0.0
        for resi_building in data_buildings_resd:
            extra_area = extra_floors_state[resi_building.id] * resi_building.area
            svg_dist += calc_distance_two_buildings(resi_building, public_building) * extra_area
        svg_dist_lst.append(svg_dist)
    sum_svg_dist_lst = sum(svg_dist_lst)
    sum_svg_dist_lst_prob = [avg_dist / sum_svg_dist_lst for avg_dist in svg_dist_lst]

    # finally, duplicate the probability (importance) of the PUBLIC buildings with its extra height
    i = 0
    ret_val = 0.0
    for public_building in public_buildings_sametype:
        sum_area_public_building = extra_floors_state[public_building.id] \
                                   * public_building.area * extra_floors_state[public_building.id]
        ret_val += sum_svg_dist_lst_prob[i] * sum_area_public_building
        # TODO: take sum_svg_dist_lst_prob[i] * sum_area_public_building as output maybe
        # TODO: so it will be good both for evalation and both calc_public_floors...
    return ret_val

"""
for MIN_CONFLICT case: when need to evaluate per building
"""
# TODO: implemnt
def calc_plan_building_score_distance(self, resd_building_obj):
    # for one residential building, calculate distance from all types of public building.
    building_distance_score = 1

    return building_distance_score


########################### NEEDS ##############################

"""
@:param b_type: String, building type from building_types.py
@:param needs_for_type: float [m^2]
@:param all_residentials:
"""
# TODO: TO CHECK IMPLEMENTATION
def evaluate_plan_needs_for_type(b_type, plan_floors_state, all_residentials, needs_for_type):

    buildings_in_type = building_types.find_buildings_in_type()

    sum_m2 = 0
    if b_type != building_types.RESIDENTIAL:
        for building in buildings_in_type:
            sum_m2 += building.area * \
                      building_types.floors_given_buldingID_type(plan_floors_state, building.get_id(), b_type)

    # for now, the requested needs are mandatory!!!
    if sum_m2 < needs_for_type:
        return 0

"""
for MIN_CONFLICT case: when need to evaluate per building
"""
# TODO: implemnt
def calc_plan_building_score_needs(resd_building_obj):
    building_needs_score = 1

    return building_needs_score

########################### COST ##############################

"""
for MIN_CONFLICT case: when need to evaluate per building
"""
"""
example, if I have 10 floors, and added:
  <=2 floors. multiply score by 1 (best score!)
  = 3 floors. multiply score by
  = 12 floors. multiply score by min(COST_MORE_NUM_FLOORS, score*(COST_MORE_PRSTG)^(extra_floors))
"""
# TODO: TO CHECK IMPLEMENTATION
def calc_plan_building_score_cost(resd_building_obj):
    building_cost_score = 1

    resd_init_floors = resd_building_obj.init_height
    resd_extra_floors = resd_building_obj.extra_height

    ratio = resd_extra_floors/resd_init_floors
    floor_prctg_score = 1

    if ratio >= FLOORS_PRCTG:
        extra_extra = resd_extra_floors - PERCENTAGE * FLOORS_PRCTG
        cost_more_prct_extra_extra_floor = pow(COST_MORE_PRSTG, extra_extra)
        floor_prctg_score = cost_more_prct_extra_extra_floor

    if resd_extra_floors + resd_init_floors > COST_MORE_NUM_FLOORS:
        building_cost_score = min(floor_prctg_score, COST_MORE_NUM_FLOORS)

    return building_cost_score


class EvaluatePlan(object):
    """
    :param building_data: List< String, List<Building>>: i.e [(kindergarden, [B1, B2, ..]), ((hospital, [B7, B8, ..])), ...]
    :param plan_floors_state: List< building_type, List<(String:building_id, int:num_of_floors)>>
    includes all (residential & public) values of ONLY heights (num of floors) as object
    :param all_needs: Dist<building_type, int>, building_type: as in building_types.py, int: num of units.
    """
    def __init__(self, buildings_data, plan_floors_state, all_needs):

        self.buildings_data = buildings_data
        self.buildings_data_resd = building_types.find_buildings_in_type(building_types.RESIDENTIAL, buildings_data)
        self.buildings_data_public = building_types.find_buildings_public(building_types.RESIDENTIAL, buildings_data)
        self.plan_floors_state = plan_floors_state
        self.all_needs = all_needs

        self.plan_needs = -1
        self.plan_distance = -1
        self.plan_cost = -1

    """
    in this case we do it for min-conflict: we need to evaluate for each building it's score (higher = better value)
    """
    # TODO: TO CHECK IMPLEMENTATION
    def calc_plan_building(self, resd_building_obj, resd_building_extra_floors):

        score_needs = calc_plan_building_score_needs(resd_building_obj) / self.calc_plan_needs()
        score_distance = calc_plan_building_score_distance(resd_building_obj) / self.calc_plan_distance()
        score_cost = calc_plan_building_score_cost(resd_building_obj) * COST_PRCTG / self.calc_plan_cost()

        return (score_needs * NEEDS_PRCTG) + (score_distance * DISTANCE_PERCTG) + (score_cost * COST_PRCTG)

    ################################### EVALUATE OVERALL PLAN ###################################

    # TODO finish implementation
    def __calc_plan_cost(self):
        # already calculated:
        if self.plan_cost != -1:
            return self.plan_cost

        # first time, should calculate it
        self.plan_cost = 1
        for building in self.plan_floors_state:
            # TODO implement

            self.plan_cost *= 1  #max(evaluated_for_type / needs_for_type, 1)
        return self.plan_cost

    # TODO TO CHECK IMPLEMENTATION, few questions
    def __calc_plan_needs(self):
        # already calculated:
        if self.plan_needs != -1:
            return self.plan_needs

        # first time, should calculate it
        self.plan_needs = 1
        # for all buildings, including residential and public!!
        for b_type in building_types.all_building_types():
            # TODO: Naama: Temp untill we have 'Needs' finished, temporarily = 10
            needs_for_type = 10  # self.all_needs.get_needs_for_type(b_type)
            # TODO: Naama: Future suggestion: different weights for different public buildings (user request!!)
            evaluated_for_type = self.evaluate_plan_needs_for_type(b_type, needs_for_type)

            # TODO: Naama: in case of better conditions than what is needed, still having 1 as rank ???
            # TODO: Naama: maybe if ratio>1, than take ratio-1 ???
            self.plan_needs *= max(evaluated_for_type / needs_for_type, 1)
        return self.plan_needs

    # TODO TO CHECK IMPLEMENTATION, few questions
    def __calc_plan_distance(self):
        # if already calculated:
        if self.plan_distance != -1:
            return self.plan_distance

        # first time, should calculate it
        self.plan_distance = 1
        # loop over only public buildings!!
        for b_type in self.data_buildings_public:
            buildings_in_type = building_types.find_buildings_in_type(b_type)
            # TODO: Naama: Future suggestion: different weights for different public buildings (user request!!)
            evaluated_for_type = evaluate_buildings_distances_for_type(self.buildings_data_resd, self.plan_floors_state, buildings_in_type)

            self.plan_distance *= max(evaluated_for_type, 1)

        return self.plan_distance

    # TODO: TO CHECK IMPLEMENTATION
    def calc_plan_score(self):
        # weighted evaluation
        return self.calc_plan_needs() * NEEDS_PRCTG + \
               self.calc_plan_distance() * DISTANCE_PERCTG + \
               self.calc_plan_cost() * COST_PRCTG


