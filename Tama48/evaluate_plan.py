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
COST_MORE_PRSTG = 0.95
COST_MORE_NUM_FLOORS = 0.1


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
        self.__buildings_data_public = bt.find_buildings_public(init_buildings_data)
        self.__plan_floors_resd_state = plan_floors_resd_state
        self.__all_needs = all_needs
        # TODO: TO ADI: this function is updating the the init_building_data with the new state of additional floors
        # TODO: of ONLY residential buildings. the result will be stores in __updated_building_data_resd
        self.__updated_building_data_resd = bt.update_building_data_with_floors_plan(self.init_buildings_data_resd,
                                                                                  plan_floors_resd_state)
        self.__plan_needs_score = -1
        self.__plan_distance_score = -1
        self.__plan_cost_score = -1

        # CALCULATE PUBLIC PLAN, and update retult in __init_building_data
        # like __init_building_data, updated with extra floors of the given RESIDENTIAL (state), and the calculated PUBLIC
        self.__updated_building_data_all = []
        self.__calculate_public_plan()

    ############################## CALCULATE PUBLIC PLAN ##############################

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


    ############################## EVALUATION AFTER CALCULATION OF PUBLIC PLAN ##############################

    # TODO TO CHECK IMPLEMENTATION,
    def __evaluate_plan_cost(self):
        # already calculated:
        if self.__plan_cost_score != -1:
            return self.__plan_cost_score

        self.__plan_cost_score = 1
        for building in self.__updated_building_data_all:
            original_height = building.get_extra_height()
            extra_height = building.get_extra_height()
            extra_extra = max(extra_height - math.ceil(FLOORS_PRCTG * original_height), 0)
            cost = pow(COST_MORE_PRSTG, extra_extra)
            if extra_height >= FLOORS_NUM:
                cost = min(COST_MORE_NUM_FLOORS, cost)

            self.__plan_cost_score *= cost  # max(evaluated_for_type / needs_for_type, 1)

        return self.__plan_cost_score

    # TODO: TO CHECK IMPLEMENTATION
    def __evaluate_plan_needs(self):
        # already calculated:
        if self.__plan_needs_score != -1:
            return self.__plan_needs_score

        # first time, should calculate it
        self.__plan_needs_score = 1
        # for all buildings, including residential and public!!
        for b_type in bt.all_building_types():
            unit_needs_for_type = self.__all_needs[b_type]
            # TODO: Naama: Future suggestion: different weights for different public buildings (user request!!)

            buildings_in_type = bt.find_buildings_in_type(b_type, self.__init_buildings_data)
            units_for_type = 0
            for building in buildings_in_type:
                units_for_type += building.get_area() * self.__plan_floors_state[building.get_id()]

            # TODO: Naama: in case of better conditions than what is needed, still having 1 as rank ???
            # TODO: Naama: maybe if ratio>1, than take ratio-1 or just to take max(ratio, 1)???
            ratio = 0
            if units_for_type >= unit_needs_for_type:
                ratio = unit_needs_for_type / units_for_type
            else:
                ratio = units_for_type / unit_needs_for_type
            if unit_needs_for_type > 0:
                self.__plan_needs_score *= ratio

        return self.__plan_needs_score

    # TODO: TO CHECK IMPLEMENTATION, few questions
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
                                           * public_building.get_area() * self.__plan_floors_state[public_building.id]
                evaluated_for_type += sum_avg_dist_lst_prob[i] * sum_area_public_building
                # TODO: take sum_avg_dist_lst_prob[i] * sum_area_public_building as output maybe
                # TODO: so it will be good both for evalation and both calc_public_floors...

            self.__plan_distance *= max(evaluated_for_type, 1)

        return self.__plan_distance

    ###################################    FOR OUTER USE    ######################################

    """
    Evaluate full plan, i.e. after public-plan has been calculated
    """
    # TODO: READY
    def evaluate_plan_score(self):
        # weighted evaluation
        return self.__evaluate_plan_needs() * NEEDS_PRCTG + \
               self.__evaluate_plan_distance() * DISTANCE_PERCTG + \
               self.__evaluate_plan_cost() * COST_PRCTG

    """
    get the calculated _updated_building_data, updated with residential and public both.
    """
    # TODO: READY
    def get_updated_building_data_all(self):
        return self.__updated_building_data_all



