import evaluate_plan as ep
import building_types as bt

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
        self.additional_floors_all = []
        self.all_needs_dict = all_needs_dict
        self.evaluate_plan_obj = ep.EvaluatePlan(self.buildings_data, self.additional_floors_resd, self.all_needs_dict)
        self.score = self.evaluate_plan_obj.evaluate_plan_score()

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
    def get_floor_state(self):
        if not self.additional_floors_all:
            self.updated_building_data = self.evaluate_plan_obj.get_updated_building_data_all()
            for b_type in bt.all_building_types():
                if b_type != bt.RESIDENTIAL:
                    additional_floors_for_type = [building.get_extra_height()
                                      for building in bt.find_buildings_in_type(b_type, self.updated_building_data)]
                    self.additional_floors_all.append((b_type, additional_floors_for_type))
                else:
                    self.additional_floors_all.append((bt.RESIDENTIAL, self.additional_floors_resd))
        return self.additional_floors_all

    def add_floor(self, building_to_increase, num_floors_to_add):
        self.additional_floors_resd[building_to_increase.get_id()] += num_floors_to_add

    # TODO: TO CHECK IMPLEMENTATION
    def get_heights_to_add(self):
        return self.additional_floors_resd

    # TODO: TO CHECK IMPLEMENTATION
    def get_building_data(self):
        return self.buildings_data