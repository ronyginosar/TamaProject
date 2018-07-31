"""
Created on July 2, 2018

@author: Naama
"""
import math

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
        self.__init_height = init_height
        self.__extra_height = 0

        #self.__nearest_public_buildings = create_empty_nearest_public_list(pub_type_list)
        # TODO: a dictionary of {building_type : (closest_building, distance)}
        # TODO: for example: {school : (school_1, 150)} for a school that is 150 meters from the building

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.__id == other.__id)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "B_" + str(self.__building_type) + "_" + str(self.__id)

    # TODO: TO Check implementation
    # def all_types_nearest_public_building(self, building_data):
    #     for b_type in bt.all_building_types():
    #         if b_type != bt.RESIDENTIAL:
    #             closest_building_per_type = None
    #             min_distance_per_type = float('inf')
    #             for building in bt.find_buildings_in_type(b_type, building_data):
    #                 dist = util.calc_distance_two_buildings(self, building)
    #                 if dist < min_distance_per_type:
    #                     min_distance_per_type = dist
    #                     closest_building_per_type = building
    #             self.add_nearest_public_building(b_type, closest_building_per_type, dist)

    # TODO: use this function to load data
    # def add_nearest_public_building(self, type, building_object, dist):
    #     self.__nearest_public_buildings[type] = (building_object, dist)

    def get_id(self):
        return self.__id

    def get_type(self):
        return self.__building_type

    def get_area(self):
        return self.__area

    def get_location(self):
        return self.__location

    def get_init_height(self):
        return self.__init_height

    def get_extra_height(self):
        return self.__extra_height

    def set_extra_height(self, extra_floors):
        self.__extra_height = math.ceil(extra_floors)

    def get_overall_area(self):
        return (self.__init_height + self.__extra_height) * self.__area


