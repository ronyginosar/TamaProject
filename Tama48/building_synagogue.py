import public_building

class Synagogue(public_building.PublicBuilding):

    def __init__(self, building_id, area, location, init_height, pub_type_list):
        public_building.PublicBuilding.__init__(self, building_id, 'synagogue', area, location, init_height, pub_type_list)


    def calc_conflicts(self):
        pass #TODO implement