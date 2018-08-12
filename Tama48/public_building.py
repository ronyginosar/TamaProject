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

    def calc_building_score(self, building_type_needs_meters):
        # (all using-resd-building * their area ) * this public area
        using_area = [using_rsd.get_overall_area() for using_rsd in self.get_users_buildings()]
        used_area_meters = sum(using_area)
        return min(float(used_area_meters/building_type_needs_meters), float(building_type_needs_meters/used_area_meters))

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

    def calc_building_score(self, all_needs):
        this_needs = all_needs.get(bt.CLINIC)
        return PublicBuilding.calc_building_score(self, this_needs)

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

    def calc_building_score(self, all_needs):
        this_needs = all_needs.get(bt.COMMUNITY_CNTR)
        return PublicBuilding.calc_building_score(self, this_needs)


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

    def calc_building_score(self, all_needs):
        this_needs = all_needs.get(bt.ELDERLY_CNTR)
        return PublicBuilding.calc_building_score(self, this_needs)

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

    def calc_building_score(self, all_needs):
        this_needs = all_needs.get(bt.HIGH_SCHOOL)
        return PublicBuilding.calc_building_score(self, this_needs)


###-------------------------------------------*(**)*---------------------------------------------###

class Hospital(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.HOSPITAL, area, location, init_height, polygon)


    def calc_conflicts(self):
        return 0 #TODO implement

    def calc_building_score(self, all_needs):
        this_needs = all_needs.get(bt.HOSPITAL)
        return PublicBuilding.calc_building_score(self, this_needs)


###-------------------------------------------*(**)*---------------------------------------------###

class Kindergarden(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.KINDERGARDEN, area, location, init_height, polygon)


    def calc_conflicts(self):
        return 0 #TODO implement

    def calc_building_score(self, all_needs):
        this_needs = all_needs.get(bt.KINDERGARDEN)
        return PublicBuilding.calc_building_score(self, this_needs)


###-------------------------------------------*(**)*---------------------------------------------###

class Mikve(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.MIKVE, area, location, init_height, polygon)


    def calc_conflicts(self):
        return 0 #TODO implement

    def calc_building_score(self, all_needs):
        this_needs = all_needs.get(bt.MIKVE)
        return PublicBuilding.calc_building_score(self, this_needs)


###-------------------------------------------*(**)*---------------------------------------------###

class Police(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.POLICE, area, location, init_height, polygon)


    def calc_conflicts(self):
        return 0 #TODO implement

    def calc_building_score(self, all_needs):
        this_needs = all_needs.get(bt.POLICE)
        return PublicBuilding.calc_building_score(self, this_needs)


###-------------------------------------------*(**)*---------------------------------------------###

class PrimarySchool(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.PRIMARY_SCHOOL, area, location, init_height, polygon)


    def calc_conflicts(self):
        return 0 #TODO implement

    def calc_building_score(self, all_needs):
        this_needs = all_needs.get(bt.PRIMARY_SCHOOL)
        return PublicBuilding.calc_building_score(self, this_needs)


###-------------------------------------------*(**)*---------------------------------------------###

class Sport(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.SPORT, area, location, init_height, polygon)


    def calc_conflicts(self):
        return 0 #TODO implement

    def calc_building_score(self, all_needs):
        this_needs = all_needs.get(bt.SPORT)
        return PublicBuilding.calc_building_score(self, this_needs)


###-------------------------------------------*(**)*---------------------------------------------###

class Synagogue(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.SYNAGOUGE, area, location, init_height, polygon)

    def calc_conflicts(self):
        return 0 #TODO implement

    def calc_building_score(self, all_needs):
        this_needs = all_needs.get(bt.SYNAGOUGE)
        return PublicBuilding.calc_building_score(self, this_needs)


