import pygame
from property.initialize_property import InitializeProperty, InitializeState

from assets.lib.battle_system.log import Logs
from assets.lib.game_object_shared_resource import GameObjectSharedResource
from assets.lib.ui.base_ui.text_line import TextLine
from assets.lib.ui.container import Container


class BattleCharacterStatusLockUpdate:

    def __init__(self):

        self._lock_update_on_health = None
        self._lock_update_on_energy = None
        self._lock_update_on_action_points = None

    def update_required(self, character):

        # Used to determine whether View update is required
        # Otherwise View is not updated to increase rendering performance

        if self._lock_update_on_health != character.base_attributes.health:

            return True

        if self._lock_update_on_energy != character.base_attributes.energy:

            return True

        if self._lock_update_on_action_points != character.base_attributes.action_points:

            return True

        return False

    def lock_update(self, character):

        # If View update is required new lock is set to optimise rendering performance

        self._lock_update_on_health = character.base_attributes.health
        self._lock_update_on_energy = character.base_attributes.energy
        self._lock_update_on_action_points = character.base_attributes.action_points

class BattleCharacterStatusViewController(GameObjectSharedResource):

    def __init__(self):
        super(BattleCharacterStatusViewController, self).__init__()

        self.font_faces = dict()
        self.interline = 20

        self.character_lines = dict()

        # Used to determine whether View update is required
        # Otherwise View is not updated to increase rendering performance
        self._lock_update_on_status = dict()
        self._lock_update_on_character = None

    def _initialize(self):

        if InitializeProperty.check_is_ready(self, InitializeState.INITIALIZED):
            super(BattleCharacterStatusViewController, self)._initialize()
            InitializeProperty.initialize_enable(self)
            Logs.InfoMessage.simple_info(self, "BattleCharacterStatusView.Controller Initialized [ OK ]")

            self.prepare_font_faces()

            return

        if InitializeProperty.check_is_ready(self, InitializeState.STARTED):

            container = Container()
            self.attach_child(container)
            container.property('TransformProperty').position.x = 20
            container.property('TransformProperty').position.y = 20

            interline = 0
            for character in self.battle_ally + self.battle_enemies:

                # Setup TextLine to display Character Status
                text_line = TextLine(self.font_faces['open_sans_normal'], (0, 0, 0), f'{character.name} HP:{character.base_attributes.health} EN:{character.base_attributes.energy} AP:{character.base_attributes.action_points}').render()
                container.attach_child(text_line)
                self.character_lines[character] = text_line
                text_line.property('TransformProperty').position.y = interline
                interline += self.interline

                # Setup structure used to determine whether View update is required
                self._lock_update_on_status[character] = BattleCharacterStatusLockUpdate()
                self._lock_update_on_status[character].lock_update(character)

            InitializeProperty.started(self)
            self.property('ScriptProperty').property_enable()
            Logs.InfoMessage.simple_info(self, "BattleCharacterStatusView.Controller Started [ OK ]")

            return

    def on_script(self):

        if not self.update_required():

            return

        self.lock_update()
        Logs.InfoMessage.simple_info(self, f'BattleCharacterStatusView.Controller OnScript Update locked')
        for character, text_line in self.character_lines.items():

            mark_current_character = ''
            if self.current_character == character:
                mark_current_character = '>'

            update_text = f'{mark_current_character}{character.name} HP:{character.base_attributes.health} EN:{character.battle_attributes.energy} AP:{character.battle_attributes.action_points}'
            self.character_lines[character].update(update_text)

    def prepare_font_faces(self):

        self.font_faces['open_sans_normal'] = pygame.font.Font("assets/fonts/open_sans/OpenSans-Regular.ttf", 16)

    def update_required(self):

        if self._lock_update_on_character != self.current_character:

            return True

        for character, text_line in self.character_lines.items():

            if self._lock_update_on_status[character].update_required(character):

                return True

    def lock_update(self):

        self._lock_update_on_character = self.current_character
        for character, text_line in self.character_lines.items():

            self._lock_update_on_status[character].lock_update(character)
