from assets.lib.character_utilities.character import BaseCharacter


class BattleCharacter(BaseCharacter):

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

        self.character_view = None
        self.character_type = None
        self.battle_modifiers = None
        self.battle_deck = None
        self.hand = None
        self.draw_pile = None
        self.discard_pile = None
        self.exile_pile = None

    @staticmethod
    def create_character_models(base_models):
        characters_list = list()
        for base_character in base_models:
            battle_character = BattleCharacter(base_character)
            characters_list.append(battle_character)

        return characters_list
