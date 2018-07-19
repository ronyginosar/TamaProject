import evaluate_plan

def genetic_solution(buildings_data, all_needs):
    additional_heights = []
    building_residential = []
    building_types = []
    # TODO implement algorithm, implement 
    for building in buildings_data:
        if building[0] == 'residential':
            building_residential == building[1]
            break
        else:
            building_types.append(building[0])

    # type algorithm here
    # for ...
    #   new_plan_state = ...
    #   additional_heights = evaluate_plan.EvaluatePlan(init_state, new_plan_state, all_needs)
    # ...

    return additional_heights