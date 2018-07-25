import evaluate_plan

class State(object):
    """
    buildings_data
    """
    def __init__(self, buildings_data, additional_floors, additional_floors_resd, all_needs):
        self.buildings_data = buildings_data
        self.additional_floors_resd = additional_floors_resd
        self.additional_floors = []

        self.eval_plan = evaluate_plan.EvaluatePlan(buildings_data, additional_floors, all_needs)
        self.score = self.calc_score()

    # returns the score of this state
    def get_score(self):
        return self.score

    def calc_public_state(self):
        self.additional_floors.append(("residential", self.additional_floors_resd))
        buildings_in_type = [building[1] for building in self.building_data if building[0] != "residential"][0]

    def calc_score(self):
        self.calc_public_state()
        return 0 #TODO implement

    def get_heights_to_add(self):
        return self.additional_floors_resd

    def get_building_data(self):
        return self.buildings_data