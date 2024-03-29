from game_object.game_object import GameObject
from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.battle_system.controllers.card_controller import CardController
from assets.lib.battle_system.controllers.character_controller import CharacterController


class CardView(GameObject):

    # SharedResources definitions

    @property
    def current_character(self):
        return self._current_character.take()

    @current_character.setter
    def current_character(self, character):
        self._current_character.set(character)

    @property
    def confirmed_target(self):
        return self._confirmed_target.take()

    @confirmed_target.setter
    def confirmed_target(self, character):
        self._confirmed_target.set(character)

    @property
    def selected_target(self):
        return self._selected_target.take()

    @selected_target.setter
    def selected_target(self, target):
        self._selected_target.set(target)

    @property
    def confirmed_card(self):
        return self._confirmed_card.take()

    @confirmed_card.setter
    def confirmed_card(self, card):
        self._confirmed_card.set(card)

    @property
    def selected_card(self):
        return self._selected_card.take()

    @selected_card.setter
    def selected_card(self, card):
        self._selected_card.set(card)

    @property
    def ally(self):
        return self._ally.take()

    @ally.setter
    def ally(self, ally):
        self._ally.set(ally)

    @property
    def enemies(self):
        return self._enemies.take()

    @enemies.setter
    def enemies(self, enemies):
        self._enemies.set(enemies)

    # end SharedResources

    # CardView SharedResources definitions

    @property
    def onboard_cards(self):
        return self._onboard_cards.take()

    @onboard_cards.setter
    def onboard_cards(self, card):
        self._onboard_cards.set(card)

    @property
    def previous_character(self):
        return self._previous_character.take()

    @previous_character.setter
    def previous_character(self, character):
        self._previous_character.set(character)

    # end SharedResources

    _initialized = False

    def __init__(self):
        super(CardView, self).__init__()

    def on_create(self):
        pass

    def _initialize(self):
        CardView._initialized = True
        print("CardView initialized")

        self._card_model = GameObject.get_object_pool().select_with_label('CardController')[0]
        self._selected_card = self._card_model._selected_card
        self._onboard_cards = self._card_model._onboard_cards
        self._current_character = self._card_model._current_character
        self._previous_character = self._card_model._previous_character

        self.position = self.property('TransformProperty').position
        self.position.y = 576
        self.position.x = 24

        # InitializeProperty.started(self)
        self.property('InitializeProperty').property_disable()

    def on_signal(self, signal):
        pass

    def _on_rise(self):
        print(f'\nCurrent Character: {self.current_character.name}')
        # for card in BattleLogic.current_character.hand:
        #     print(card.card_name)

        step = 0
        for card in self.current_character.hand:
            self.attach_child(card)
            card.property('SpriteProperty').visible = True

            position = card.property('TransformProperty').position
            position.x = 0
            position.x += step
            step += 128
            position.y = 576

        # print(f'\nPrevious Character: {CardController.previous_character.name}')
        previous = self.current_character
        self.previous_character = previous

    def _on_fall(self):
        #
        # _card_model = GameObject.get_object_pool().select_with_label("CardController")[0]
        # self.previous_character = _card_model.previous_character

        # print(f'On_Fall')
        print(f'Previous Character: {self.previous_character.name}')

        for card in self.previous_character.hand:
            # self.detach_child(card)
            card.property('SpriteProperty').visible = False

            position = card.property('TransformProperty').position
            position.x = 0

    def on_script(self):
        if not CardView._initialized and CardController._initialized and CharacterController._initialized and BattleLogic._initialized and BattleLogic.started:
            self._initialize()
        elif CardView._initialized:
            pass
            # for card in self.current_character.hand:
            #     if card.selected == True:
            #         position = card.property('TransformProperty').position
            #         position.y = 0
            #     if card.selected == False:
            #         position = card.property('TransformProperty').position
            #         position.y = 16
            #     if card.current == True:
            #         position = card.property('TransformProperty').position
            #         position.y = -32

    def on_event(self, event):
        pass
