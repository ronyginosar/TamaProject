import math
import util
import public_building as pb
import building_types as bt
import numpy as np

SINGLE = "single"
PARENT = "parent"
CHILD = "child"
ELDERLY = "elderly"

CLINIC = 'clinic'
COMMUNITY_CNTR = 'community_center'
ELDERLY_CNTR = 'elderly_center'
HIGH_SCHOOL = 'high_school'
HOSPITAL = 'hospital'
KINDERGARDEN = 'kindergarden'
MIKVE = 'mikve'
POLICE = 'police'
PRIMARY_SCHOOL = 'primary_school'
RESIDENTIAL = 'residential'
SPORT = 'sport'
SYNAGOUGE = 'synagogue'

person_types = []


class Person(object):
    def __init__(self, person_type, religious=False):
        """
        Constructor
        """
        self.__person_type = person_type
        self.__religious = religious
        self.__satisfaction = 1

    def get_type(self):
        return self.__person_type

    def get_satisfaction(self):
        return self.__satisfaction

    def get_religious(self):
        return self.__religious

    # residence is the building where the person resides
    def set_residence(self, residence):
        self.__residence = residence

    def get_residence(self):
        return self.__residence.get_id()

    def set_satisfaction(self):
        if self.__person_type == SINGLE:
            self.set_single_satisfaction()
        elif self.__person_type == PARENT:
            self.set_parent_satisfaction()
        elif self.__person_type == CHILD:
            self.set_child_satisfaction()
        elif self.__person_type == ELDERLY:
            self.set_elderly_satisfaction()

        if self.__religious:
            self.update_if_religious_satisfaction()
        return self.__satisfaction

    # single people need community, sport, clinic
    def set_single_satisfaction(self):
        satisfaction = 1
        used_buildings = self.__residence.get_used_public_buildings()
        for (building, distance) in used_buildings:
            if (building.get_type() == CLINIC) or \
                (building.get_type() == COMMUNITY_CNTR) or\
                (building.get_type() == POLICE) or\
                (building.get_type() == SPORT):
                dist = (1000-distance)/1000
                satisfaction *=  (max(dist, pb.calc_score_for_persons(building)))
                # satisfaction *=  dist    
        self.__satisfaction = satisfaction

    # parent need all schools, clinic, police
    def set_parent_satisfaction(self):
        satisfaction = 1
        used_buildings = self.__residence.get_used_public_buildings()
    
        for (building, distance) in used_buildings:
            if (building.get_type() == KINDERGARDEN) or \
                (building.get_type() == PRIMARY_SCHOOL) or \
                (building.get_type() == HIGH_SCHOOL) or \
                (building.get_type() == CLINIC) or \
                (building.get_type() == POLICE):
                dist = (1000-distance)/1000
                satisfaction *=  (max(dist, pb.calc_score_for_persons(building)))
                # satisfaction *=  dist

        self.__satisfaction = satisfaction

    # child needs school, sport, community
    def set_child_satisfaction(self):
        satisfaction = 1
        used_buildings = self.__residence.get_used_public_buildings()
        for (building, distance) in used_buildings:
            
            if (building.get_type() == KINDERGARDEN) or \
                (building.get_type() == PRIMARY_SCHOOL) or \
                (building.get_type() == HIGH_SCHOOL) or \
                (building.get_type() == COMMUNITY_CNTR) or \
                (building.get_type() == POLICE):
                dist = (1000-distance)/1000
                satisfaction *=  (max(dist, pb.calc_score_for_persons(building)))
                # satisfaction *=  dist

        self.__satisfaction = satisfaction

    # elderly needs hospital, elderly, community
    def set_elderly_satisfaction(self):

        satisfaction = 1
        used_buildings = self.__residence.get_used_public_buildings()

        for (building, distance) in used_buildings:
            
            if (building.get_type() == HOSPITAL) or \
                (building.get_type() == ELDERLY_CNTR) or \
                (building.get_type() == COMMUNITY_CNTR) or \
                (building.get_type() == CLINIC):
                dist = (1000-distance)/1000
                satisfaction *=  (max(dist, pb.calc_score_for_persons(building)))
                # # satisfaction *=  (average(dist, building.get_building_score()))
                # satisfaction *=  dist

        self.__satisfaction = satisfaction

    def update_if_religious_satisfaction(self):
        used_buildings = self.__residence.get_used_public_buildings()

        for (building, distance) in used_buildings:
            if (building.get_type() == MIKVE) or \
                (building.get_type() == SYNAGOUGE):
                dist = (1000-distance)/1000
                self.__satisfaction *=  (max(dist, pb.calc_score_for_persons(building)))

                    # self.__satisfaction *=  (average(dist, building.get_building_score()))
                    # self.__satisfaction *=  dist


def average(a,b):
    return (a+b)/2 
