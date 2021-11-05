import pygame

from assets.lib.battle_system.battle_modifiers import BattleModifiers
from assets.lib.battle_system.log import Logs
from assets.lib.character_utilities.attributes import Attributes
from assets.lib.character_utilities.character_model import BaseCharacter
from assets.lib.character_utilities.modifiers import Modifiers


class BattleCharacter(BaseCharacter):

    BATTLE_CHARACTER_SIGNAL = pygame.event.custom_type()

    def battle_attribute(self, attribute):
        return getattr(self.battle_attributes, attribute)\
               + getattr(self.battle_modifiers, attribute)

    def __init__(self, base_character):
        super(BaseCharacter, self, ).__init__()

        self.name = base_character.name
        self.character_class = base_character.character_class
        self.character_type = base_character.character_type
        self.affiliation = base_character.affiliation
        self.state = base_character.state

        self.base_attributes = base_character.base_attributes
        self.base_modifiers = base_character.base_modifiers
        self.inventory = base_character.inventory
        self.equipment = base_character.equipment
        self.card_collection = base_character.card_collection
        self.deck = base_character.deck
        self.status_list = base_character.status_list
        self.card_draw = base_character.card_draw

        self.preferences = base_character.preferences

        self.character_view = None
        self.battle_attributes = self.base_attributes + self.base_modifiers
        self.battle_modifiers = BattleModifiers()
        self.battle_deck = list()
        self.draw_pile = list()
        self.discard_pile = list()
        self.exile_pile = list()
        self.hand = list()

    def modify_battle_attributes(self, attribute, value):
        Logs.CharacterModelMessage.modify_battle_attributes_info(self, attribute, value, BattleCharacter.modify_battle_attributes.__name__)
        battle_attributes_value = getattr(self.battle_attributes, attribute)
        setattr(self.battle_attributes, attribute, battle_attributes_value + value)
        Logs.CharacterModelMessage.modify_battle_attributes_info(self, attribute, value, BattleCharacter.modify_battle_attributes.__name__)

    def modify_battle_modifiers(self, attribute, value, related_status):

        modifier = Modifiers(attribute, value, related_status)

        self.battle_modifiers.add_modifier(modifier)

        # print(f'{self.name}: battle_modifiers.{attribute}:{getattr(self.battle_modifiers, attribute)}')
        # battle_modifiers_value = getattr(self.battle_modifiers, attribute)
        # setattr(self.battle_modifiers, attribute, battle_modifiers_value + value)
        # print(f'{self.name}: battle_modifiers.{attribute}:{getattr(self.battle_modifiers, attribute)}')

    def take_damage_battle_attribute(self, value):
        self.battle_attributes.health -= value

    def heal_health_battle_attribute(self, value):
        self.battle_attributes.health += value

    @staticmethod
    def create_character_models(base_models):
        characters_list = list()
        for base_character in base_models:
            battle_character = BattleCharacter(base_character)
            characters_list.append(battle_character)

        return characters_list
