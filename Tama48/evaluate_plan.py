"""
buildings_data: list of tuples, each tuple contains (buildings_type, list of all Building objects in this type)
additional_height: tuple of (building_id(int), additional_height(meters))
type_importance_dict:
"""
def calc_plan_evaluation(buildings_data, additional_height, type_importance_dict):
    plan_grade = 0.0
    for building_type in buildings_data:
        imp = type_importance_dict[building_type]
        plan_grade += calc_specific_plan_evaluation(building_type)*imp

    return plan_grade

def calc_specific_plan_evaluation (building_type, buildings_data):
    return 0.0
