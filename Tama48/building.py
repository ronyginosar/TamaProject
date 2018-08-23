"""
Created on July 2, 2018

@author: Naama
"""
import math

FLOOR_HEIGHT = 3

class Location(object):
    # longitude, latitude represent a location in the globe, altitude represent the altitude in respect to the sea level
    def __init__(self, x, y, alt):
        self.x = x
        self.y = y
        self.alt = alt


class Building(object):
    def __init__(self, building_id, building_type, area, location, init_height, polygon):
        """
        Constructor
        """
        self.__id = building_id
        self.__building_type = building_type
        self.__area = area
        self.__location = location
        # List of triples: (x,y,alt)
        self.__polygon = polygon
        self.__init_floors = math.ceil(init_height/FLOOR_HEIGHT)
        self.__added_floors = 0

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.__id == other.__id)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "B_" + str(self.__building_type) + "_" + str(self.__id)

    # def calc__public_building_dist_ordered(self, all_building_data):
    #     for b_type in bt.ALL_PUBLIC_BUILDING_TYPES:
    #         dist_buildings_in_type = [(building.get_id(), util.calc_distance_two_buildings(self, building))
    #                                   for building in bt.find_buildings_in_type(b_type, all_building_data)]
    #         # sort public building by distance, ordered: closest to farther..
    #         self.__public_buildings_dist_ordered[b_type] = sorted(dist_buildings_in_type, key=lambda x: x[1])

    def get_id(self):
        return self.__id

    def get_type(self):
        return self.__building_type

    def get_area(self):
        return self.__area

    def get_location(self):
        return self.__location

    def get_polygon(self):
        return self.__polygon

    def get_init_height(self):
        return self.__init_floors

    def get_extra_height(self):
        return self.__added_floors

    def set_extra_height(self, extra_floors):
        self.__added_floors = math.ceil(extra_floors)

    def add_extra_height(self, extra_extra_floors):
        self.__added_floors += math.ceil(extra_extra_floors)

    def get_overall_area(self):
        return self.get_overall_height() * self.__area

    def get_overall_height(self):
        return (self.__init_floors + self.__added_floors)


