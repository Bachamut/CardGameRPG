import pygame
from property.initialize_property import InitializeProperty, InitializeState

from assets.lib.battle_system.action_types import ActionType
from assets.lib.battle_system.battle_character_view_manager import BattleCharacterViewManager
from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.battle_system.card_model import CardModel
from assets.lib.battle_system.log import Logs
from assets.lib.card_utilities.card_manager import CardManager

from assets.lib.game_object_shared_resource import GameObjectSharedResource


class ActionModel(GameObjectSharedResource):


    _initialized = False
    # active = BattleLogic.turn_model_active

    def __init__(self):
        super(ActionModel, self).__init__()

    def _initialize(self):

        if InitializeProperty.check_status(self, InitializeState.INITIALIZED):
            super(ActionModel, self)._initialize()
            InitializeProperty.initialize_enable(self)
            Logs.InfoMessage.SimpleInfo(self, "ActionModel Initialized [ OK ]")

            return

        if InitializeProperty.check_status(self, InitializeState.STARTED):
            InitializeProperty.started(self)
            self.property('SignalProperty').property_enable()
            Logs.InfoMessage.SimpleInfo(self, "ActionModel Started [ OK ]")

            return

    def on_script(self):
        pass

    def on_event(self, event):
        pass


    def on_signal(self, signal):

        # AM1
        if signal.type == BattleLogic.ACTION_MODEL_SIGNAL and signal.subtype == "PRE_TURN":
            Logs.DebugMessage.SignalReceived(self, signal, "AM1<-BL2")

            ActionType.status_for_activation(self.current_character, signal.subtype)
            ActionType.status_for_deactivation(self.current_character, signal.subtype)

            emit_signal = pygame.event.Event(BattleLogic.ACTION_MODEL_RESPONSE, {"event": "ACTION_MODEL_RESPONSE", "subtype": "PRE_TURN"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "AM1->BL3")
            return

        # AM2
        if signal.type == BattleLogic.ACTION_MODEL_SIGNAL and signal.subtype == "PRE_DRAW":
            Logs.DebugMessage.SignalReceived(self, signal, "AM2<-BL4")

            ActionType.status_for_activation(self.current_character, signal.subtype)
            ActionType.status_for_deactivation(self.current_character, signal.subtype)

            emit_signal = pygame.event.Event(BattleLogic.ACTION_MODEL_RESPONSE, {"event": "ACTION_MODEL_RESPONSE", "subtype": "PRE_DRAW"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "AM2->BL5")
            return

        # AM3
        if signal.type == BattleLogic.ACTION_MODEL_SIGNAL and signal.subtype == "POST_DRAW":
            Logs.DebugMessage.SignalReceived(self, signal, "AM3<-BL6")

            ActionType.status_for_activation(self.current_character, signal.subtype)
            ActionType.status_for_deactivation(self.current_character, signal.subtype)

            emit_signal = pygame.event.Event(BattleLogic.ACTION_MODEL_RESPONSE, {"event": "ACTION_MODEL_RESPONSE", "subtype": "POST_DRAW"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "AM3->BL3")
            return

        # AM4
        if signal.type == BattleLogic.ACTION_MODEL_SIGNAL and signal.subtype == "STANDARD":
            Logs.DebugMessage.SignalReceived(self, signal, "AM4<-BL13")

            ActionModel.action_model_signal(self.current_character, self.confirmed_target, CardManager.create_battle_card(self.confirmed_card))

            emit_signal = pygame.event.Event(BattleLogic.ACTION_MODEL_RESPONSE, {"event": "ACTION_MODEL_RESPONSE", "subtype": "STANDARD"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "AM4->BL14")
            return

        # AM5
        if signal.type == BattleLogic.ACTION_MODEL_SIGNAL and signal.subtype == "POST_ACTION":
            Logs.DebugMessage.SignalReceived(self, signal, "AM5<-BL14")

            ActionType.status_for_activation(self.current_character, signal.subtype)
            ActionType.status_for_deactivation(self.current_character, signal.subtype)

            emit_signal = pygame.event.Event(BattleLogic.ACTION_MODEL_RESPONSE, {"event": "ACTION_MODEL_RESPONSE", "subtype": "POST_ACTION"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "AM5->BL8")
            return

        # ?AM100
        if signal.type == BattleLogic.ACTION_MODEL_SIGNAL and signal.subtype == "POST_TURN":
            Logs.DebugMessage.SignalReceived(self, signal, "?AM100<-?BL100")

            ActionType.status_for_activation(self.current_character, signal.subtype)
            ActionType.status_for_deactivation(self.current_character, signal.subtype)

            # Discarding current character hand at turn finish
            print(f'\n{self.current_character.name}:\n AP: {self.current_character.battle_attribute("action_points")}\n HP: {self.current_character.battle_attribute("health")}')
            CardModel.discard_hand(self.current_character)
            print(f'Zdiscardowano hand {self.current_character.name}')
            print(f'ilość kart:\n hand: {len(self.current_character.hand)}\n draw_pile: {len(self.current_character.draw_pile)}\n discard_pile: {len(self.current_character.discard_pile)}')

            emit_signal = pygame.event.Event(BattleLogic.ACTION_MODEL_RESPONSE, {"event": "ACTION_MODEL_RESPONSE", "subtype": "POST_TURN"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "?AM100->?BL101")
            return

    @staticmethod
    def action_model_signal(caster, targets, card):

        caster.modify_battle_modifiers("action_points", -card.ap_cost)
        # caster.base_attributes.action_points -= card.ap_cost
        print(f'{caster.name}: AP:{caster.battle_attribute("action_points")}')

        for target in targets:

            target_action, caster_action = ActionType.action_process(caster, target, card)

            target_signal = pygame.event.Event(BattleLogic.CHARACTER_VIEW_SIGNAL,
                                               {"event": "CHARACTER_VIEW_SIGNAL",
                                                "subtype": "TARGET",
                                                "receiver": target,
                                                "second_character": caster,
                                                "actions": target_action
                                                })
            pygame.event.post(target_signal)

        caster_signal = pygame.event.Event(BattleLogic.CHARACTER_VIEW_SIGNAL,
                                           {"event": "CHARACTER_VIEW_SIGNAL",
                                            "subtype": "CASTER",
                                            "receiver": caster,
                                            "second_character": target,
                                            "actions": caster_action
                                            })
        pygame.event.post(caster_signal)

        list = BattleCharacterViewManager.battle_character_view_list
        print(f'')
