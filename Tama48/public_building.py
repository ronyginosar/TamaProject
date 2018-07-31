import building
import util

class PublicBuilding(building.Building):

    def __init__(self, building_id, area, type, location, init_height, pub_type_list):
        building.Building.__init__(self, building_id, type, area, location, init_height, pub_type_list)
        self.__users_buildings = []

    def set_users_buildings(self, users_buildings):
        self.__users_buildings = users_buildings

    def get_users_buildings(self):
        return self.__users_buildings

    '''
    returs the population size using this public building
    '''
    def get_using_population(self):
        return util.calc_pop_size(self.__users_buildings)

    def calc_conflicts(self):
        pass