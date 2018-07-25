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
        self.all_needs_dict = all_needs_dict

    # TODO: TO CHECK IMPLEMENTATION
    """
    returns the score of this state
    """
    def get_score(self):
        return self.score

    # TODO: TO CHECK IMPLEMENTATION
    """
    return List< building_type, List<(String:building_id, int:num_of_floors)>>
    """
    def calc_public_state(self):
        for b_type in building_types.all_building_types():
            if b_type != building_types.RESIDENTIAL:
                b_public_floors = ep.calc_public_floors(self.buildings_data, self.additional_floors_resd, b_type)
                self.additional_floors.append((b_type, b_public_floors))
            else:
                self.additional_floors.append((building_types.RESIDENTIAL, self.additional_floors_resd))

    # TODO: TO CHECK IMPLEMENTATION
    def calc_score(self):
        self.calc_public_state()
        self.evaluate_plan_obj = ep.EvaluatePlan(self.buildings_data, self.additional_floors, self.all_needs_dict)
        self.score = self.evaluate_plan_obj.calc_plan_score()
        return self.score

    # TODO: To implement
    def evaluate_distance_score(self):
        pass

    # TODO: TO CHECK IMPLEMENTATION
    def get_heights_to_add(self):
        return self.additional_floors_resd

    # TODO: TO CHECK IMPLEMENTATION
    def get_building_data(self):
        return self.buildings_data