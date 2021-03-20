from assets.lib.battle_logic import BattleLogic
from assets.lib.card_model import CardModel
from assets.lib.character_model import CharacterModel
from game_object.game_object import GameObject


class CardView(GameObject):

    _initialized = False

    def __init__(self):
        super(CardView, self).__init__()
        self.onboard_cards = None
        self.selected_card = None
    #     self.position = None



    def on_create(self):
        pass

    def _initialize(self):
        CardView._initialized = True
        self.character = BattleLogic.current_character
        self.position = self.property('TransformProperty').position
        self.position.y = 576
        self.position.x = 24
        self.onboard_cards = CardModel.onboard_cards
        self.selected_card = CardModel.selected_card

        #     step = 0
    #     for key, value in CharacterView.current_character.deck.items():
    #         for number in range(0, value):
    #             card = CardManager.create_card(key)
    #             card.object_class = 'Card'
    #             card.object_type = 'Card'
    #             card.object_label = card.card_name
    #             card.add_property('TransformProperty')
    #             card.add_property('BlitProperty')
    #             card.add_property('SpriteProperty')
    #             card.add_property('TranslateProperty')
    #             card.property('SpriteProperty').set_resource(CardManager.card_config[key]['resource'])
    #             card.on_create()
    #
    #             position = card.property('TransformProperty').position
    #             position.x += step
    #             step += 128
    #             position.y = 576
    #
    #             GameObject.add_new_object(card)
    #             self.attach_child(card)
    #             self.onboard_cards.append(card)
    #             self.onboard_cards[0].selected = True

    def on_rise(self):
        step = 0
        for card in self.character.hand:
            self.attach_child(card)
            card.property('SpriteProperty').visible = True

            position = card.property('TransformProperty').position
            position.x = 0
            position.x += step
            step += 128
            position.y = 576

    def on_fall(self):
        for card in self.character.hand:
            card.property('SpriteProperty').visible = False

            position = card.property('TransformProperty').position
            position.x = 0

    def on_script(self):
        if not CardView._initialized and CardModel._initialized and CharacterModel._initialized and BattleLogic._initialized and BattleLogic.started:
            self._initialize()
        elif CardView._initialized:

            for card in self.character.hand:
                if card.selected == True:
                    position = card.property('TransformProperty').position
                    position.y = 0
                elif card.selected == False:
                    position = card.property('TransformProperty').position
                    position.y = 16

    def on_event(self, event):
        pass
