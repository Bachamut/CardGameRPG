import pygame

from game_object.game_object import GameObject
from resource_manager.shared_resource import SharedResource

from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.battle_system.character_model import CharacterModel
from assets.lib.battle_system.log import Logs
from assets.lib.game_logic import GameLogic


class ItemModel(GameObject):

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

    # ItemModel SharedResources definitions

    # end SharedResources

    _initialized = False

    def __init__(self):
        super(ItemModel, self).__init__()

        self._onboard_items = SharedResource()
        self._onboard_items = list()

    def _initialize(self):
        ItemModel._initialized = True
        print("ItemModel initialized")

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
        if BattleLogic.card_model_active and ItemModel._initialized:
            pass

    def on_signal(self, signal):
        if ItemModel._initialized:

            # IM1
            if signal.type == BattleLogic.ITEM_MODEL_SIGNAL and signal.subtype == "STANDARD":
                Logs.DebugMessage.SignalReceived(self, signal, "IM1<-BL9")

                emit_signal = pygame.event.Event(BattleLogic.ITEM_MODEL_RESPONSE, {"event": "ITEM_MODEL_RESPONSE", "subtype": "STANDARD"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.SignalEmit(self, emit_signal, "CM1->BL12")
                return