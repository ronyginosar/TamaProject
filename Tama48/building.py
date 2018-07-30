"""
Created on July 2, 2018

@author: Naama
"""
#from enum import Enum
#import copy
#import numpy as np
#import math

# class BuildingType(Enum):
#     # TODO: edit more in details, like different types of public buildings..
#     Private = 0
#     PUBLIC = 1
#     DO_NOT_BUILD = 2
#     PARK = 3
#     OTHER = 4

# class Polygon:
#     def __init__(self):
#          self.polygon_pts = []
#
#     def set_polygon(self, other):
#         self.polygon_pt = copy.deepcopy(other.polygon_pts)
#
#     def get_polygon(self):
#         if (self.polygon_pts):
#             return self.polygon_pts
#         else:
#             return None
#
#     # shoelace formula
#     def polygon_area(self):
#         corners = self.polygon_pts
#         n = len() # of corners
#         area = 0.0
#         for i in range(n):
#             j = (i + 1) % n
#             area += corners[i][0] * corners[j][1]
#             area -= corners[j][0] * corners[i][1]
#         area = abs(area) / 2.0
#         return area
#
#     # Shoelace formula, in Numpy
#     # def polyArea(self, x,y):
#     #     return 0.5*np.abs(np.dot(x,np.roll(y,1))-np.dot(y,np.roll(x,1)))
#     #
#     # # Another option for area
#     # def area_polygon(self, n, s):
#     #     return 0.25 * n * s**2 / math.tan(math.pi/n)


class Location(object):
    # longitude, latitude represent a location in the globe, altitude represent the altitude in respect to the sea level
    def __init__(self, x, y, alt):
        self.x = x
        self.y = y
        self.alt = alt


def create_empty_nearest_public_list(pub_type_list):
    pub_dict = dict()
    for type in pub_type_list:
        pub_dict[type] = (None, None)
    return pub_dict


class Building(object):
    def __init__(self, building_id, building_type, area, location, init_height, pub_type_list):
        """
        Constructor
        """
        self.id = building_id
        self.building_type = building_type
        self.area = area
        self.location = location
        self.init_height = init_height
        self.extra_height = 0
        self.nearest_public_buildings = create_empty_nearest_public_list(pub_type_list) # TODO: a dictionary of
        # TODO {building_type : (closest_building, distance)} for example:
        # TODO {school : (school_1, 150)} for a school that is 150 meters from the building

        # self.building_polygon = building_polygon # on top (roof)

    def calc_building_volume(self):
        return self.area*(self.init_height + self.extra_height)

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.id == other.id)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "B_" + str(self.building_type) + "_" + str(self.id)

    def add_nearest_public_building(self, type, building_object, dist): #TODO: use this function to load data
        self.nearest_public_buildings[type] = (building_object, dist)

    def get_id(self):
        return self.id

    def get_type(self):
        return self.building_type

    def get_area(self):
        return self.area

    def get_location(self):
        return self.location

    def get_init_height(self):
        return self.init_height

    def get_extra_height(self):
        return self.extra_height

    # def __hash__(self):
    #     return hash(self.id)
