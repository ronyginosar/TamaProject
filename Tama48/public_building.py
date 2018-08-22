import building
import util
import needs
import building_types as bt

class PublicBuilding(building.Building):

    def __init__(self, building_id, b_type, area, location, init_height, polygon):
        building.Building.__init__(self, building_id, b_type, area, location, init_height, polygon)
        # list of residential building which are using this public building (among other public building in this type)
        self.__users_buildings = []
        self.building_score= 0

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
        using_area_meters = sum(using_area)
        area_ratio_score = self.get_overall_area()/using_area_meters
        self.building_score = area_ratio_score / (self.get_extra_height() + self.get_init_height())
        return self.building_score

    def get_building_score(self):
        return self.building_score


    def calc_conflicts(self):
        pass


###-------------------------------------------*(**)*---------------------------------------------###

IDEAL_SIZE_PER_PERSON = 0.1

class Clinic(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.CLINIC, area, location, init_height, polygon)
        self.__max_height = bt.MAX_HEIGHTS_DICT.get(bt.CLINIC)

    def get_max_height(self):
        return self.__max_height

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
        this_needs = all_needs.get(bt.CLINIC)*needs.one_unit_in_meter_square(bt.CLINIC)
        return PublicBuilding.calc_building_score(self, this_needs)

###-------------------------------------------*(**)*---------------------------------------------###

PERCENTAGE_OF_USERS_FROM_POPULATION = 0.2
IDEAL_AREA_PER_USER_COMMUNITY = 0.5

class CommunityCenter(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.COMMUNITY_CNTR, area, location, init_height, polygon)
        self.__max_height = bt.MAX_HEIGHTS_DICT.get(bt.COMMUNITY_CNTR)

    def get_max_height(self):
        return self.__max_height

    def calc_conflicts(self):
        num_users = int(self.get_using_population() * PERCENTAGE_OF_USERS_FROM_POPULATION)
        area_per_person = self.get_overall_area()/num_users
        conflict_points = int((IDEAL_AREA_PER_USER_COMMUNITY - area_per_person)*(10/IDEAL_AREA_PER_USER_COMMUNITY))
        if conflict_points <= 0:
            return 0
        else:
            return conflict_points

    def calc_building_score(self, all_needs):
        this_needs = all_needs.get(bt.COMMUNITY_CNTR)*needs.one_unit_in_meter_square(bt.COMMUNITY_CNTR)
        return PublicBuilding.calc_building_score(self, this_needs)


###-------------------------------------------*(**)*---------------------------------------------###

ELDERLY_PERCENTAGE_FROM_POPULATION = 0.11
PERCENTAGE_OF_ELDERLY_USERS_FROM_POPULATION = 0.15 * ELDERLY_PERCENTAGE_FROM_POPULATION
IDEAL_AREA_PER_USER_ELDERLY = 1

class ElderlyCenter(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.ELDERLY_CNTR, area, location, init_height, polygon)
        self.__max_height = bt.MAX_HEIGHTS_DICT.get(bt.ELDERLY_CNTR)

    def get_max_height(self):
        return self.__max_height

    def calc_conflicts(self):
        num_users = int(self.get_using_population() * PERCENTAGE_OF_ELDERLY_USERS_FROM_POPULATION)
        area_per_person = self.get_overall_area()/num_users
        conflict_points = int((IDEAL_AREA_PER_USER_ELDERLY - area_per_person)*(10/IDEAL_AREA_PER_USER_ELDERLY))
        if conflict_points <= 0:
            return 0
        else:
            return conflict_points

    def calc_building_score(self, all_needs):
        this_needs = all_needs.get(bt.ELDERLY_CNTR)*needs.one_unit_in_meter_square(bt.ELDERLY_CNTR)
        return PublicBuilding.calc_building_score(self, this_needs)

###-------------------------------------------*(**)*---------------------------------------------###

IDEAL_CLASS_SIZE = needs.CLASS_SIZE
NUM_AGE_GROUPS = 6

