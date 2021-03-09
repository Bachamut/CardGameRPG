from attributes import Attributes
from card_manager import CardManager
from deck import Deck
from equipment import Equipment
from inventory import Inventory
from item import NoCardInItemException


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
        self.status = {}

    def add_item(self, item):
        # add item to inventory
        self.inventory.append(item)

    def remove_item(self, item):
        # remove item form inventory
        self.inventory.remove(item)

    def add_equip(self, slot, item):
        # add item to equipment slot
        if item.slot_type == slot:
            self.inventory.remove(item)
            self.inventory.append(self.equipment[slot])
            self.equipment[slot] = item
            # adding card from item to card_pool
            try:
                self._add_item_card(item)
            except NoCardInItemException:
                print(f'Dodano przedmiot {item}')
                print(f'Nie dodano karty')
            else:
                print(f'Dodano przedmiot {item}')
                print(f'Dodano kartę {item.add_card}')
        else:
            raise InvalidSlotException("Invalid Slot Exception")

    def _add_item_card(self, item):
        card_list = item.get_card()
        for key, value in card_list.items():
            for number in range(0, value):
                new_card = CardManager.create_card(key)
                self.deck.card_pool.append(new_card)

    def remove_equip(self, slot, item):
        # remove item form equipment slot
        if self.equipment[slot] != None:
            self.equipment[slot] = None
            self.inventory.append(item)
            try:
                self._remove_item_card(item)
            except NoCardInItemException:
                print(f'Usunięto przedmiot {item}')
                print(f'Nie usunięto karty ponieważ nie ma żadnych w przedmiocie')
            else:
                print(f'Usunięto przedmiot {item}')
                print(f'Usunięto kartę {item.add_card}')
        else:
            raise EmptySlotException("Empty Slot Exception")

    def _remove_item_card(self, item):
        card_list = item.get_card()
        for key, value in card_list.items():
            for number in range(0, value):
                # poprawić kod by podawać nazwę karty
                self.deck.card_pool.pop(0)








