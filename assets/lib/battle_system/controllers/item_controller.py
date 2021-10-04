import pygame

from game_object.game_object import GameObject
from resource_manager.shared_resource import SharedResource

from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.battle_system.log import Logs


class ItemController(GameObject):


    _initialized = False

    def __init__(self):
        super(ItemController, self).__init__()

        self._onboard_items = SharedResource()
        self._onboard_items = list()

    def _initialize(self):
        ItemController._initialized = True
        print("ItemController initialized")

    def on_script(self):
            pass

    def on_event(self, event):
        if BattleLogic.card_model_active and ItemController._initialized:
            pass

    def on_signal(self, signal):
        if ItemController._initialized:

            # IC1
            if signal.type == BattleLogic.ITEM_CONTROLLER_SIGNAL and signal.subtype == "STANDARD":
                Logs.DebugMessage.SignalReceived(self, signal, "IC1<-BL9")

                emit_signal = pygame.event.Event(BattleLogic.ITEM_CONTROLLER_RESPONSE, {"event": "ITEM_CONTROLLER_RESPONSE", "subtype": "STANDARD"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.SignalEmit(self, emit_signal, "CC1->BL12")
                return