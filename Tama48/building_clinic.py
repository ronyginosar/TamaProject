
import public_building

IDEAL_SIZE_PER_PERSON = 0.1

class Clinic(public_building.PublicBuilding):

    def __init__(self, building_id, area, location, init_height, pub_type_list):
        public_building.PublicBuilding.__init__(self, building_id, 'clinic', area, location, init_height, pub_type_list)

    # conflicts calculation will be done as follows:
    # more than 0.1 m^2 per person = 0
    # else - 1 conflict point per 0.01 m^2 shortage
    def calc_conflicts(self):
        area_per_person = self.get_overall_area()/self.get_using_population()
        conflict_points = int((IDEAL_SIZE_PER_PERSON - area_per_person)*(10/IDEAL_SIZE_PER_PERSON))
        if conflict_points <= 0:
            return 0
        else:
            return conflict_points