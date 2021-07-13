import pygame

from assets.lib.battle_system.action_types import ActionType
from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.battle_system.character_model import CharacterModel
from assets.lib.battle_system.status import Status
from assets.lib.game_logic import GameLogic
from game_object.game_object import GameObject


class TurnModel(GameObject):

    _initialized = False
    # active = BattleLogic.turn_model_active

    def __init__(self):
        super(TurnModel, self).__init__()

    def _initialize(self):
        TurnModel._initialized = True
        print("TurnModel initialized")

        _battle_logic = GameObject.get_object_pool().select_with_label("BattleLogic")[0]
        self.current_character = _battle_logic.current_character
        self.current_target = _battle_logic.current_target
        self.current_card = _battle_logic.current_card
        self.selected_card = _battle_logic.selected_card

    def on_script(self):
        if not self._initialized and \
                GameLogic._initialized and \
                BattleLogic._initialized and \
                CharacterModel._initialized and \
                BattleLogic.started:
            self._initialize()
        else:
            pass

    def on_event(self, event):
        if BattleLogic.card_model_active and TurnModel._initialized:
            pass


    def on_signal(self, signal):
            if signal.type == BattleLogic.TURN_ACTIVE_SIGNAL:

                BattleLogic.turn_model_active = True

                _battle_logic = GameObject.get_object_pool().select_with_label("BattleLogic")[0]

                TurnModel.action_process(self.current_character, self.current_target, self.current_card)

                BattleLogic.turn_model_active = False

    def current_action(self):
        _battle_logic = GameObject.get_object_pool().select_with_label("BattleLogic")[0]

        if self.current_card.ap_cost <= self.current_character.action_points:
            print(f'Możesz użyć karty')

            TurnModel.action_process(self.current_character, self.current_target, self.current_card)

        if self.current_card.ap_cost > self.current_character.action_points:
            print(f'Nie masz wystarczającej ilości AP')

    @staticmethod
    def action_process(caster, target, card):

        if card.take().action_type == 'magic_attack':
            ActionType.magic_attack(caster, target, card)
        elif card.take().action_type == 'basic_attack':
            ActionType.basic_attack(caster, target, card)
        elif card.take().action_type == 'piercing_attack':
            ActionType.piercing_attack(caster, target, card)
        elif card.take().action_type == 'agile_attack':
            ActionType.agile_attack(caster, target, card)
        elif card.take().action_type == 'magic_spell':
            ActionType.magic_spell(caster, target, card)
        elif card.take().action_type == 'bow_attack':
            ActionType.bow_attack(caster, target, card)

        Status.add_status(caster, target, card)


