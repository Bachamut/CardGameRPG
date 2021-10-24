import pygame
from property.initialize_property import InitializeProperty, InitializeState

from assets.lib.battle_system.log import Logs
from assets.lib.card_utilities.card_manager import CardManager
from assets.lib.game_object_shared_resource import GameObjectSharedResource
from assets.lib.ui.base_ui.text_box import TextBox
from assets.lib.ui.base_ui.text_line import TextLine
from assets.lib.ui.container import Container


class CardViewController(GameObjectSharedResource):

    def __init__(self):
        super(CardViewController, self).__init__()

        self.font_faces = dict()
        self.interline = 20

        # Used to determine whether View update is required
        # Otherwise View is not updated to increase rendering performance
        self._lock_update_on_hand = list()
        self._lock_update_on_character = None
        self._lock_update_on_selected_card = None
        self._lock_update_on_confirmed_card = None
        self.elements = dict()

    def _initialize(self):

        if InitializeProperty.check_is_ready(self, InitializeState.INITIALIZED):
            super(CardViewController, self)._initialize()
            InitializeProperty.initialize_enable(self)
            Logs.InfoMessage.simple_info(self, "CardView.Controller Initialized [ OK ]")

            self.prepare_font_faces()

            container = Container()
            self.attach_child(container)
            container.property('TransformProperty').position.x = 240
            container.property('TransformProperty').position.y = 600

            text_line = TextLine(self.font_faces['open_sans_normal'], (0, 0, 0), "CardView.Controller")
            container.attach_child(text_line)
            text_line.render()

            text_line = TextLine(self.font_faces['open_sans_normal'], (0, 0, 0), "CurrentCharacterName:")
            container.attach_child(text_line)
            self.elements['character_name'] = text_line
            text_line.property('TransformProperty').position.x = 240
            text_line.render()

            text_box = TextBox(self.font_faces['open_sans_normal']).update("No Cards", (0, 0, 0))
            container.attach_child(text_box)
            self.elements['card_list'] = text_box
            text_box.property('TransformProperty').position.y = 24

            return

        if InitializeProperty.check_is_ready(self, InitializeState.STARTED):

            if self.current_character is None:

                return

            InitializeProperty.started(self)
            # # self.property('SignalProperty').property_enable()
            self.property('ScriptProperty').property_enable()
            Logs.InfoMessage.simple_info(self, "CardView.Controller Started [ OK ]")

            return

    def on_script(self):

        if not self.update_required():

            return

        self.lock_update()
        Logs.InfoMessage.simple_info(self, f'CardView.Controller OnScript Update locked on {self._lock_update_on_character.name}')
        self.elements['character_name'].update(f'CurrentCharacterName:')
        card_list = "No Cards"

        if self.current_character in self.battle_ally:

            self.elements['character_name'].update(f'CurrentCharacterName: {self.current_character.name}')
            if len(self.current_character.hand) != 0:

                card_list = ""
                for card in self.current_character.hand:

                    mark_confirmed_card = ''
                    if self.confirmed_card == card:
                        mark_confirmed_card = '>> '
                    elif self.selected_card == card:
                        mark_confirmed_card = '> '

                    card_list += f'{mark_confirmed_card}{card.card_name} AP: {CardManager.create_battle_card(card).ap_cost}\n'

        self.elements['card_list'].update(f'{card_list}')

    def prepare_font_faces(self):

        self.font_faces['open_sans_normal'] = pygame.font.Font("assets/fonts/open_sans/OpenSans-Regular.ttf", 16)

    def update_required(self):

        # Used to determine whether View update is required
        # Otherwise View is not updated to increase rendering performance

        if self._lock_update_on_character != self.current_character:

            return True

        if self._lock_update_on_selected_card != self.selected_card:

            return True

        if self._lock_update_on_confirmed_card != self.confirmed_card:

            return True

        if len(self._lock_update_on_hand) != len(self.current_character.hand):

            return True

        for index, card in enumerate(self.current_character.hand):

            if card != self._lock_update_on_hand[index]:

                return True

        return False

    def lock_update(self):

        # If View update is required new lock is set to optimise rendering performance

        self._lock_update_on_character = self.current_character
        self._lock_update_on_hand = self.current_character.hand.copy()
        self._lock_update_on_selected_card = self.selected_card
        self._lock_update_on_confirmed_card = self.confirmed_card
