from attributes import Attributes
from battle_logic import BattleLogic
from card_manager import CardManager
from deck import Deck
from equipment import Equipment
from inventory import Inventory
from item import NoCardInItemException
from item_manager import ItemManager


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
        self.card_pool = Deck()
        # self.battle = BattleLogic()
        self.status = {}
        self.battledeck = []
        self.hand = []


    def add_equip(self, slot, item):
        # add item to equipment slot
        item_instance = ItemManager.create_item(item)
        if item_instance.slot_type == slot:
            self.inventory[item] -= 1
            if self.equipment[slot] != None:
                removed_item = self.equipment[slot]
                self.inventory[removed_item.item_name] += 1
            self.equipment[slot] = item_instance
            # add card from item to deck
            try:
                self._add_item_card(item_instance)
            except NoCardInItemException:
                print(f'Do ekwipunku dodano przedmiot: {item}')
                print(f'Nie dodano karty')
            else:
                print(f'Do ekwipunku dodano przedmiot: {item}')
                print(f'Dodano kartę {item_instance.add_card}')
        else:
            raise InvalidSlotException("Invalid Slot Exception")

    def _add_item_card(self, item_instance):
        for key, value in item_instance.add_card.items():
            if key in self.deck:
                self.deck[key] += value
            else:
                self.deck[key] = value

    def remove_equip(self, slot):
        # remove item form equipment slot
        if self.equipment[slot] != None:
            removed_item = self.equipment[slot]
            self.inventory[removed_item.item_name] += 1
            self.equipment[slot] = None
            try:
                self._remove_item_card(removed_item)
            except NoCardInItemException:
                print(f'Z ekwipunku usunięto przedmiot: {removed_item.item_name}')
                print(f'Nie usunięto karty ponieważ nie ma żadnych w przedmiocie')
            else:
                print(f'Z ekwipunku usunięto przedmiot: {removed_item.item_name}')
                print(f'Usunięto kartę {removed_item.add_card}')
        else:
            raise EmptySlotException("Empty Slot Exception")

    def _remove_item_card(self, removed_item):
        for key, value in removed_item.add_card.items():
            self.deck[key] -= value
            if self.deck[key] == 0:
                del self.deck[key]

    def add_deck_card(self, card):
        if card in self.deck:
            self.deck[card] += 1
        else:
            self.deck[card] = 1
        self.card_pool[card] -=1
        if self.card_pool[card] <= 0:
            del self.card_pool[card]

    def remove_deck_card(self, card):
        if card in self.card_pool:
            self.card_pool[card] += 1
        else:
            self.card_pool[card] = 1
        self.deck[card] -= 1
        if self.deck[card] <= 0:
            del self.deck[card]

    def add_pool_card(self, card):
        if card in self.card_pool:
            self.card_pool[card] += 1
        else:
            self.card_pool[card] = 1

    def remove_pool_card(self, card):
        self.card_pool[card] -= 1
        if self.card_pool[card] <= 0:
            del self.card_pool[card]



