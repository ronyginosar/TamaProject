import building
import util
import needs
import building_types as bt

class PublicBuilding(building.Building):

    def __init__(self, building_id, b_type, area, location, init_height, polygon):
        building.Building.__init__(self, building_id, b_type, area, location, init_height, polygon)
        # list of residential building which are using this public building (among other public building in this type)
        self.__users_buildings = []

    def set_users_buildings(self, users_buildings):
        self.__users_buildings = users_buildings

    def add_user_buildings(self, user_building):
        self.__users_buildings.append(user_building)

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

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.CLINIC, area, location, init_height, polygon)

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

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.COMMUNITY_CNTR, area, location, init_height, polygon)

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

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.ELDERLY_CNTR, area, location, init_height, polygon)

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

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.HIGH_SCHOOL, area, location, init_height, polygon)


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

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.HOSPITAL, area, location, init_height, polygon)


    def calc_conflicts(self):
        return 0 #TODO implement


###-------------------------------------------*(**)*---------------------------------------------###

class Kindergarden(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.KINDERGARDEN, area, location, init_height, polygon)


    def calc_conflicts(self):
        return 0 #TODO implement


###-------------------------------------------*(**)*---------------------------------------------###

class Mikve(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.MIKVE, area, location, init_height, polygon)


    def calc_conflicts(self):
        return 0 #TODO implement


###-------------------------------------------*(**)*---------------------------------------------###

class Police(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.POLICE, area, location, init_height, polygon)


    def calc_conflicts(self):
        return 0 #TODO implement


###-------------------------------------------*(**)*---------------------------------------------###

class PrimarySchool(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.PRIMARY_SCHOOL, area, location, init_height, polygon)


    def calc_conflicts(self):
        return 0 #TODO implement


###-------------------------------------------*(**)*---------------------------------------------###

class Sport(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.SPORT, area, location, init_height, polygon)


    def calc_conflicts(self):
        return 0 #TODO implement


###-------------------------------------------*(**)*---------------------------------------------###

class Synagogue(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.SYNAGOUGE, area, location, init_height, polygon)


    def calc_conflicts(self):
        return 0 #TODO implement


