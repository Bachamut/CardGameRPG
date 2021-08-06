import pygame

from assets.lib.battle_system.action_types import ActionType
from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.battle_system.character_model import CharacterModel
from assets.lib.battle_system.log import Logs
from assets.lib.battle_system.status import Status
from assets.lib.game_logic import GameLogic
from game_object.game_object import GameObject


class TurnModel(GameObject):

    # SharedResources definitions

    @property
    def current_character(self):
        return self._current_character.take()

    @current_character.setter
    def current_character(self, character):
        self._current_character.set(character)

    @property
    def current_target(self):
        return self._current_target.take()

    @current_target.setter
    def current_target(self, character):
        self._current_target.set(character)

    @property
    def selected_target(self):
        return self._selected_target.take()

    @selected_target.setter
    def selected_target(self, target):
        self._selected_target.set(target)

    @property
    def current_card(self):
        return self._current_card.take()

    @current_card.setter
    def current_card(self, card):
        self._current_card.set(card)

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

    _initialized = False
    # active = BattleLogic.turn_model_active

    def __init__(self):
        super(TurnModel, self).__init__()

    def _initialize(self):
        TurnModel._initialized = True
        print("TurnModel initialized")

        _battle_logic = GameObject.get_object_pool().select_with_label("BattleLogic")[0]
        self._current_character = _battle_logic._current_character
        self._current_target = _battle_logic._current_target
        self._current_card = _battle_logic._current_card
        self._selected_card = _battle_logic._selected_card

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

        if signal.type == BattleLogic.ACTION_MODEL_SIGNAL and signal.subtype == "PRE_TURN":
            Logs.DebugMessage.SignalReceived(self, signal)

            signal = pygame.event.Event(BattleLogic.ACTION_MODEL_RESPONSE, {"event": "ACTION_MODEL_RESPONSE", "subtype": "PRE_TURN"})
            pygame.event.post(signal)
            Logs.DebugMessage.SignalEmit(self, signal)
            pass

        if signal.type == BattleLogic.ACTION_MODEL_SIGNAL and signal.subtype == "PRE_DRAW":
            Logs.DebugMessage.SignalReceived(self, signal)

            signal = pygame.event.Event(BattleLogic.ACTION_MODEL_RESPONSE, {"event": "ACTION_MODEL_RESPONSE", "subtype": "PRE_DRAW"})
            pygame.event.post(signal)
            Logs.DebugMessage.SignalEmit(self, signal)
            pass

        if signal.type == BattleLogic.ACTION_MODEL_SIGNAL and signal.subtype == "POST_DRAW":
            Logs.DebugMessage.SignalReceived(self, signal)

            signal = pygame.event.Event(BattleLogic.ACTION_MODEL_RESPONSE, {"event": "ACTION_MODEL_RESPONSE", "subtype": "POST_DRAW"})
            pygame.event.post(signal)
            Logs.DebugMessage.SignalEmit(self, signal)
            pass
        pass

    def current_action(self):
        if self.current_card.ap_cost <= self.current_character.action_points:
            print(f'Możesz użyć karty')

            TurnModel.action_process(self.current_character, self.current_target, self.current_card)

        if self.current_card.ap_cost > self.current_character.action_points:
            print(f'Nie masz wystarczającej ilości AP')

    @staticmethod
    def action_process(caster, target, card):

        if card.action_type == 'magic_attack':
            ActionType.magic_attack(caster, target, card)
        elif card.action_type == 'basic_attack':
            ActionType.basic_attack(caster, target, card)
        elif card.action_type == 'piercing_attack':
            ActionType.piercing_attack(caster, target, card)
        elif card.action_type == 'agile_attack':
            ActionType.agile_attack(caster, target, card)
        elif card.action_type == 'magic_spell':
            ActionType.magic_spell(caster, target, card)
        elif card.action_type == 'bow_attack':
            ActionType.bow_attack(caster, target, card)

        Status.add_status(caster, target, card)


