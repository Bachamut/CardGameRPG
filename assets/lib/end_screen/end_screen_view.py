import pygame
from game_object.game_object import GameObject
from property.initialize_property import InitializeProperty, InitializeState

from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.battle_system.log import Logs
from assets.lib.project_controller.project_controller import ProjectController
from assets.lib.ui.base_ui.text_line import TextLine
from assets.lib.ui.base_ui.text_box import TextBox
from assets.lib.ui.container import Container


class EndScreenView(GameObject):

    def __init__(self):
        super(EndScreenView, self).__init__()
        self.messages = dict()
        self.font_faces = dict()

    def _initialize(self):

        if InitializeProperty.check_is_ready(self, InitializeState.INITIALIZED):
            InitializeProperty.initialize_enable(self)
            Logs.InfoMessage.simple_info(self, "EndScreen.View Initialized [ OK ]")

            self.prepare_font_faces()
            self.prepare_messages()

            return

        if InitializeProperty.check_is_ready(self, InitializeState.STARTED):
            InitializeProperty.started(self)
            self.property('ScriptProperty').property_enable()
            self.property('EventProperty').property_enable()
            self.property('SignalProperty').property_enable()
            Logs.InfoMessage.simple_info(self, "EndScreen.View Started [ OK ]")

            self.timer_event = pygame.event.custom_type()
            pygame.time.set_timer(self.timer_event, 5000)

            self.wait = True
            self.show = False
            self.wait_to_press = False
            self.start_time = pygame.time.get_ticks()

            self.property('InitializeProperty').property_disable()

            return

    def on_script(self):

        current_time = pygame.time.get_ticks()

        if self.wait:
            if current_time - self.start_time >= 1000:
                self.wait = False
                self.show = True

                # print(self.start_time)
                self.start_time = pygame.time.get_ticks()

        if self.show:
            diff = current_time - self.start_time
            # print(diff)
            if diff < 256 * 10.5:
                for msg, tb in self.messages.items():
                    if type(tb) == TextBox:
                        for line in tb._text_lines:
                            line.property('SpriteProperty').set_alpha(diff / 10.5)
            if current_time - self.start_time >= 255 * 10.5:
                for msg, tb in self.messages.items():
                    if type(tb) == TextBox:
                        for line in tb._text_lines:
                            line.property('SpriteProperty').set_alpha(255)
                self.show = False

        pass

    def on_event(self, event):

        if event.type == self.timer_event:
            print("Timer event")
            self.messages['continue'].property('SpriteProperty').set_alpha(255)
            pygame.time.set_timer(self.timer_event, 0)

            self.wait_to_press = True

        if self.wait_to_press and event.type == pygame.KEYDOWN:

            pygame.time.set_timer(ProjectController.START_MAIN_MENU_SCENE_TIME_EVENT, 900)

    def on_signal(self, signal):

        if signal.type == BattleLogic.BATTLE_LOGIC_SIGNAL and signal.subtype == "BATTLE_LOST":

            pass

        if signal.type == BattleLogic.BATTLE_LOGIC_SIGNAL and signal.subtype == "BATTLE_WON":

            pass

    def prepare_font_faces(self):

        self.font_faces['roboto_h1'] = pygame.font.Font("assets/fonts/roboto/Roboto-Regular.ttf", 56)
        self.font_faces['open_sans_normal'] = pygame.font.Font("assets/fonts/open_sans/OpenSans-Regular.ttf", 16)
        self.font_faces['noto_sans_jp_h1'] = pygame.font.Font("assets/fonts/noto_sans_jp/NotoSansJP-Regular.otf", 24)
        self.font_faces['noto_sans_jp_normal'] = pygame.font.Font("assets/fonts/noto_sans_jp/NotoSansJP-Regular.otf", 16)

    def prepare_messages(self):

        main_container = Container()
        self.attach_child(main_container)
        main_container.property('TransformProperty').position.x = 240
        main_container.property('TransformProperty').position.y = 370

        container_en = Container()
        main_container.attach_child(container_en)
        container_en.property('TransformProperty').position.y = 0

        message = "YOU DIED"
        text_box = TextBox(self.font_faces['roboto_h1'])
        container_en.attach_child(text_box)
        text_box.update(message, (255, 255, 255))
        text_box.property('TransformProperty').position.y = 0
        text_box.property('TransformProperty').position.x = 260
        self.messages['en_title'] = text_box

        message = "[Press any key to continue]"
        text_line = TextLine(self.font_faces['open_sans_normal'], (255, 255, 255), message)
        main_container.attach_child(text_line)
        text_line.property('TransformProperty').position.x = 760
        text_line.property('TransformProperty').position.y = 540
        text_line.render()

        text_line.property('SpriteProperty').set_alpha(40)
        self.messages['continue'] = text_line

        for msg, tb in self.messages.items():
            if type(tb) == TextBox:
                for line in tb._text_lines:
                    line.property('SpriteProperty').set_alpha(0)
