import public_building

PERCENTAGE_OF_USERS_FROM_POPULATION = 0.2
IDEAL_AREA_PER_USER = 0.5

class CommunityCenter(public_building.PublicBuilding):

    def __init__(self, building_id, area, location, init_height, pub_type_list):
        public_building.PublicBuilding.__init__(self, building_id, 'community_center', area, location, init_height, pub_type_list)

    def calc_conflicts(self):
        num_users = int(self.get_using_population()*PERCENTAGE_OF_USERS_FROM_POPULATION)
        area_per_person = self.get_overall_area()/num_users
        conflict_points = int((IDEAL_AREA_PER_USER - area_per_person)*(10/IDEAL_AREA_PER_USER))
        if conflict_points <= 0:
            return 0
        else:
            return conflict_points