import building
import util
import needs

class PublicBuilding(building.Building):

    def __init__(self, building_id, area, type, location, init_height, pub_type_list):
        building.Building.__init__(self, building_id, type, area, location, init_height, pub_type_list)
        self.__users_buildings = []

    def set_users_buildings(self, users_buildings):
        self.__users_buildings = users_buildings

    def get_users_buildings(self):
        return self.__users_buildings

    '''
    returns the population size using this public building
    '''
    def get_using_population(self):
        return util.calc_pop_size(self.__users_buildings)

    def calc_conflicts(self):
        pass


###-------------------------------------------*(**)*---------------------------------------------###

IDEAL_SIZE_PER_PERSON = 0.1

class Clinic(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, pub_type_list):
        PublicBuilding.__init__(self, building_id, 'clinic', area, location, init_height, pub_type_list)

    # conflicts calculation will be done as follows:
    # more than 0.1 m^2 per person = 0
    # else - 1 conflict point per 0.01 m^2 shortage
    def calc_conflicts(self):
        area_per_person = self.get_overall_area()/self.get_using_population()
        conflict_points = int((IDEAL_SIZE_PER_PERSON - area_per_person)*(10/IDEAL_SIZE_PER_PERSON))
        if conflict_points <= 0:
            return 0
        else:
            return conflict_points


###-------------------------------------------*(**)*---------------------------------------------###

PERCENTAGE_OF_USERS_FROM_POPULATION = 0.2
IDEAL_AREA_PER_USER_COMMUNITY = 0.5

class CommunityCenter(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, pub_type_list):
        PublicBuilding.__init__(self, building_id, 'community_center', area, location, init_height, pub_type_list)

    def calc_conflicts(self):
        num_users = int(self.get_using_population() * PERCENTAGE_OF_USERS_FROM_POPULATION)
        area_per_person = self.get_overall_area()/num_users
        conflict_points = int((IDEAL_AREA_PER_USER_COMMUNITY - area_per_person)*(10/IDEAL_AREA_PER_USER_COMMUNITY))
        if conflict_points <= 0:
            return 0
        else:
            return conflict_points


###-------------------------------------------*(**)*---------------------------------------------###

ELDERLY_PERCENTAGE_FROM_POPULATION = 0.11
PERCENTAGE_OF_ELDERLY_USERS_FROM_POPULATION = 0.15 * ELDERLY_PERCENTAGE_FROM_POPULATION
IDEAL_AREA_PER_USER_ELDERLY = 1

class ElderlyCenter(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, pub_type_list):
        PublicBuilding.__init__(self, building_id, 'elderly_center', area, location, init_height, pub_type_list)

    def calc_conflicts(self):
        num_users = int(self.get_using_population() * PERCENTAGE_OF_ELDERLY_USERS_FROM_POPULATION)
        area_per_person = self.get_overall_area()/num_users
        conflict_points = int((IDEAL_AREA_PER_USER_ELDERLY - area_per_person)*(10/IDEAL_AREA_PER_USER_ELDERLY))
        if conflict_points <= 0:
            return 0
        else:
            return conflict_points


###-------------------------------------------*(**)*---------------------------------------------###

IDEAL_CLASS_SIZE = needs.CLASS_SIZE

class HighSchool(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, pub_type_list):
        PublicBuilding.__init__(self, building_id, 'high_school', area, location, init_height, pub_type_list)


    def get_class_size(self):
        pass #TODO implement

    def calc_conflicts(self):
        conflict_points = IDEAL_CLASS_SIZE - self.get_class_size()
        if conflict_points <= 0:
            return 0
        else:
            return conflict_points


###-------------------------------------------*(**)*---------------------------------------------###

class Hospital(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, pub_type_list):
        PublicBuilding.__init__(self, building_id, 'hospital', area, location, init_height, pub_type_list)


    def calc_conflicts(self):
        pass #TODO implement


###-------------------------------------------*(**)*---------------------------------------------###

class Kindergarten(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, pub_type_list):
        PublicBuilding.__init__(self, building_id, 'kindergarten', area, location, init_height, pub_type_list)


    def calc_conflicts(self):
        pass #TODO implement


###-------------------------------------------*(**)*---------------------------------------------###

class Mikve(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, pub_type_list):
        PublicBuilding.__init__(self, building_id, 'mikve', area, location, init_height, pub_type_list)


    def calc_conflicts(self):
        pass #TODO implement


###-------------------------------------------*(**)*---------------------------------------------###

class Police(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, pub_type_list):
        PublicBuilding.__init__(self, building_id, 'police', area, location, init_height, pub_type_list)


    def calc_conflicts(self):
        pass #TODO implement


###-------------------------------------------*(**)*---------------------------------------------###

class PrimarySchool(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, pub_type_list):
        PublicBuilding.__init__(self, building_id, 'primary_school', area, location, init_height, pub_type_list)


    def calc_conflicts(self):
        pass #TODO implement


###-------------------------------------------*(**)*---------------------------------------------###

class Sport(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, pub_type_list):
        PublicBuilding.__init__(self, building_id, 'sport', area, location, init_height, pub_type_list)


    def calc_conflicts(self):
        pass #TODO implement


###-------------------------------------------*(**)*---------------------------------------------###

class Synagogue(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, pub_type_list):
        PublicBuilding.__init__(self, building_id, 'synagogue', area, location, init_height, pub_type_list)


    def calc_conflicts(self):
        pass #TODO implement


