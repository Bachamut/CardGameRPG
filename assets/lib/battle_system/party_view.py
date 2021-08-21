import pygame

from game_object.game_object import GameObject
from assets.lib.battle_system.character_model import CharacterModel
from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.battle_system.party_character_view import PartyCharacterView, CharacterIcon, CharacterName, AttributeLine


class CurrentPartyCharacterView(GameObject):

    # SharedResources definitions

    @property
    def character(self):
        return self._character.take()

    @character.setter
    def character(self, character):
        self._character.set(character)

    # end SharedResources

    def __init__(self, character):
        super(CurrentPartyCharacterView, self).__init__()
        self.object_class = 'PartyCharacterView'

        self._character = character

        self.add_property('TransformProperty')
        self.position = self.property('TransformProperty').position

        self.character_icon = CharacterIcon()
        self.character_name = CharacterName(self.character.name)
        self.character_hp = AttributeLine("HP", self.character.base_attributes.health, (0, 204, 10))
        self.character_ep = AttributeLine("EP", self.character.base_attributes.energy, (0, 92, 204))
        self.character_ap = AttributeLine("AP", self.character.base_attributes.action_points, (204, 112, 0))

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
        self._character = character

        self.character_name.update(self.character.name)
        self.character_hp.update(self.character.base_attributes.health)
        self.character_ep.update(self.character.base_attributes.energy)

    def equal(self, character):
        if self.character == character:
            return True

        return False


class PartyView(GameObject):

    # SharedResources definitions

    @property
    def current_character(self):
        return self._current_character.take()

    @current_character.setter
    def current_character(self, character):
        self._current_character.set(character)

    @property
    def current_target(self):
        return self._current_target.take()

    @current_target.setter
    def current_target(self, character):
        self._current_target.set(character)

    @property
    def selected_target(self):
        return self._selected_target.take()

    @selected_target.setter
    def selected_target(self, target):
        self._selected_target.set(target)

    @property
    def current_card(self):
        return self._current_card.take()

    @current_card.setter
    def current_card(self, card):
        self._current_card.set(card)

    @property
    def selected_card(self):
        return self._selected_card.take()

    @selected_card.setter
    def selected_card(self, card):
        self._selected_card.set(card)

    @property
    def battle_ally(self):
        return self._battle_ally.take()

    @battle_ally.setter
    def battle_ally(self, ally):
        self._battle_ally.set(ally)

    @property
    def enemies(self):
        return self._enemies.take()

    @enemies.setter
    def enemies(self, enemies):
        self._enemies.set(enemies)

    # end SharedResources

    _initialized = False

    def __init__(self):
        super(PartyView, self).__init__()
        self.object_class = 'PartyView'

        # TODO: Modele powinny mieć unikatową nazwę _model (?)
        _character_model = GameObject.get_object_pool().select_with_label("CharacterModel")[0]
        self._current_character = _character_model._current_character

        self.characters_status = list()
        self.current_character_status = None

    def _initialize(self):
        PartyView._initialized = True
        print("PartyView initialized")

        self._battle_ally = GameObject.get_object_pool().select_with_label('CharacterModel')[0]._battle_ally
        self.add_property('TransformProperty')
        self.position = self.property('TransformProperty').position
        self.position.x = 16
        self.position.y = 200

        #self.current_character_status = CurrentPartyCharacterView(self._current_character)

    def setup_party(self):
        step = 0
        for character in self.ally:
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
            pass

    def _on_status_update(self):
        for line in self.characters_status:
            if line.equal(self.current_character):
                print(f'Current Character in PartyView: {self.current_character.name}')
                self.current_character_status.update(self._current_character)

            line.update()

        self.draw_view()

    def draw_view(self):
        pass
