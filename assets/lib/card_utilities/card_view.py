import pygame
from asserts.type_assert import TypeAssert

from assets.lib.battle_system.action_utilities.action_process import ActionProcess
from assets.lib.card_utilities.card_model import FullCard
from assets.lib.game_object_shared_resource import GameObjectSharedResource
from assets.lib.ui.base_ui.text_box import TextBox
from assets.lib.ui.container import Container


class HandCardView(GameObjectSharedResource):

    def __init__(self, full_card_model):
        TypeAssert.equal(full_card_model, FullCard)
        super(HandCardView, self).__init__()

        self.messages = dict()
        self.font_faces = dict()

        self.object_class = 'HandCardView'
        self.object_label = full_card_model.card_type
        self.object_type = 'CardView'

        # Set reference to model
        self._model = full_card_model

        # Add Object Properties
        self.add_property('TransformProperty')
        self.add_property('SpriteProperty')
        self.add_property('BlitProperty')

        # Configure Object Properties
        config = {'package': 'card_assets', 'set_resource': self._model.resource_name}
        self.property('SpriteProperty').configure(config)

        self.prepare_font_faces()
        self.prepare_content()

    def prepare_content(self):

        # Main container
        main_container = Container()
        self.attach_child(main_container)
        main_container.property('TransformProperty').position.x = 0
        main_container.property('TransformProperty').position.y = 0

        # Title container
        title_bar = Container()
        main_container.attach_child(title_bar)
        title_bar.property('TransformProperty').position.x = 0
        title_bar.property('TransformProperty').position.y = 0

        message = self._model.card_name
        text_box = TextBox(self.font_faces['roboto_h1'])
        title_bar.attach_child(text_box)
        text_box.update(message, (0, 0, 0))
        text_box.property('TransformProperty').position.x = 28
        text_box.property('TransformProperty').position.y = 121

        self.messages['title_bar'] = text_box

        ap_cost = Container()
        main_container.attach_child(ap_cost)
        title_bar.property('TransformProperty').position.x = 0
        title_bar.property('TransformProperty').position.y = 0

        message = self._model.ap_cost
        text_box = TextBox(self.font_faces['roboto_h3'])
        ap_cost.attach_child(text_box)
        text_box.update(message, (255, 255, 255))
        text_box.property('TransformProperty').position.x = 98
        text_box.property('TransformProperty').position.y = 15

        self.messages['ap_cost'] = text_box


        # Description container
        description_container = Container()
        main_container.attach_child(description_container)
        description_container.property('TransformProperty').position.x = 0
        description_container.property('TransformProperty').position.y = 140

        message = self._model.usage_description
        text_box = TextBox(self.font_faces['roboto_h2'])
        description_container.attach_child(text_box)
        text_box.update(message, (0, 0, 0))
        text_box.property('TransformProperty').position.x = 24
        text_box.property('TransformProperty').position.y = 10

        self.messages['description_container'] = text_box

        # Values container
        values_container = Container()
        main_container.attach_child(values_container)
        values_container.property('TransformProperty').position.x = 0
        values_container.property('TransformProperty').position.y = 150

        message = self.prepare_value_description()
        text_box = TextBox(self.font_faces['roboto_h2'])
        values_container.attach_child(text_box)
        text_box.update(message, (0, 0, 0))
        text_box.property('TransformProperty').position.x = 24
        text_box.property('TransformProperty').position.y = 10

        self.messages['description_container'] = text_box

    def prepare_value_description(self):

        # if self.selected_target:
        #
        #     value = ActionProcess.value_calculation(self.current_character, self.selected_target, self.confirmed_card)

            for attribute, multiplier_value in self._model.attribute_multiplier.items():

                message = "Deal " + str(multiplier_value) + " damage x " + str(attribute)

            return message

    def prepare_font_faces(self):

        self.font_faces['roboto_h1'] = pygame.font.Font("assets/fonts/roboto/Roboto-Regular.ttf", 14)
        self.font_faces['roboto_h2'] = pygame.font.Font("assets/fonts/roboto/Roboto-Regular.ttf", 10)
        self.font_faces['roboto_h3'] = pygame.font.Font("assets/fonts/roboto/Roboto-Regular.ttf", 20)
        self.font_faces['open_sans_normal'] = pygame.font.Font("assets/fonts/open_sans/OpenSans-Regular.ttf", 16)
        self.font_faces['noto_sans_jp_h1'] = pygame.font.Font("assets/fonts/noto_sans_jp/NotoSansJP-Regular.otf", 24)
        self.font_faces['noto_sans_jp_normal'] = pygame.font.Font("assets/fonts/noto_sans_jp/NotoSansJP-Regular.otf", 16)