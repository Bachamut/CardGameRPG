from attributes import Attributes
from deck import Deck
from equipment import Equipment
from inventory import Inventory


class InvalidSlotException(Exception):
    pass


class EmptySlotException(object):
    pass


class Character():

    def __init__(self):

        self.name = ''
        self.character_class = ''
        self.attributes = Attributes()
        self.modifiers = Attributes()
        self.inventory = Inventory()
        self.equipment = Equipment()
        self.deck = Deck()

    def add_item(self, item):
        # dodanie przedmiotu do inwentarza
        self.inventory.container.append(item)

    def remove_item(self, item):
        # usunięcie przedmiotu z inwentarza
        self.inventory.container.remove(item)

    def add_equip(self, slot, item):

        if item.slot_type == slot:
            self.inventory.container.pop(item)
            self.inventory.container.append(self.equipment.equipment_slots[slot])
            self.equipment.equipment_slots[slot] = item
        else:
            raise InvalidSlotException("Invalid Slot Exception")

    def remove_equip(self, slot, item):

        if self.equipment.equipment_slots(slot) != '':
            self.equipment.equipment_slots[slot] = ''
            self.inventory.container.append(item)
        else:
            raise EmptySlotException("Empty Slot Exception")






