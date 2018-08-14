import math
import util
import building_types as bt

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
SPORT =  'sport'
SYNAGOUGE = 'synagogue'



person_types = []

#     return [CLINIC, COMMUNITY_CNTR, ELDERLY_CNTR, HIGH_SCHOOL, HOSPITAL, KINDERGARDEN, MIKVE,
#                               POLICE, PRIMARY_SCHOOL, SPORT, SYNAGOUGE]


class Person(object):
    def __init__(self, person_id, person_type, religious = False):
        """
        Constructor
        """
        self.__id = person_id
        self.__person_type = person_type
        self.__religious = religious
        self.__satisfaction = 1

    def get_id(self):
        return self.__id

    def get_type(self):
        return self.__person_type

    def get_satisfaction(self):
        return self.__satisfaction

    def set_residence(self, residence):
        self.__residence = residence

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

    #single people need community, sport, clinic
    def set_single_satisfaction(self):
        satisfaction = 1
        used_buildings = self.__residence.get_used_public_buildings()

        for (building,distance) in used_buildings:
            if building.get_type() == CLINIC:
                if distance < 300:
                    satisfaction *= 1
                else:
                    satisfaction *=.5
            if building.get_type() == COMMUNITY_CNTR:
                if distance < 300:
                    satisfaction *= 1
                else:
                    satisfaction *=.5
            if building.get_type() == SPORT:
                if distance < 300:
                    satisfaction *= 1
                else:
                    satisfaction *=.5
        self.__satisfaction = satisfaction

    #parent need all schools, clinic, police
    def get_parent_satisfaction(self):
        satisfaction = 1
        used_buildings = self.__residence.get_used_public_buildings()

        for (building,distance) in used_buildings:
            if building.get_type() == KINDERGARDEN:
                if distance < 300:
                    satisfaction *= 1
                else:
                    satisfaction *=.5
            if building.get_type() == PRIMARY_SCHOOL:
                if distance < 300:
                    satisfaction *= 1
                else:
                    satisfaction *=.5
            if building.get_type() == HIGH_SCHOOL:
                if distance < 300:
                    satisfaction *= 1
                else:
                    satisfaction *=.5
            if building.get_type() == CLINIC:
                if distance < 300:
                    satisfaction *= 1
                else:
                    satisfaction *=.5
            if building.get_type() == POLICE:
                if distance < 300:
                    satisfaction *= 1
                else:
                    satisfaction *=.5
        self.__satisfaction = satisfaction

    #child needs at least one school, sport, community
    def get_child_satisfaction(self):
        satisfaction = 1
        used_buildings = self.__residence.get_used_public_buildings()

        for (building,distance) in used_buildings:
            if building.get_type() == KINDERGARDEN:
                if distance < 300:
                    satisfaction *= 1
                else:
                    satisfaction *=.5
            if building.get_type() == PRIMARY_SCHOOL:
                if distance < 300:
                    satisfaction *= 1
                else:
                    satisfaction *=.5
            if building.get_type() == HIGH_SCHOOL:
                if distance < 300:
                    satisfaction *= 1
                else:
                    satisfaction *=.5
            if building.get_type() == COMMUNITY_CNTR:
                if distance < 300:
                    satisfaction *= 1
                else:
                    satisfaction *=.5
            if building.get_type() == SPORT:
                if distance < 300:
                    satisfaction *= 1
                else:
                    satisfaction *=.5
        self.__satisfaction = satisfaction

    #elderly needs hospital, elderly, community
    def get_elderly_satisfaction(self):

        satisfaction = 1
        used_buildings = self.__residence.get_used_public_buildings()

        for (building,distance) in used_buildings:
            if building.get_type() == HOSPITAL:
                if distance < 300:
                    satisfaction *= 1
                else:
                    satisfaction *=.5
            if building.get_type() == ELDERLY_CNTR:
                if distance < 300:
                    satisfaction *= 1
                else:
                    satisfaction *=.5
            if building.get_type() == COMMUNITY_CNTR:
                if distance < 300:
                    satisfaction *= 1
                else:
                    satisfaction *=.5
        self.__satisfaction = satisfaction

    def update_if_religious_satisfaction(self):
        used_buildings = self.__residence.get_used_public_buildings()

        for (building,distance) in used_buildings:
            if building.get_type() == MIKVE:
                if distance < 300:
                    self.__satisfaction *= 1
                else:
                    self.__satisfaction *=.5
            if building.get_type() == SYNAGOUGE:
                if distance < 300:
                    self.__satisfaction *= 1
                else:
                    self.__satisfaction *=.5







