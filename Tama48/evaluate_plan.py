import building_types as bt
import util
import copy
import needs
import math

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
:param init_buildings_data- initial param data.
:param additional_floors_resd
:param b_type, public building type to add units
:param all_needs
return: List<int, int>, first int: building_id, second int:number of floors to add.
is a solution for public public from type b_type
"""
# TODO: to implement
def get_public_floors(init_buildings_data, additional_floors_resd, b_type, all_needs):
    public_floors_lst = []

    return public_floors_lst

########################### DISTANCE ##############################

"""
evaluate distance of all buildings from all public buildings from one building_type.
the result is a weighted value

given all residential building, the new plan for heights, and a list of specific type of public building
we return a probability vector over the public building from this type, which is the weighted sum of
all residential building' new area (of the new state) * all distances of them to this specific building
normalized to 0-1, for probability preferences.
"""
# TODO: TO CHECK IMPLEMENTATION
def evaluate_buildings_distances_for_type(updated_building_data_resd, public_buildings_sametype):
    avg_dist_lst = []
    for public_building in public_buildings_sametype:
        avg_dist = 0.0
        for resd_building in bt.find_buildings_in_type(bt.RESIDENTIAL, updated_building_data_resd):
            area = resd_building.get_overall_area()
            avg_dist += util.calc_distance_two_buildings(resd_building, public_building) * area
        avg_dist_lst.append(avg_dist)
    sum_avg_dist_lst = sum(avg_dist_lst)
    sum_avg_dist_lst_prob = [avg_dist / sum_avg_dist_lst for avg_dist in avg_dist_lst]

    return sum_avg_dist_lst_prob

class EvaluatePlan(object):
    """
    :param init_buildings_data: List< String, List<Building>>: i.e [(kindergarden, [B1, B2, ..]), ((hospital, [B7, B8, ..])), ...]
    :param plan_floors_resd_state: List< building_type, List<(String:building_id, int:num_of_floors)>>
    includes all (residential & public) values of ONLY heights (num of floors) as object
    :param all_needs: Dist<building_type, int>, building_type: as in building_types.py, int: num of units.
    """
    def __init__(self, init_buildings_data, plan_floors_resd_state, all_needs):

        self.__init_buildings_data = init_buildings_data
        self.__init_buildings_data_resd = bt.find_buildings_in_type(bt.RESIDENTIAL, init_buildings_data)
        self.__buildings_data_public = bt.find_buildings_public(bt.RESIDENTIAL, init_buildings_data)
        self.__plan_floors_resd_state = plan_floors_resd_state
        self.__all_needs = all_needs
        # TODO: TO ADI: this function is updating the the init_building_data with the new state of additional floors
        # TODO: of ONLY residential buildings. the result will be stores in __updated_building_data_resd
        self.__updated_building_data_resd = bt.update_building_data_with_floors_plan(self.init_buildings_data_resd,
                                                                                  plan_floors_resd_state)

        # TODO: TO ADI: do you need this? I mean an updated state of residential and public #(of floors)?
        self.__plan_floors_state_all = []

        # like __init_building_data, just with the RESIDENTIAL (state) extra floors, and calculated extra PUBLIC floors.
        self.__updated_building_data_all = []

        self.__calculate_public_plan()

        self.__plan_needs_score = -1
        self.__plan_distance_score = -1
        self.__plan_cost_score = -1

    """
    calculate the vector of probabilities for each public type,
    :return: public_plan_prob_vec_per_type_dist is a Dict<Key = public_type, Value = List<float, float, ..>>
    the number of values in the list is as the number of public building from this specific public_type.
    """
    # TODO CHECK IMPLEMENTATION
    def __calculate_public_plan_prob_importance(self):
        # in current situation (before building more floors), we don't know the cost, because it depends on the num
        # of floors, and the needs are mandatory for us. so importance is based on distance only.
        public_plan_prob_vec_per_type_dist = dict()

        # same function used for evaluation (distance parameter), just for planning the public here.
        for public_type in bt.all_public_building_types():
            # it doesnt' matter if it is self.__init_buildings_data or self.__updated_building_data_resd,
            # because the public buildings are not updated anyway..
            public_buildings_sametype = bt.find_buildings_in_type(public_type, self.__init_buildings_data)
            public_plan_prob_vec_per_type_dist[public_type] = evaluate_buildings_distances_for_type\
                (self.__updated_building_data_resd, public_buildings_sametype)

        return public_plan_prob_vec_per_type_dist

    """
    this function is an approximation for a public plan result we want.
    in in this sense, it get the probability vector of importance (based on distances only for now)
    and calculate the number of floors to add for each public building based on this vector,
    as the number of units as required, or more (using ceil for this)
    """
    # TODO CHECK IMPLEMENTATION
    def __calculate_public_plan(self):
        # only for public
        public_plan_prob_vec_per_type = self.__calculate_public_plan_prob_importance()  # ex: <0.5,0.2,0.3> for one type
        self.__updated_building_data_all = copy.deepcopy(self.__updated_building_data_resd)
        add_extra_floors_dict = dict()
        for public_type in bt.all_public_building_types():
            units_needed_for_type = self.__all_needs[public_type]                          # ex: 3 units
            area_per_unit_for_type = needs.one_unit_in_meter_square(public_type)         # ex: 100 m^2 per unit
            area_needed_for_type = units_needed_for_type * area_per_unit_for_type        # ex: 300 m^2 overall
            vec_area_for_type = [prob * area_needed_for_type
                                 for prob in public_plan_prob_vec_per_type[public_type]] # ex: <150,60,90>
            floors_importance_for_type = []
            idx = 0
            for public_building in bt.find_buildings_in_type(public_type, self.__buildings_data_public):
                floors_importance_for_type.append((public_building.get_id(), public_plan_prob_vec_per_type[idx],
                                                   vec_area_for_type[idx] * public_building.get_area()))
                idx += 1
            # sort by importance
            sorted_floors_importance_for_type = sorted(floors_importance_for_type, key=lambda x: x[1])

            add_extra_floors_dict[public_type] = dict()
            left_area = area_needed_for_type
            for (id,imp,floors) in sorted_floors_importance_for_type:
                if left_area <= 0:
                    add_extra_floors_dict.append((id, 0.0))
                else:
                    building = bt.find_buildings_in_type(public_building, id)
                    floors_to_add = min(math.ceil(floors), left_area/building.get_area())
                    add_extra_floors_dict[public_type][id] = floors_to_add
                    left_area -= building.get_area() * floors_to_add

        # update __updated_building_data_all with all public extra heights.
        for building in self.__updated_building_data_all:
            building_type = building.get_type()
            if building_type != bt.RESIDENTIAL:
                building.set_extra_height(add_extra_floors_dict[building_type][building.get_id()])

    # def get_plan_floors_state_all(self):
    #     return self.__plan_floors_state_all

    ############################## EVALUATION AFTER CALCULATION OF PUBLIC PLAN ##############################

    def __calc_plan_cost(self):
        # already calculated:
        if self.__plan_cost_score != -1:
            return self.__plan_cost_score

        # first time, should calculate it
        self.__plan_cost_score = 1
        for building in self.__plan_floors_state:
            # TODO implement
            self.__plan_cost_score *= 1  #max(evaluated_for_type / needs_for_type, 1)

        return self.__plan_cost_score

    # TODO TO CHECK IMPLEMENTATION, few questions
    # TODO: TO CHECK IMPLEMENTATION
    def __evaluate_plan_needs_for_public_type(self, b_type, needs_for_type):

        buildings_in_type = bt.find_buildings_in_type(b_type, self.__init_buildings_data)

        sum_m2 = 0
        if b_type != bt.RESIDENTIAL:
            for building in buildings_in_type:
                sum_m2 += building.area * self.__plan_floors_state[building.get_id()] # * bt.floors_given_buldingID_type(self.__plan_floors_state, building.get_id(), b_type)

        # for now, the requested needs are mandatory!!!
        if sum_m2 < needs_for_type:
            return 0

    def __evaluate_plan_needs(self):
        # already calculated:
        if self.__plan_needs_score != -1:
            return self.__plan_needs_score

        # first time, should calculate it
        self.__plan_needs_score = 1
        # for all buildings, including residential and public!!
        for b_type in bt.all_building_types():
            # TODO: Naama: Temp untill we have 'Needs' finished, temporarily = 10
            needs_for_type = 10  # self.__all_needs.get_needs_for_type(b_type)
            # TODO: Naama: Future suggestion: different weights for different public buildings (user request!!)
            evaluated_for_type = self.__evaluate_plan_needs_for_public_type(b_type, needs_for_type)

            # TODO: Naama: in case of better conditions than what is needed, still having 1 as rank ???
            # TODO: Naama: maybe if ratio>1, than take ratio-1 ???
            self.__plan_needs_score *= max(evaluated_for_type / needs_for_type, 1)
        return self.__plan_needs_score

    # TODO TO CHECK IMPLEMENTATION, few questions
    def __evaluate_plan_distance(self):
        # if already calculated:
        if self.__plan_distance != -1:
            return self.__plan_distance

        # first time, should calculate it
        self.__plan_distance = 1
        # loop over only public buildings!!
        for b_type in bt.all_public_building_types():
            buildings_in_type = bt.find_buildings_in_type(b_type)
            # TODO: Naama: Future suggestion: different weights for different public buildings (user request!!)
            sum_avg_dist_lst_prob = evaluate_buildings_distances_for_type(self.__updated_building_data_resd, buildings_in_type)

            # finally, duplicate the probability (importance) of the PUBLIC buildings with its extra height
            i = 0
            evaluated_for_type = 0.0
            for public_building in buildings_in_type:
                sum_area_public_building = self.__plan_floors_state[public_building.id] \
                                           * public_building.area * self.__plan_floors_state[public_building.id]
                evaluated_for_type += sum_avg_dist_lst_prob[i] * sum_area_public_building
                # TODO: take sum_svg_dist_lst_prob[i] * sum_area_public_building as output maybe
                # TODO: so it will be good both for evalation and both calc_public_floors...

            self.__plan_distance *= max(evaluated_for_type, 1)

        return self.__plan_distance

    """
    Evaluate full plan, i.e. after public-plan has been calculated
    """
    # TODO: READY
    def evaluate_plan_score(self):
        # weighted evaluation
        self.__evaluate_plan_needs()
        self.__evaluate_plan_distance()
        self.__evaluate_plan_cost()
        return (self.__plan_needs * NEEDS_PRCTG) +\
               (self.__plan_distance * DISTANCE_PERCTG) +\
               (self.__plan_cost * COST_PRCTG)

    """
    get the calculated _updated_building_data, updated with residential and public both.
    """
    # TODO: READY
    def get_updated_building_data_all(self):
        return self.__updated_building_data_all

    # TODO: READY
    def get_updated_building_data_floors_state(self):
        return self.__plan_floors_state_all


