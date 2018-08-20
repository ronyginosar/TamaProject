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
	personal_satisfaction = []

	for person in people:
		person.set_residence(residential_buildings[np.random.randint(len(residential_buildings))])
		personal_satisfaction.append((person.get_type(), str(person.get_religious()), person.get_residence(), person.set_satisfaction()))
	return personal_satisfaction
		
