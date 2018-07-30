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
import building_types as bt
import util

class Location(object):
    # longitude, latitude represent a location in the globe, altitude represent the altitude in respect to the sea level
    def __init__(self, x, y, alt):
        self.x = x
        self.y = y
        self.alt = alt

# TODO: Naama
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
        self.nearest_public_buildings = create_empty_nearest_public_list(pub_type_list)
        # TODO: a dictionary of {building_type : (closest_building, distance)}
        # TODO: for example: {school : (school_1, 150)} for a school that is 150 meters from the building

    def __eq__(self, other):
        return (isinstance(other, self.__class__) and self.id == other.id)

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        return "B_" + str(self.building_type) + "_" + str(self.id)

    # TODO: TO Check implementation
    def all_types_nearest_public_building(self, building_data):
        for b_type in bt.all_building_types():
            if b_type != bt.RESIDENTIAL:
                closest_building_per_type = None
                min_distance_per_type = float('inf')
                for building in bt.find_buildings_in_type(b_type, building_data):
                    dist = util.calc_distance_two_buildings(self, building)
                    if dist < min_distance_per_type:
                        min_distance_per_type = dist
                        closest_building_per_type = building
                self.add_nearest_public_building(b_type, closest_building_per_type, dist)

    # TODO: use this function to load data
    def add_nearest_public_building(self, type, building_object, dist):
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

    def get_overall_volume(self):
        return (self.init_height + self.extra_height) * self.area

    # def __hash__(self):
    #     return hash(self.id)
