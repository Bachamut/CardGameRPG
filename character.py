from attributes import Attributes


class InvalidSlotException(Exception):
    pass


class Character():

    def __init__(self):

        self.name = ''
        self.character_class = ''
        self.attributes = Attributes()
        self.modifiers = Attributes()
        self.deck = []
        self.inventory = []
        self.equipment = {}

    def add_item(self, item):
        # dodanie przedmiotu do inwentarza
        self.inventory.append(item)

    def remove_item(self, item):
        # usunięcie przedmiotu z inwentarza
        self.inventory.remove()

    def equip_item(self, slot, item):

        if item.slot_type == slot:
            self.inventory.pop(item)
            self.inventory.append(self.equipment[slot])
            self.equipment[slot] = item

        else:

            raise InvalidSlotException("Invalid Slot Exception")

    def equip_remove(self, slot, item):





