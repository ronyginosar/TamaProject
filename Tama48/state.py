

class State(object):
    def __init__(self, buildings_data, additional_floors, additional_public):
        self.buildings_data = buildings_data
        self.additional_floors = additional_floors
        self.pub_floors = additional_public
        self.score = self.calc_score()

    # returns the score of this state
    def get_score(self):
        return self.score

    def calc_score(self):
        return 0 #TODO implement

    def get_heights_to_add(self):
        return self.additional_floors