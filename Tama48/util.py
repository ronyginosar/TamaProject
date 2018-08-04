import needs


"""
returns the number of units added to a building
"""
# TODO: TO CHECK IMPLEMENTATION
def get_units_added_to_one_building(building_to_increase, additional_floors):
    return int(additional_floors * building_to_increase.get_area() / needs.METERS_PER_UNIT)


"""
adds floors to a given list of additional floors (changes the original list)
return: number of units added
"""
# TODO: TO CHECK IMPLEMENTATION
def add_floors(num_floors_to_add, state_to_update, building_to_increase):
    state_to_update.add_floor(building_to_increase, num_floors_to_add)
    return get_units_added_to_one_building(building_to_increase, num_floors_to_add)


"""
returns the number of units added to the city
"""
# TODO: TO CHECK IMPLEMENTATION
def get_units_added(residential_buildings, additional_floors):
    units_added = 0
    for i in range(len(residential_buildings)):
        units_added += get_units_added_to_one_building(residential_buildings[i], additional_floors[i])
    return units_added

"""
Done!
distance between centers of two buildings
usually for one public, one residential
"""
# TODO: TO CHECK IMPLEMENTATION
def calc_distance_two_buildings(buildings_resd, building_public):
    loc1 = buildings_resd.get_location()
    loc2 = building_public.get_location()

    euclid_dist = pow(pow(loc1[0] - loc2[0], 2) + pow(loc1[1] - loc2[1], 2), 0.5)
    return euclid_dist

"""
volume of all residential buildings, including init heights, and extra heights
"""
# TODO: TO CHECK IMPLEMENTATION
def get_overall_resd_area(buildings_data_resd):
    sum_vol = 0
    for building in buildings_data_resd:
        sum_vol += building.get_overall_volume()
    return sum_vol

"""
help to tell how many people there is in this building in ratio to the population of the neighborhood.
i.e. how much this specific_resd_building is important, relatively to the others..
"""
# TODO: TO CHECK IMPLEMENTATION
def calc_importance_of_building(specific_resd_building, buildings_data_resd):
    overall_resd_volume = get_overall_resd_area(buildings_data_resd)
    building_resd_volume = specific_resd_building.get_overall_area()
    return building_resd_volume/overall_resd_volume

def calc_pop_size(buildings):
    pop_size = 0
    for building in buildings:
        pop_size += int(building.get_overall_area()*needs.AVG_FAMILY_SIZE/needs.METERS_PER_UNIT)
    return pop_size