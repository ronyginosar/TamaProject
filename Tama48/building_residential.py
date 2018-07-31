import building

class Residential(building.Building):

    def __init__(self, building_id, area, location, init_height, pub_type_list):
        building.Building.__init__(self, building_id, 'residential', area, location, init_height, pub_type_list)