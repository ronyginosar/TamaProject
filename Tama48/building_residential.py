import building
import building_types as bt

class Residential(building.Building):
    def __init__(self, building_id, area, location, init_height, polygon):
        building.Building.__init__(self, building_id, bt.RESIDENTIAL, area, location, init_height, polygon)
        self.__public_buildings_dist_ordered = dict()
        # TODO: a dictionary of {building_type : (closest_building, distance)}
        # TODO: for example: {school : (school_1, 150)} for a school that is 150 meters from the building
        self.used_public_buildings = [] #TODO - implement the choosing of one building per type


    def calculate_used_public_buildings(self):
        pass #TODO implement

    def add_used_public_building(self, public_building):
        self.used_public_buildings.append(public_building)

    def set_used_public_buildings(self, public_buildings):
        self.used_public_buildings = public_buildings

    def get_used_public_buildings(self):
        return self.used_public_buildings