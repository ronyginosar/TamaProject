import evaluate_plan

def find_solution(buildings_data, add_housing_unit):
    additional_heights = []
    building_types = [building[0] for building in buildings_data]
    building_residential = []
    needs = evaluate_plan.Needs(buildings_data, add_housing_unit)
    all_needs = needs.calc_all_needs()

    # TODO implement algorithm, implement 
    for building in buildings_data:
        if building[0] == 'residential':
            building_residential == building[1]
            break
        else:
            building_types.append(building)

    return additional_heights