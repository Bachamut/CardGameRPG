from game_object.game_object import GameObject
from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.battle_system.card_model import CardModel, CARD_VIEW_ON_RISE, CARD_VIEW_ON_FALL
from assets.lib.battle_system.character_model import CharacterModel

class CardView(GameObject):

    _initialized = False

    def __init__(self):
        super(CardView, self).__init__()

    def on_create(self):
        pass

    def _initialize(self):
        CardView._initialized = True
        print("CardView initialized")

        self.selected_card = GameObject.get_object_pool().select_with_label('CardModel')[0].selected_card
        self.onboard_cards = GameObject.get_object_pool().select_with_label('CardModel')[0].onboard_cards
        self.current_character = GameObject.get_object_pool().select_with_label('CardModel')[0].current_character
        self.previous_character = GameObject.get_object_pool().select_with_label('CardModel')[0].previous_character

        self.position = self.property('TransformProperty').position
        self.position.y = 576
        self.position.x = 24

    def on_signal(self, signal):
        if signal.type == CARD_VIEW_ON_RISE:
            self._on_rise()
        if signal.type == CARD_VIEW_ON_FALL:
            self._on_fall()

    def _on_rise(self):

        _card_model = GameObject.get_object_pool().select_with_label("CardModel")[0]
        self.current_character = _card_model.current_character

        print(f'\nCurrent Character: {self.current_character().name}')
        # for card in BattleLogic.current_character.hand:
        #     print(card.card_name)

        step = 0
        for card in self.current_character().hand:
            self.attach_child(card)
            card.property('SpriteProperty').visible = True

            position = card.property('TransformProperty').position
            position.x = 0
            position.x += step
            step += 128
            position.y = 576

        # print(f'\nPrevious Character: {CardModel.previous_character.name}')
        previous = self.current_character
        self.previous_character = previous

    def _on_fall(self):
        #
        # _card_model = GameObject.get_object_pool().select_with_label("CardModel")[0]
        # self.previous_character = _card_model.previous_character

        # print(f'On_Fall')
        print(f'Previous Character: {self.previous_character().name}')

        for card in self.previous_character().hand:
            # self.detach_child(card)
            card.property('SpriteProperty').visible = False

            position = card.property('TransformProperty').position
            position.x = 0

    def on_script(self):
        if not CardView._initialized and CardModel._initialized and CharacterModel._initialized and BattleLogic._initialized and BattleLogic.started:
            self._initialize()
        elif CardView._initialized:

            _card_model = GameObject.get_object_pool().select_with_label("CardModel")[0]
            self.current_character = _card_model.current_character

            for card in self.current_character().hand:
                if card.selected == True:
                    position = card.property('TransformProperty').position
                    position.y = 0
                if card.selected == False:
                    position = card.property('TransformProperty').position
                    position.y = 16
                if card.current == True:
                    position = card.property('TransformProperty').position
                    position.y = -32

    def on_event(self, event):
        pass
