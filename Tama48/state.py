import evaluate_plan as ep
import building_types

class State(object):
    """
    init State CTOR
    @:param buildings_data- List<(string, List<Building>>, string:building_type (from building_types.py file)
    @:param all_needs_dict- dict<string, int>, string:building_type, int:num_of_units
    @:param additional_floors_resd- List<int, int>, first int: building_id, second int:number of floors to add.
    """
    def __init__(self, buildings_data, additional_floors_resd, all_needs_dict):
        self.buildings_data = buildings_data
        self.additional_floors_resd = additional_floors_resd
        self.additional_floors = []
        self.evaluate_plan_obj = None
        self.score = self.calc_score()

    # returns the score of this state
    def get_score(self):
        return self.score

    def calc_public_state(self):
        #TODO: to implement!
        self.additional_floors.append(("residential", self.additional_floors_resd))

        b_public_types = [b_type for b_type in building_types.all_building_types()
                          if b_type != building_types.RESIDENTIAL][0]
    def calc_score(self):
        self.calc_public_state()
        self.evaluate_plan_obj = ep.EvaluatePlan(self.buildings_data, self.additional_floors, self.all_needs_dict)
        self.score = building_types.DISTANCE_PERCTG * self.evaluate_plan_obj.calc_plan_score()
        return self.score

    def evaluate_distance_score(self):
        pass

    def get_heights_to_add(self):
        return self.additional_floors_resd

    def get_building_data(self):
        return self.buildings_data