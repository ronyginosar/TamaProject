import building

class Residential(building.Building):

    def __init__(self, building_id, area, location, init_height, pub_type_list):
        building.Building.__init__(self, building_id, 'residential', area, location, init_height, pub_type_list)
        self.__public_buildings_dist_ordered = dict()
        # TODO: a dictionary of {building_type : (closest_building, distance)}
        # TODO: for example: {school : (school_1, 150)} for a school that is 150 meters from the building
        self.used_public_buildings = [] #TODO - implement the choosing of one building per type


    def calculate_used_public_buildings(self):
        pass #TODO implement

    def get_used_public_buildings(self):
        return self.used_public_buildings