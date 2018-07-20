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
    def __init__(self, init_state, plan_hights_state, needs):

        self.init_state = init_state
        self.plan_hights_state = plan_hights_state
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
                sum_m2 += building.area * self.plan_hights_state[idx]

                # add another function between 0-1 related to the distances..

                # more??

                idx += 1
        else:
            # maybe to check something else, in this case, it is mandatory to have number of meters per person...
            pass
