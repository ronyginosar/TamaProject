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
def add_floors(num_floors_to_add, additional_floors, building_to_increase):
    additional_floors[building_to_increase.get_id()] += num_floors_to_add
    return get_units_added_to_one_building(building_to_increase, additional_floors)


"""
returns the number of units added to the city
"""
# TODO: TO CHECK IMPLEMENTATION
def get_units_added(residential_buildings, additional_floors):
    units_added = 0
    for i in range(len(residential_buildings)):
        units_added += get_units_added_to_one_building(residential_buildings[i], additional_floors[i])
    return units_added