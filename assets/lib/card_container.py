import pygame

from assets.lib.card_manager import CardManager
from assets.lib.game_logic import GameLogic
from game_object.game_object import GameObject


class CardContainer(GameObject):

    def __init__(self):
        super(CardContainer, self).__init__()
        self._initialized = False

        self.position = None
        self.onboard_cards = []
        self.selected_card = 0


    def on_create(self):
        self.position = self.property('TransformProperty').position
        self.position.y = 576
        self.position.x = 24

    def _initialize(self):
        self._initialized = True

        step = 0
        for key, value in GameLogic.current_player.deck.items():
            for number in range(0, value):
                card = CardManager.create_card(key)
                card.object_class = 'Card'
                card.object_type = 'Card'
                card.object_label = card.card_name
                card.add_property('TransformProperty')
                card.add_property('BlitProperty')
                card.add_property('SpriteProperty')
                card.add_property('TranslateProperty')
                card.property('SpriteProperty').set_resource(CardManager.card_config[key]['resource'])
                card.on_create()

                position = card.property('TransformProperty').position
                position.x += step
                step += 128
                position.y = 576

                GameObject.add_new_object(card)
                self.attach_child(card)
                self.onboard_cards.append(card)
                self.onboard_cards[0].selected = True

    def on_script(self):
        if not self._initialized and GameLogic.initialized:
            self._initialize()
        else:
            pass

        for card in self.onboard_cards:
            if card.selected == True:
                position = card.property('TransformProperty').position
                position.y = 0
            elif card.selected == False:
                position = card.property('TransformProperty').position
                position.y = 16

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            self._on_arrow_right(event)
            self._on_arrow_left(event)

    def _on_arrow_right(self, event):
        if event.key == pygame.K_RIGHT:
            if self.selected_card < 2:
                self.onboard_cards[self.selected_card].selected = False
                self.selected_card += 1
                print(f'{self.selected_card}')
                self.onboard_cards[self.selected_card].selected = True

    def _on_arrow_left(self, event):
        if event.key == pygame.K_LEFT:
            if self.selected_card > 0:
                self.onboard_cards[self.selected_card].selected = False
                self.selected_card -= 1
                print(f'{self.selected_card}')
                self.onboard_cards[self.selected_card].selected = True