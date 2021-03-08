from attributes import Attributes
from deck import Deck
from equipment import Equipment
from inventory import Inventory


class InvalidSlotException(Exception):
    pass


class EmptySlotException(Exception):
    pass


class Character():

    def __init__(self):

        self.name = ''
        self.character_class = ''
        self.attributes = Attributes()
        self.modifiers = Attributes()
        self.inventory = Inventory(20)
        self.equipment = Equipment()
        self.deck = Deck(8, 20)

    def add_item(self, item):
        # add item to inventory
        self.inventory.append(item)

    def remove_item(self, item):
        # remove item form inventory
        self.inventory.remove(item)

    def add_equip(self, slot, item):
        # add item to equipment slot
        if item.slot_type == slot:
            self.inventory.pop(item)
            self.inventory.append(self.equipment[slot])
            self.equipment[slot] = item
        else:
            raise InvalidSlotException("Invalid Slot Exception")

    def remove_equip(self, slot, item):
        # remove item form equipment slot
        if self.equipment[slot] != None:
            self.equipment[slot] = None
            self.inventory.append(item)
        else:
            raise EmptySlotException("Empty Slot Exception")






