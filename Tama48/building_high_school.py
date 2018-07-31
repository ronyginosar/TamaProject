import public_building
import needs

IDEAL_CLASS_SIZE = needs.CLASS_SIZE

class HighSchool(public_building.PublicBuilding):

    def __init__(self, building_id, area, location, init_height, pub_type_list):
        public_building.PublicBuilding.__init__(self, building_id, 'high_school', area, location, init_height, pub_type_list)


    def get_class_size(self):
        self.get_overall_area()/
        return 0

    def calc_conflicts(self):
        conflict_points = IDEAL_CLASS_SIZE - self.get_class_size()
        if conflict_points <= 0:
            return 0
        else:
            return conflict_points