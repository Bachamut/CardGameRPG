class QueueModel():

    def __init__(self, character_model):
        self.cm = character_model
        self.temp_queue = []
        self.end_cycle = {}
        self.it = 0

    def create_queue(self):
        self.cm.units = self.cm.party_list + self.cm.enemy_list
        for unit in self.cm.units:
            speed = unit.attributes.speed
            self.cm.character_list[unit] = speed

    def update_queue(self):
        count = 10

        for n in range(0, count-len(self.temp_queue)):
            self.temp_queue.append(self._get_next())
        print(len(self.temp_queue))
        # print(f'\n---QUEUE---')
        # for character in self.cm.queue_list:
        #     print(character.name)
        # print(f'---END QUEUE---')
        next_char = self.temp_queue.pop(0)
        self.cm.queue_list = self.temp_queue[0:9]
        return next_char

    def _get_next(self):

        while True:
            if self.it == len(self.cm.character_list):
                self.end_cycle = self.cm.character_list
                print(f'---CYCLE END---')
                for character, speed in self.cm.character_list.items():
                    print(f'{character.name} speed = {speed}')
                self.it = 0
            fastest_char = max(self.cm.character_list, key=self.cm.character_list.get)
            if self.cm.character_list[fastest_char] >= 100:
                self.cm.character_list[fastest_char] -= 100
                next_char = fastest_char
                print("\nEND LOOP")
                for character, speed in self.cm.character_list.items():
                    print(f'{character.name} speed = {speed}')
                self.it += 1
                return next_char
                break
            else:
                for unit in self.cm.units:
                    speed = unit.attributes.speed
                    self.cm.character_list[unit] += speed
            print("\nIN LOOP")
            for character, speed in self.cm.character_list.items():
                print(f'{character.name} speed = {speed}')