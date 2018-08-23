import math
import util
import building_types as bt
import person as p
import numpy as np

SINGLE = "single"
PARENT = "parent"
CHILD = "child"
ELDERLY = "elderly"


person_types = []


def evaluate_personal_satisfaction(plan):
    
	residential_buildings = bt.find_buildings_in_type(bt.RESIDENTIAL, plan)

	people = []
	people.append(p.Person(CHILD, False))
	people.append(p.Person(SINGLE, False))
	people.append(p.Person(SINGLE,True))
	people.append(p.Person(PARENT, False))
	people.append(p.Person(ELDERLY,True))
	personal_satisfaction_raw = []
	personal_satisfaction = []
	max_sat = 0
	for person in people:
		person.set_residence(residential_buildings[np.random.randint(len(residential_buildings))])
		curr_sat = round(person.set_satisfaction(),4)
		personal_satisfaction_raw.append(curr_sat)
		if(curr_sat>max_sat):
			max_sat=curr_sat
	for i in range(len(people)):
		curr_sat = round(personal_satisfaction_raw[i]/max_sat,4)
		personal_satisfaction.append((people[i].get_type(), str(people[i].get_religious()), people[i].get_residence(), curr_sat)) 
	return personal_satisfaction
		