class HighSchool(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.HIGH_SCHOOL, area, location, init_height, polygon)
        self.__max_height = bt.MAX_HEIGHTS_DICT.get(bt.HIGH_SCHOOL)

    def get_max_height(self):
        return self.__max_height

    def get_class_size(self):
        age_group_size = self.get_using_population()*needs.AGE_GROUP18_PRCTG*0.01*NUM_AGE_GROUPS
        num_classes = int(self.get_overall_area()/needs.one_unit_in_meter_square(bt.HIGH_SCHOOL))
        return age_group_size / num_classes

    def calc_conflicts(self):
        conflict_points = IDEAL_CLASS_SIZE - self.get_class_size()
        if conflict_points <= 0:
            return 0
        else:
            return conflict_points

    def calc_building_score(self, all_needs):
        this_needs = all_needs.get(bt.HIGH_SCHOOL)*needs.one_unit_in_meter_square(bt.HIGH_SCHOOL)
        return PublicBuilding.calc_building_score(self, this_needs)


###-------------------------------------------*(**)*---------------------------------------------###

class Hospital(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.HOSPITAL, area, location, init_height, polygon)
        self.__max_height = bt.MAX_HEIGHTS_DICT.get(bt.HOSPITAL)

    def get_max_height(self):
        return self.__max_height

    # Hospital is not needed in the neighborhood level
    def calc_conflicts(self):
        return 0

    def calc_building_score(self, all_needs):
        this_needs = all_needs.get(bt.HOSPITAL)*needs.one_unit_in_meter_square(bt.HOSPITAL)
        return PublicBuilding.calc_building_score(self, this_needs)


###-------------------------------------------*(**)*---------------------------------------------###

IDEAL_K_CLASS_SIZE = needs.CLASS_SIZE
NUM_K_AGE_GROUPS = 3

class Kindergarden(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.KINDERGARDEN, area, location, init_height, polygon)
        self.__max_height = bt.MAX_HEIGHTS_DICT.get(bt.KINDERGARDEN)

    def get_max_height(self):
        return self.__max_height


    def get_class_size(self):
        age_group_size = self.get_using_population()*needs.AGE_GROUP18_PRCTG*0.01*NUM_K_AGE_GROUPS
        num_classes = int(self.get_overall_area()/needs.one_unit_in_meter_square(bt.KINDERGARDEN))
        return age_group_size / num_classes


    def calc_conflicts(self):
        conflict_points = IDEAL_K_CLASS_SIZE - self.get_class_size()
        if conflict_points <= 0:
            return 0
        else:
            return conflict_points


    def calc_building_score(self, all_needs):
        this_needs = all_needs.get(bt.KINDERGARDEN)*needs.one_unit_in_meter_square(bt.KINDERGARDEN)
        return PublicBuilding.calc_building_score(self, this_needs)


###-------------------------------------------*(**)*---------------------------------------------###

IDEAL_USERS_PER_PIT = 500

class Mikve(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.MIKVE, area, location, init_height, polygon)
        self.__max_height = bt.MAX_HEIGHTS_DICT.get(bt.MIKVE)

    def get_max_height(self):
        return self.__max_height


    def calc_conflicts(self):
        num_using_units = self.get_using_population()/needs.AVG_FAMILY_SIZE
        num_pits = int(self.get_overall_area() / 65)
        people_per_pit = num_using_units / num_pits
        # needs a pit for 500 users
        conflict_points = (IDEAL_USERS_PER_PIT - people_per_pit)*(10/IDEAL_USERS_PER_PIT)
        if conflict_points <= 0:
            return 0
        else:
            return conflict_points


    def calc_building_score(self, all_needs):
        this_needs = all_needs.get(bt.MIKVE)*needs.one_unit_in_meter_square(bt.MIKVE)
        return PublicBuilding.calc_building_score(self, this_needs)


###-------------------------------------------*(**)*---------------------------------------------###

IDEAL_POLICE_SIZE_PER_PERSON = 0.1

