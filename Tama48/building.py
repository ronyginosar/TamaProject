"""
Created on July 2, 2018

@author: Naama
"""
import math
import util
import building_types as bt

FLOOR_HEIGHT = 3

class Location(object):
    # longitude, latitude represent a location in the globe, altitude represent the altitude in respect to the sea level
    def __init__(self, x, y, alt):
        self.x = x
        self.y = y
        self.alt = alt

# # TODO: Naama
# def create_empty_nearest_public_list(pub_type_list):
#     pub_dict = dict()
#     for type in pub_type_list:
#         pub_dict[type] = (None, None)
#     return pub_dict


class Building(object):
    def __init__(self, building_id, building_type, area, location, init_height, pub_type_list):
        """
        Constructor
        """
        self.__id = building_id
        self.__building_type = building_type
        self.__area = area
        self.__location = location
        self.__init_floors = math.ceil(init_height/FLOOR_HEIGHT)
        self.__added_floors = 0

        self.__public_buildings_dist_ordered = dict()
        # TODO: a dictionary of {building_type : (closest_building, distance)}
        # TODO: for example: {school : (school_1, 150)} for a school that is 150 meters from the building

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.__id == other.__id)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "B_" + str(self.__building_type) + "_" + str(self.__id)

    # TODO: TO Check implementation
    def calc__public_building_dist_ordered(self, all_building_data):
        for b_type in bt.all_public_building_types():
            dist_buildings_in_type = [(building.get_id(), util.calc_distance_two_buildings(self, building))
                                      for building in bt.find_buildings_in_type(b_type, all_building_data)]
            # sort public building by distance
            self.__public_buildings_dist_ordered[b_type] = sorted(dist_buildings_in_type, key=lambda x: x[1])

    def get_id(self):
        return self.__id

    def get_type(self):
        return self.__building_type

    def get_area(self):
        return self.__area

    def get_location(self):
        return self.__location

    def get_init_height(self):
        return self.__init_floors

    def get_extra_height(self):
        return self.__added_floors

    def set_extra_height(self, extra_floors):
        self.__added_floors = math.ceil(extra_floors)

    def get_overall_area(self):
        return (self.__init_floors + self.__added_floors) * self.__area


