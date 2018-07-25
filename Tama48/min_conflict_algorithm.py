import evaluate_plan

def min_conflict_solution(buildings_data, all_needs):
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



    # iter until max_iter
    # for i=1 to ____ :
        # if current_state is a solution of csp then return current_state
        # we return a solution set of values for the variable
        # var <-- a randomly chosen variable from the set of conflicted variables CONFLICTED[csp]
        # value <-- the value v for var that minimizes CONFLICTS(var,v,current_state,csp)
        # set var = value in current_state
    # return fail

    # current_state, an initial assignment of values for the variables in the csp
    # csp, a constraint satisfaction problem: <variables> , <constraints> ,

    return additional_heights

