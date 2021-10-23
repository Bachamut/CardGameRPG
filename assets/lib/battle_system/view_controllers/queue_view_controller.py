import pygame
from game_object.game_object import GameObject
from property.initialize_property import InitializeProperty, InitializeState

from assets.lib.battle_system.controllers.queue_controller import QueueController
from assets.lib.battle_system.log import Logs
from assets.lib.game_object_shared_resource import GameObjectSharedResource
from assets.lib.ui.base_ui.text_box import TextBox
from assets.lib.ui.base_ui.text_line import TextLine
from assets.lib.ui.container import Container


class QueueViewController(GameObjectSharedResource):

    def __init__(self):
        super(QueueViewController, self).__init__()

        self.font_faces = dict()
        self.interline = 20

        self.elements = dict()

        self.queue_controller = None

    def _initialize(self):

        if InitializeProperty.check_is_ready(self, InitializeState.INITIALIZED):
            super(QueueViewController, self)._initialize()
            InitializeProperty.initialize_enable(self)
            Logs.InfoMessage.simple_info(self, "QueueView.Controller Initialized [ OK ]")

            self.prepare_font_faces()

            container = Container()
            self.attach_child(container)
            container.property('TransformProperty').position.x = 1000
            container.property('TransformProperty').position.y = 60

            text_line = TextLine(self.font_faces['open_sans_normal'], (0, 0, 0), "QueueView.Controller")
            container.attach_child(text_line)
            text_line.render()

            text_line = TextLine(self.font_faces['open_sans_normal'], (0, 0, 0), "CurrentCharacterName:")
            container.attach_child(text_line)
            self.elements['character_name'] = text_line
            text_line.property('TransformProperty').position.y = 24
            text_line.render()

            text_box = TextBox(self.font_faces['open_sans_normal']).update("No Queue", (0, 0, 0))
            container.attach_child(text_box)
            self.elements['card_list'] = text_box
            text_box.property('TransformProperty').position.y = 48

            return

        if InitializeProperty.check_is_ready(self, InitializeState.STARTED):

            if self.current_character is None:

                return

            self.queue_controller = GameObject.get_object_pool().select_with_label('QueueController')[0]

            InitializeProperty.started(self)
            # # self.property('SignalProperty').property_enable()
            self.property('ScriptProperty').property_enable()
            Logs.InfoMessage.simple_info(self, "QueueView.Controller Started [ OK ]")

            return

    def on_script(self):

        self.elements['character_name'].update(f'CurrentCharacterName:')
        queue_list = ""

        self.elements['character_name'].update(f'CurrentCharacterName: {self.current_character.name}')

        for character in self.queue_controller.queue:

            mark_confirmed_card = ''
            # if self.confirmed_card == card:
            #     mark_confirmed_card = '>>> '

            queue_list += f'{mark_confirmed_card}{character.name}\n'

        self.elements['card_list'].update(f'{queue_list}')

    def prepare_font_faces(self):

        self.font_faces['open_sans_normal'] = pygame.font.Font("assets/fonts/open_sans/OpenSans-Regular.ttf", 16)