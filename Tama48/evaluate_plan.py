import building_types

"""
cost                    : more than 20% of the height is more expensive in x*money.
                        : more than 12 floors- more expensive by y*money
distance                :
ratio to optimum needs  :
"""

NEEDS_PRCTG = 0.5
DISTANCE_PERCTG = 0.25
COST_PRCTG = 0.25


class EvaluatePlan(object):
    """
    init_state: List< String, List<Building>>: i.e [(kindergarden, [B1, B2, ..]), ((hospital, [B7, B8, ..])), ...]

    plan_floors_state: includes all values of ONLY heights (num of floors) as object i.e
    [(kindergarden, [(b_id=1, h1), (b_id=2, h2), ..]), ((hospital, [(b_id = 7, h7), (b_id=8, h8), ..])), ...]

    needs is an object of Needs. it's a "singleton" for one run,
    i.e for onerequest of additional population, we create this object only once.
    """
    def __init__(self, building_data, plan_floors_state, all_needs):

        self.building_data = building_data
        self.plan_floors_state = plan_floors_state
        self.all_needs = all_needs

        self.plan_needs = -1
        self.plan_distance = -1
        self.plan_cost = -1

    def calc_plan_building_score_needs(self, resd_building_obj):
        # TODO: implemnt
        return 0

    def calc_plan_building_score_distance(self, resd_building_obj):
        # TODO: implemnt
        return 0

    def calc_plan_building_score_cost(self, resd_building_obj):
        # TODO: implemnt
        return 0

    def calc_building_score_given_plan(self, resd_building_obj):
        score_needs = self.calc_plan_building_score_needs(resd_building_obj) / self.calc_plan_needs()
        score_distance = self.calc_plan_building_score_distance(resd_building_obj) / self.calc_plan_distance()
        score_cost = self.calc_plan_building_score_cost(resd_building_obj) * COST_PRCTG / self.calc_plan_cost()

        return (score_needs * NEEDS_PRCTG) + (score_distance * DISTANCE_PERCTG) + (score_cost * COST_PRCTG)


    def calc_plan_score(self):
         # weighted evaluation
        return self.calc_plan_needs() * NEEDS_PRCTG + \
               self.calc_plan_distance() * DISTANCE_PERCTG + \
               self.calc_plan_cost() * COST_PRCTG

    ########################### COST ##############################



    ########################### NEEDS ##############################
    """
    @:param b_type: String, building type from building_types.py
    @:param needs_for_type: float [m^2]
    @:param all_residentials:
    """
    def evaluate_plan_needs_for_type(self, b_type, all_residentials, needs_for_type):
        # TODO: TO CHECK IMPLEMENTATION
        buildings_in_type = building_types.find_buildings_in_type()

        sum_m2 = 0
        if b_type != building_types.RESIDENTIAL:
            for building in buildings_in_type:
                sum_m2 += building.area * \
                          building_types.floors_given_buldingID_type(self.plan_floors_state, building.get_id(), b_type)

        # for now, the requested needs are mandatory!!!
        if sum_m2 < needs_for_type:
            return 0

    def calc_plan_needs(self):
        # already calculated:
        if self.plan_needs != -1:
            return self.plan_needs

        # first time, should calculate it
        self.plan_needs = 1
        for b_type in building_types.all_building_types():
            # TODO: Naama: Temp untill we have 'Needs' finished..
            needs_for_type = 10  # self.all_needs.get_needs_for_type(b_type)  #  temporarily = 10
            evaluated_for_type = self.evaluate_plan_needs_for_type(b_type, needs_for_type)

            # TODO: Naama: in case of better conditions than what is needed, still having 1 as rank ???
            # TODO: Naama: maybe if ratio>1, than take ratio-1 ???
            self.plan_needs *= max(evaluated_for_type / needs_for_type, 1)


    ########################### DISTANCE ##############################

    def calc_distance_two_buildings(self, residential_building, public_building):
        loc1 = residential_building.get_location()
        loc2 = residential_building.get_location()

        euclid_dist = pow(pow(loc1.x - loc2.x, 2) + pow(loc1.y - loc2.y, 2), 0.5)
        return euclid_dist

    def evaluate_by_distance_all_buildings(self, residential_buildings, extra_heights_state, public_buildings_sametype):
        # given all residential building, the new plan for heights, and a list of specific type of public building
        # we return a probability vector over the public building from this type, which is the weighted sum of
        # all residential building' new area (of the new state) * all distances of them to this specific building
        # normalized to 0-1, for probability preferences.

        svg_dist_lst = []
        for public_building in public_buildings_sametype:
            svg_dist = 0.0
            for resi_building in residential_buildings:
                extra_area = extra_heights_state[resi_building.id] * resi_building.area
                svg_dist += self.calc_distance_two_buildings(resi_building, public_building) * extra_area
            svg_dist_lst.append(svg_dist)
        sum_svg_dist_lst = sum(svg_dist_lst)
        sum_svg_dist_lst_prob = [avg_dist / sum_svg_dist_lst for avg_dist in svg_dist_lst]

        # finally, duplicate the probability (importance) of the PUBLIC buildings with its extra height
        i = 0
        ret_val = 0.0
        for public_building in public_buildings_sametype:
            sum_area_public_building = extra_heights_state[public_building.id] \
                                       * public_building.area * extra_heights_state[public_building.id]
            ret_val += sum_svg_dist_lst_prob[i] * sum_area_public_building
        return ret_val

    def calc_plan_distance(self):
        # already calculated:
        if self.plan_distance != -1:
            return self.plan_distance

        # first time, should calculate it
        # return evaluate_by_distance_all_buildings()




