import pygame
from property.initialize_property import InitializeProperty, InitializeState

from assets.lib.battle_system.ai_utilities.ai_condition_manager import AIConditionManager
from assets.lib.battle_system.ai_utilities.ai_process import AIProcess
from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.battle_system.log import Logs
from assets.lib.card_utilities.card_manager import CardManager
from assets.lib.game_object_shared_resource import GameObjectSharedResource


class AIController(GameObjectSharedResource):
    """Control block for AI algorithm"""

    _initialized = False

    def __init__(self):
        super(AIController, self).__init__()

    def _initialize(self):

        if InitializeProperty.check_is_ready(self, InitializeState.INITIALIZED):
            super(AIController, self)._initialize()
            InitializeProperty.initialize_enable(self)
            Logs.InfoMessage.simple_info(self, "AIController Initialized [ OK ]")

            return

        if InitializeProperty.check_is_ready(self, InitializeState.STARTED):
            InitializeProperty.started(self)
            self.property('SignalProperty').property_enable()
            Logs.InfoMessage.simple_info(self, "AIController Started [ OK ]")

            return

    def on_script(self):
        pass

    def on_event(self, event):
        pass

    def on_signal(self, signal):

        # AICS1
        if signal.type == BattleLogic.AI_CONTROLLER_SIGNAL and signal.subtype == "INITIAL":
            Logs.DebugMessage.signal_received(self, signal, "AICS1<-BLS4")

            for character in (self.battle_ally + self.battle_enemies):
                AIConditionManager.create_condition_blocks(character)

            emit_signal = pygame.event.Event(BattleLogic.AI_CONTROLLER_RESPONSE, {"event": "AI_CONTROLLER_RESPONSE", "subtype": "INITIAL"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.signal_emit(self, emit_signal, "AICS1->BL1")
            return

        # AIC1
        if signal.type == BattleLogic.AI_CONTROLLER_SIGNAL and signal.subtype == "STANDARD":
            Logs.DebugMessage.signal_received(self, signal, "AIC1<-BL8")

            if self.current_character.state == 'alive':

                best_pairs = AIProcess.action_calculation(self.current_character, self.battle_ally + self.battle_enemies)
                self.get_confirmed_objects(best_pairs)

                # Check if value of action is positive
                if self.action_validation(best_pairs):

                    Logs.AIControllerMessage.ai_choice_info(self, CardManager.create_battle_card(self.confirmed_card), self.confirmed_target)

                    emit_signal = pygame.event.Event(BattleLogic.AI_CONTROLLER_RESPONSE, {"event": "AI_CONTROLLER_RESPONSE", "subtype": "STANDARD"})
                    pygame.event.post(emit_signal)
                    Logs.DebugMessage.signal_emit(self, emit_signal, "AIC1->BL13")
                    return

            Logs.AIControllerMessage.ai_controller_simple_info('Turn skipped')

            emit_signal = pygame.event.Event(BattleLogic.BATTLE_LOGIC_SIGNAL, {"event": "BATTLE_LOGIC_SIGNAL", "subtype": "NO_ACTION"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.signal_emit(self, emit_signal, "AIC1->?BL100")
            return

    def get_confirmed_objects(self, best_pairs):

        self.confirmed_card = next(iter(best_pairs))
        self.confirmed_target.append(best_pairs[self.confirmed_card][0])

    def action_validation(self, best_pairs):

        action_value = best_pairs[self.confirmed_card][1]

        if action_value > 0:
            return True
        else:
            return False
