import pygame
from property.initialize_property import InitializeProperty, InitializeState

from assets.lib.battle_system.ai_utilities.ai_condition_manager import AIConditionManager
from assets.lib.battle_system.ai_utilities.ai_process import AIProcess
from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.battle_system.log import Logs
from assets.lib.game_object_shared_resource import GameObjectSharedResource


class AIController(GameObjectSharedResource):
    """Control block for AI algorithm"""

    _initialized = False

    def __init__(self):
        super(AIController, self).__init__()

    def _initialize(self):

        if InitializeProperty.check_status(self, InitializeState.INITIALIZED):
            super(AIController, self)._initialize()
            InitializeProperty.initialize_enable(self)
            Logs.InfoMessage.SimpleInfo(self, "AIController Initialized [ OK ]")

            return

        if InitializeProperty.check_status(self, InitializeState.STARTED):
            InitializeProperty.started(self)
            self.property('SignalProperty').property_enable()
            Logs.InfoMessage.SimpleInfo(self, "AIController Started [ OK ]")

            return

    def on_script(self):
        pass

    def on_event(self, event):
        pass

    def on_signal(self, signal):

        # AICS1
        if signal.type == BattleLogic.AI_CONTROLLER_SIGNAL and signal.subtype == "INITIAL":
            Logs.DebugMessage.SignalReceived(self, signal, "AICS1<-BLS4")

            for character in (self.battle_ally + self.battle_enemies):
                AIConditionManager.create_condition_blocks(character)

            emit_signal = pygame.event.Event(BattleLogic.AI_CONTROLLER_RESPONSE, {"event": "AI_CONTROLLER_RESPONSE", "subtype": "INITIAL"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "AICS1->BL1")
            return

        # AIC1
        if signal.type == BattleLogic.AI_CONTROLLER_SIGNAL and signal.subtype == "STANDARD":
            Logs.DebugMessage.SignalReceived(self, signal, "AIC1<-BL8")

            best_card, best_character = AIProcess.action_calculation(self.current_character, self.battle_ally + self.battle_enemies)

            self.confirmed_card = best_card
            self.confirmed_target.append(best_character)

            print(f'\nAI choosing action')

            emit_signal = pygame.event.Event(BattleLogic.AI_CONTROLLER_RESPONSE, {"event": "AI_CONTROLLER_RESPONSE", "subtype": "STANDARD"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "AIC1->BL13")
            return
