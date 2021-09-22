import pygame

from assets.lib.character_utilities.attributes import Attributes
from assets.lib.character_utilities.character import BaseCharacter



class BattleCharacter(BaseCharacter):

    BATTLE_CHARACTER_SIGNAL = pygame.event.custom_type()

    def battle_attribute(self, attribute):
        return getattr(self.base_attributes, attribute)\
               + getattr(self.base_modifiers, attribute)\
               + getattr(self.battle_modifiers, attribute)

    def __init__(self, base_character):
        super(BaseCharacter, self, ).__init__()

        self.name = base_character.name
        self.character_class = base_character.character_class
        self.base_attributes = base_character.base_attributes
        self.base_modifiers = base_character.base_modifiers
        self.inventory = base_character.inventory
        self.equipment = base_character.equipment
        self.card_collection = base_character.card_collection
        self.deck = base_character.deck
        self.status_list = base_character.status_list
        self.card_draw = base_character.card_draw

        self.character_view = None
        self.character_type = None
        self.battle_modifiers = Attributes()
        self.battle_deck = list()
        self.draw_pile = list()
        self.discard_pile = list()
        self.exile_pile = list()
        self.hand = list()

    def modify_battle_modifiers(self, attribute, value):
        print(f'{self.name}: battle_modifiers.{attribute}:{getattr(self.battle_modifiers, attribute)}')
        battle_modifiers_value = getattr(self.battle_modifiers, attribute)
        setattr(self.battle_modifiers, attribute, battle_modifiers_value + value)
        print(f'{self.name}: battle_modifiers.{attribute}:{getattr(self.battle_modifiers, attribute)}')

    @staticmethod
    def create_character_models(base_models):
        characters_list = list()
        for base_character in base_models:
            battle_character = BattleCharacter(base_character)
            characters_list.append(battle_character)

        return characters_list
