#import needs
#import math

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
