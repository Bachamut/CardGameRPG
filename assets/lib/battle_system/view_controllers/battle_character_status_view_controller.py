import pygame
from property.initialize_property import InitializeProperty, InitializeState

from assets.lib.battle_system.log import Logs
from assets.lib.game_object_shared_resource import GameObjectSharedResource
from assets.lib.ui.base_ui.text_line import TextLine
from assets.lib.ui.container import Container


class BattleCharacterStatusViewController(GameObjectSharedResource):

    def __init__(self):
        super(BattleCharacterStatusViewController, self).__init__()

        self.font_faces = dict()
        self.interline = 20

        self.character_lines = dict()

    def _initialize(self):

        if InitializeProperty.check_is_ready(self, InitializeState.INITIALIZED):
            super(BattleCharacterStatusViewController, self)._initialize()
            InitializeProperty.initialize_enable(self)
            Logs.InfoMessage.SimpleInfo(self, "BattleCharacterStatusView.Controller Initialized [ OK ]")

            self.prepare_font_faces()

            return

        if InitializeProperty.check_is_ready(self, InitializeState.STARTED):

            container = Container()
            self.attach_child(container)
            container.property('TransformProperty').position.x = 20
            container.property('TransformProperty').position.y = 20

            interline = 0
            for character in self.battle_ally:

                text_line = TextLine(self.font_faces['open_sans_normal'], (0, 0, 0), f'{character.name} HP:{character.base_attributes.health} EN:{character.base_attributes.energy} AP:{character.base_attributes.action_points}').render()
                container.attach_child(text_line)
                self.character_lines[character] = text_line
                text_line.property('TransformProperty').position.y = interline
                interline += self.interline

            InitializeProperty.started(self)
            # self.property('SignalProperty').property_enable()
            self.property('ScriptProperty').property_enable()
            Logs.InfoMessage.SimpleInfo(self, "BattleCharacterStatusView.Controller Started [ OK ]")

            return

    def on_script(self):

        for character, text_line in self.character_lines.items():

            mark_current_character = ''
            if self.current_character == character:
                mark_current_character = '>'

            update_text = f'{mark_current_character}{character.name} HP:{character.base_attributes.health} EN:{character.base_attributes.energy} AP:{character.base_attributes.action_points}'
            self.character_lines[character].update(update_text)

    def prepare_font_faces(self):

        self.font_faces['open_sans_normal'] = pygame.font.Font("assets/fonts/open_sans/OpenSans-Regular.ttf", 16)
