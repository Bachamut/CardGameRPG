from game_object.game_object import GameObject

from assets.lib.battle_system.ai_utilities.ai_preferences import Preferences
from assets.lib.battle_system.log import Logs
from assets.lib.character_utilities.attributes import Attributes
from assets.lib.card_utilities.deck import Deck
from assets.lib.item_utilities.equipment import Equipment
from assets.lib.item_utilities.inventory import Inventory
from assets.lib.item_utilities.item_model import NoCardInItemException
from assets.lib.item_utilities.item_manager import ItemManager


class InvalidSlotException(Exception):
    pass


class EmptySlotException(Exception):
    pass

class BaseCharacter(GameObject):

    def __init__(self):
        self.name = None
        self.character_class = None
        self.character_type = None
        self.affiliation = None
        self.set_resource = None
        self.state = None
        self.base_attributes = Attributes()
        self.base_modifiers = Attributes()
        self.inventory = Inventory(20)
        self.equipment = Equipment()
        self.card_collection = Deck()
        self.deck = Deck(8, 20)
        self.status_list = list()
        self.card_draw = 3

        self.preferences = Preferences()


    def add_status(self, status):
        self.status_list.append(status)
        Logs.CharacterModelMessage.add_status_info(self, status, BaseCharacter.add_status.__name__)


    def remove_status(self, status):
        self.status_list.remove(status)
        Logs.CharacterModelMessage.remove_status_info(self, status, BaseCharacter.add_status.__name__)

    def add_equip(self, slot, item):
        # add item to equipment slot
        item_instance = ItemManager.create_item(item)
        if item_instance.slot_type == slot:
            self.inventory.remove_item(item)
            # self.inventory[item] -= 1
            if self.equipment[slot] != None:
                removed_item = self.equipment[slot]
                self.inventory.add_item(removed_item.item_name)
            self.equipment[slot] = item_instance
            # add card from item to deck
            try:
                self._add_item_card(item_instance)
            except NoCardInItemException:
                print(f'{self.name}: Do ekwipunku dodano przedmiot: {item}')
                print(f'Nie dodano karty')
            else:
                print(f'{self.name}: Do ekwipunku dodano przedmiot: {item}')
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
            self.inventory.add_item(removed_item.item_name)
            self.equipment[slot] = None
            try:
                self._remove_item_card(removed_item)
            except NoCardInItemException:
                print(f'{self.name}: Z ekwipunku usunięto przedmiot: {removed_item.item_name}')
                print(f'Nie usunięto karty ponieważ nie ma żadnych w przedmiocie')
            else:
                print(f'{self.name}: Z ekwipunku usunięto przedmiot: {removed_item.item_name}')
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
        self.card_collection[card] -=1
        if self.card_collection[card] <= 0:
            del self.card_collection[card]

    def remove_deck_card(self, card):
        if card in self.card_collection:
            self.card_collection[card] += 1
        else:
            self.card_collection[card] = 1
        self.deck[card] -= 1
        if self.deck[card] <= 0:
            del self.deck[card]

    def add_pool_card(self, card):
        if card in self.card_collection:
            self.card_collection[card] += 1
        else:
            self.card_collection[card] = 1

    def remove_pool_card(self, card):
        self.card_collection[card] -= 1
        if self.card_collection[card] <= 0:
            del self.card_collection[card]

    def take_damage(self, value):
        self.base_attributes.health -= value

        # if self.base_attributes.health <= 0:
        #     print(f'{self.name} nie żyje')

    def modify_action_points(self, value):
        self.base_attributes.action_points += value

    def modify_base_attribute(self, attribute, value):
        base_attribute_value = getattr(self.base_attributes, attribute)
        setattr(self.base_attributes, attribute, base_attribute_value + value)

    def modify_base_modifiers(self, attribute, value):
        base_modifiers_value = getattr(self.base_modifiers, attribute)
        setattr(self.base_modifiers, attribute, base_modifiers_value + value)