class Police(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.POLICE, area, location, init_height, polygon)
        self.__max_height = bt.MAX_HEIGHTS_DICT.get(bt.POLICE)

    def get_max_height(self):
        return self.__max_height


    def calc_conflicts(self):
        area_per_person = self.get_overall_area()/self.get_using_population()
        conflict_points = int((IDEAL_POLICE_SIZE_PER_PERSON - area_per_person)*(10/IDEAL_POLICE_SIZE_PER_PERSON))
        if conflict_points <= 0:
            return 0
        else:
            return conflict_points

    def calc_building_score(self, all_needs):
        this_needs = all_needs.get(bt.POLICE)*needs.one_unit_in_meter_square(bt.POLICE)
        return PublicBuilding.calc_building_score(self, this_needs)


###-------------------------------------------*(**)*---------------------------------------------###

IDEAL_P_CLASS_SIZE = needs.CLASS_SIZE
NUM_P_AGE_GROUPS = 6

class PrimarySchool(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.PRIMARY_SCHOOL, area, location, init_height, polygon)
        self.__max_height = bt.MAX_HEIGHTS_DICT.get(bt.PRIMARY_SCHOOL)

    def get_max_height(self):
        return self.__max_height

    def get_class_size(self):
        age_group_size = self.get_using_population()*needs.AGE_GROUP18_PRCTG*0.01*NUM_P_AGE_GROUPS
        num_classes = int(self.get_overall_area()/needs.one_unit_in_meter_square(bt.PRIMARY_SCHOOL))
        return age_group_size / num_classes


    def calc_conflicts(self):
        conflict_points = IDEAL_P_CLASS_SIZE - self.get_class_size()
        if conflict_points <= 0:
            return 0
        else:
            return conflict_points


    def calc_building_score(self, all_needs):
        this_needs = all_needs.get(bt.PRIMARY_SCHOOL)*needs.one_unit_in_meter_square(bt.PRIMARY_SCHOOL)
        return PublicBuilding.calc_building_score(self, this_needs)


###-------------------------------------------*(**)*---------------------------------------------###

class Sport(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.SPORT, area, location, init_height, polygon)
        self.__max_height = bt.MAX_HEIGHTS_DICT.get(bt.SPORT)

    def get_max_height(self):
        return self.__max_height

    # no special needs for sports facilities in the neighborhood level - later to be added to the parks area
    def calc_conflicts(self):
        return 0

    def calc_building_score(self, all_needs):
        this_needs = all_needs.get(bt.SPORT)*needs.one_unit_in_meter_square(bt.SPORT)
        return PublicBuilding.calc_building_score(self, this_needs)


###-------------------------------------------*(**)*---------------------------------------------###

PERCENTAGE_OF_RELIGIOUS_FROM_POPULATION = 0.01*needs.RELIGION_PRCTG
IDEAL_AREA_PER_USER_SYNAGOGUE = 1.1


class Synagogue(PublicBuilding):

    def __init__(self, building_id, area, location, init_height, polygon):
        PublicBuilding.__init__(self, building_id, bt.SYNAGOUGE, area, location, init_height, polygon)
        self.__max_height = bt.MAX_HEIGHTS_DICT.get(bt.SYNAGOUGE)

    def get_max_height(self):
        return self.__max_height

    def calc_conflicts(self):
        num_users = int(self.get_using_population() * PERCENTAGE_OF_RELIGIOUS_FROM_POPULATION)
        area_per_person = self.get_overall_area()/num_users
        conflict_points = int((IDEAL_AREA_PER_USER_SYNAGOGUE - area_per_person)*(10/IDEAL_AREA_PER_USER_SYNAGOGUE))
        if conflict_points <= 0:
            return 0
        else:
            return conflict_points

    def calc_building_score(self, all_needs):
        this_needs = all_needs.get(bt.SYNAGOUGE)*needs.one_unit_in_meter_square(bt.SYNAGOUGE)
        return PublicBuilding.calc_building_score(self, this_needs)


