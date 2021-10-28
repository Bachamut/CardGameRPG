import pygame
from asserts.type_assert import TypeAssert
from property.initialize_property import InitializeProperty, InitializeState

from assets.lib.battle_system.action_utilities.action_process import ActionProcess
from assets.lib.battle_system.battle_character_utilities.battle_character_model import BattleCharacter
from assets.lib.battle_system.view_controllers.battle_character_view_manager import BattleCharacterViewManager
from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.battle_system.controllers.card_controller import CardController
from assets.lib.battle_system.log import Logs
from assets.lib.card_utilities.card_manager import CardManager
from assets.lib.card_utilities.card_model import BaseCard

from assets.lib.game_object_shared_resource import GameObjectSharedResource


class ActionController(GameObjectSharedResource):


    _initialized = False

    def __init__(self):
        super(ActionController, self).__init__()

    def _initialize(self):

        if InitializeProperty.check_is_ready(self, InitializeState.INITIALIZED):
            super(ActionController, self)._initialize()
            InitializeProperty.initialize_enable(self)
            Logs.InfoMessage.simple_info(self, "ActionController Initialized [ OK ]")

            return

        if InitializeProperty.check_is_ready(self, InitializeState.STARTED):
            InitializeProperty.started(self)
            self.property('SignalProperty').property_enable()
            Logs.InfoMessage.simple_info(self, "ActionController Started [ OK ]")

            return

    def on_script(self):
        pass

    def on_event(self, event):
        pass


    def on_signal(self, signal):

        # AC1
        if signal.type == BattleLogic.ACTION_CONTROLLER_SIGNAL and signal.subtype == "PRE_TURN":
            Logs.DebugMessage.signal_received(self, signal, "AC1<-BL2")

            ActionProcess.status_for_activation(self.current_character, signal.subtype)
            ActionProcess.status_for_deactivation(self.current_character, signal.subtype)

            ActionProcess.battle_state(self.battle_ally, self.battle_enemies)

            # Restocking current_character action_points
            ActionProcess.restock_action_points(self.current_character)

            emit_signal = pygame.event.Event(BattleLogic.ACTION_CONTROLLER_RESPONSE, {"event": "ACTION_CONTROLLER_RESPONSE", "subtype": "PRE_TURN"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.signal_emit(self, emit_signal, "AC1->BL3")
            return

        # AC2
        if signal.type == BattleLogic.ACTION_CONTROLLER_SIGNAL and signal.subtype == "PRE_DRAW":
            Logs.DebugMessage.signal_received(self, signal, "AC2<-BL4")

            ActionProcess.status_for_activation(self.current_character, signal.subtype)
            ActionProcess.status_for_deactivation(self.current_character, signal.subtype)

            ActionProcess.battle_state(self.battle_ally, self.battle_enemies)

            emit_signal = pygame.event.Event(BattleLogic.ACTION_CONTROLLER_RESPONSE, {"event": "ACTION_CONTROLLER_RESPONSE", "subtype": "PRE_DRAW"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.signal_emit(self, emit_signal, "AC2->BL5")
            return

        # AC3
        if signal.type == BattleLogic.ACTION_CONTROLLER_SIGNAL and signal.subtype == "POST_DRAW":
            Logs.DebugMessage.signal_received(self, signal, "AC3<-BL6")

            ActionProcess.status_for_activation(self.current_character, signal.subtype)
            ActionProcess.status_for_deactivation(self.current_character, signal.subtype)

            ActionProcess.battle_state(self.battle_ally, self.battle_enemies)

            emit_signal = pygame.event.Event(BattleLogic.ACTION_CONTROLLER_RESPONSE, {"event": "ACTION_CONTROLLER_RESPONSE", "subtype": "POST_DRAW"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.signal_emit(self, emit_signal, "AC3->BL3")
            return

        # AC4
        if signal.type == BattleLogic.ACTION_CONTROLLER_SIGNAL and signal.subtype == "STANDARD":
            Logs.DebugMessage.signal_received(self, signal, "AC4<-BL13")

            ActionController.action_controller_signal(self.current_character, self.confirmed_target, self.confirmed_card)

            self.confirmed_target.clear()
            self.confirmed_card = None

            emit_signal = pygame.event.Event(BattleLogic.ACTION_CONTROLLER_RESPONSE, {"event": "ACTION_CONTROLLER_RESPONSE", "subtype": "STANDARD"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.signal_emit(self, emit_signal, "AC4->BL14")
            return

        # AC5
        if signal.type == BattleLogic.ACTION_CONTROLLER_SIGNAL and signal.subtype == "POST_ACTION":
            Logs.DebugMessage.signal_received(self, signal, "AC5<-BL14")

            ActionProcess.status_for_activation(self.current_character, signal.subtype)
            ActionProcess.status_for_deactivation(self.current_character, signal.subtype)

            ActionProcess.battle_state(self.battle_ally, self.battle_enemies)

            emit_signal = pygame.event.Event(BattleLogic.ACTION_CONTROLLER_RESPONSE, {"event": "ACTION_CONTROLLER_RESPONSE", "subtype": "POST_ACTION"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.signal_emit(self, emit_signal, "AC5->BL8")
            return

        # ?AC100
        if signal.type == BattleLogic.ACTION_CONTROLLER_SIGNAL and signal.subtype == "POST_TURN":
            Logs.DebugMessage.signal_received(self, signal, "?AC100<-?BL100")

            ActionProcess.status_for_activation(self.current_character, signal.subtype)
            ActionProcess.status_for_deactivation(self.current_character, signal.subtype)

            ActionProcess.battle_state(self.battle_ally, self.battle_enemies)

            # Discarding current character hand at turn finish
            print(f'\n{self.current_character.name}:\n AP: {self.current_character.battle_attribute("action_points")}\n HP: {self.current_character.battle_attribute("health")}')
            CardController.discard_hand(self.current_character)
            print(f'Zdiscardowano hand {self.current_character.name}')
            print(f'ilość kart:\n hand: {len(self.current_character.hand)}\n draw_pile: {len(self.current_character.draw_pile)}\n discard_pile: {len(self.current_character.discard_pile)}')

            emit_signal = pygame.event.Event(BattleLogic.ACTION_CONTROLLER_RESPONSE, {"event": "ACTION_CONTROLLER_RESPONSE", "subtype": "POST_TURN"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.signal_emit(self, emit_signal, "?AC100->?BL101")
            return

    @staticmethod
    def action_controller_signal(caster, targets, card):

        TypeAssert.equal(caster, BattleCharacter)
        TypeAssert.islist_equal(targets, BattleCharacter)
        TypeAssert.equal(card, BaseCard)

        CardController.discard_used_card(caster, card)

        print(f'{caster.name}: AP:{caster.battle_attribute("action_points")}')

        for target in targets:

            target_action, caster_action = ActionProcess.action_process(caster, target, card)

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
