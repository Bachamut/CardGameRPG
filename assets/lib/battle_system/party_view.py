import pygame

from game_object.game_object import GameObject
from assets.lib.battle_system.character_model import CharacterModel
from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.battle_system.party_character_view import PartyCharacterView, CharacterIcon, CharacterName, AttributeLine


class CurrentPartyCharacterView(GameObject):
    def __init__(self, character):
        super(CurrentPartyCharacterView, self).__init__()
        self.object_class = 'PartyCharacterView'

        self.character = character

        self.add_property('TransformProperty')
        self.position = self.property('TransformProperty').position

        self.character_icon = CharacterIcon()
        self.character_name = CharacterName(self.character.name)
        self.character_hp = AttributeLine("HP", self.character.attributes.health, (0, 204, 10))
        self.character_ep = AttributeLine("EP", self.character.attributes.energy, (0, 92, 204))
        self.character_ap = AttributeLine("AP", self.character.attributes.action_points, (204, 112, 0))

        self.attach_child(self.character_icon)
        self.attach_child(self.character_name)
        self.attach_child(self.character_hp)
        self.attach_child(self.character_ep)
        self.attach_child(self.character_ap)

        position = self.character_name.property('TransformProperty').position
        position.x = 68
        position.y = 4

        position = self.character_hp.property('TransformProperty').position
        position.x = 136
        position.y = 4

        position = self.character_ep.property('TransformProperty').position
        position.x = 196
        position.y = 4

        position = self.character_ap.property('TransformProperty').position
        position.x = 256
        position.y = 4

    def update(self, character):
        self.character = character

        self.character_name.update(self.character.name)
        self.character_hp.update(self.character.attributes.health)
        self.character_ep.update(self.character.attributes.energy)

    def equal(self, character):
        if self.character == character:
            return True

        return False


class PartyView(GameObject):

    _initialized = False

    def __init__(self):
        super(PartyView, self).__init__()
        self.object_class = 'PartyView'

        _battle_logic = GameObject.get_object_pool().select_with_label("BattleLogic")[0]

        self.characters_status = list()
        self.current_character_status = None

    def _initialize(self):
        PartyView._initialized = True
        print("PartyView initialized")

        _battle_logic = GameObject.get_object_pool().select_with_label("BattleLogic")[0]
        self.current_character = _battle_logic.current_character

        self.ally = GameObject.get_object_pool().select_with_label('CharacterModel')[0].ally
        self.add_property('TransformProperty')
        self.position = self.property('TransformProperty').position
        self.position.x = 16
        self.position.y = 200

        self.current_character_status = CurrentPartyCharacterView(self.current_character)

    def setup_party(self):
        _battle_logic = GameObject.get_object_pool().select_with_label("BattleLogic")[0]

        step = 0
        for character in self.ally():
            if character == self.current_character:
                print(f'Current Character in PartyView: {character.name}')

            line = PartyCharacterView(character)

            position = line.property('TransformProperty').position
            position.y = 40
            position.y += step
            step += 28
            position.x = 0

            self.attach_child(line)
            self.characters_status.append(line)

    def on_create(self):
        pass

    def on_script(self):
        if not PartyView._initialized and CharacterModel._initialized:
            self._initialize()
        else:
            pass

        if PartyView._initialized:
            pass

    def on_signal(self, signal):
        if PartyView._initialized:
            if signal.type == BattleLogic.STATUS_RESET_SIGNAL:
                self.setup_party()
            if signal.type == BattleLogic.STATUS_UPDATE_SIGNAL:
                self._on_status_update()

    def _on_status_update(self):
        _battle_logic = GameObject.get_object_pool().select_with_label("BattleLogic")[0]
        for line in self.characters_status:
            if line.equal(self.current_character):
                print(f'Current Character in PartyView: {self.current_character.name}')
                self.current_character_status.update(self.current_character)

            line.update()

        self.draw_view()

    def draw_view(self):
        pass
