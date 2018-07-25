import evaluate_plan

class State(object):
    """

    """
    def __init__(self, buildings_data, additional_floors, additional_public, all_needs):
        self.buildings_data = buildings_data
        self.additional_floors = additional_floors
        self.pub_floors = additional_public

        all_additional = []

        self.eval_plan = evaluate_plan.EvaluatePlan(buildings_data, additional_floors, all_needs)
        self.score = self.calc_score()

    # returns the score of this state
    def get_score(self):
        return self.score

    def calc_score(self):
        return 0 #TODO implement

    def get_heights_to_add(self):
        return self.additional_floors

    def get_building_data(self):
        return self.buildings_data