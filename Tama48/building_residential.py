import building
import building_types as bt

class Residential(building.Building):
    def __init__(self, building_id, area, location, init_height, polygon):
        building.Building.__init__(self, building_id, bt.RESIDENTIAL, area, location, init_height, polygon)
        self.__public_buildings_dist_ordered = dict()
        self.used_public_buildings = [] #TODO - implement the choosing of one building per type

    def calculate_used_public_buildings(self):
        pass #TODO implement

    def add_used_public_building(self, public_building, dist):
        self.used_public_buildings.append((public_building,dist))

    def set_used_public_buildings(self, public_buildings):
        self.used_public_buildings = public_buildings

    def get_used_public_buildings(self):
        return self.used_public_buildings