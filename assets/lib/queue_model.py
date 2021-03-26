import copy


class QueueModel():

    def __init__(self):
        self.characters_speed = dict()
        self.modifiers = dict()

        self.party = dict()

        self.queue = list()

    def setup_speeds(self, character_model):
        units = character_model.party_list + character_model.enemy_list
        for u in units:
            speed = u.attributes.speed
            self.characters_speed[u] = speed
            self.party[u] = 0
            self.modifiers[u] = 0

    @staticmethod
    def update_party(party, characters_speed, modifiers):
        for c in party:
            party[c] += characters_speed[c] + modifiers[c]

    @staticmethod
    def get_next(party):
        fastest = max(party, key=party.get)
        if party[fastest] >= 100:
            return fastest
        elif party[fastest] < 100:
            return None

    @staticmethod
    def reduce_speed(party, character):
        party[character] -= 100

    @staticmethod
    def get_queue(queue, party, character_speeds, modifiers):
        _party = dict()

        for key, value in party.items():
            _party[key] = value

        quantity = 8

        while quantity - len(queue) != 0:
            character = QueueModel.get_next(_party)
            if character != None:
                queue.append(character)
                QueueModel.reduce_speed(_party, character)
            elif character == None:
                QueueModel.update_party(_party, character_speeds, modifiers)

        return _party, queue
