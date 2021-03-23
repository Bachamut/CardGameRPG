class QueueModel():

    def __init__(self, character_model):
        self.cm = character_model


    def create_queue(self):
        self.cm.units = self.cm.party_list + self.cm.enemy_list
        for unit in self.cm.units:
            speed = unit.attributes.speed
            self.cm.character_list[unit] = speed

    def update_queue(self):
        count = 8
        self.cm.queue_list = []

        for n in range(0, count):
            self.cm.queue_list.append(self._update_queue())

        for character in self.cm.queue_list:
            print(character.name)

        return self.cm.queue_list[0]

    def _update_queue(self):
        while True:
            fastest_char = max(self.cm.character_list, key=self.cm.character_list.get)
            if self.cm.character_list[fastest_char] >= 100:
                self.cm.character_list[fastest_char] -= 100
                next_char = fastest_char
                # print("\nEND LOOP")
                # for character, speed in self.cm.character_list.items():
                #     print(f'{character.name} speed = {speed}')
                return next_char
                break
            else:
                for unit in self.cm.units:
                    speed = unit.attributes.speed
                    self.cm.character_list[unit] += speed
            # print("\nIN LOOP")
            # for character, speed in self.cm.character_list.items():
            #     print(f'{character.name} speed = {speed}')