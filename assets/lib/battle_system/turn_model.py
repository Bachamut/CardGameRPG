import pygame
from property.initialize_property import InitializeProperty, InitializeState

from assets.lib.battle_system.action_types import ActionType
from assets.lib.battle_system.battle_character import BattleCharacter
from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.battle_system.card_model import CardModel
from assets.lib.battle_system.character_model import CharacterModel
from assets.lib.battle_system.log import Logs
from assets.lib.battle_system.status import Status
from assets.lib.card_utilities.card import BaseCard, BattleCard
from assets.lib.card_utilities.card_manager import CardManager
from assets.lib.game_logic import GameLogic
from game_object.game_object import GameObject

from assets.lib.game_object_shared_resource import GameObjectSharedResource


class TurnModel(GameObjectSharedResource):


    _initialized = False
    # active = BattleLogic.turn_model_active

    def __init__(self):
        super(TurnModel, self).__init__()

    def _initialize(self):

        if InitializeProperty.check_status(self, InitializeState.INITIALIZED):
            super(TurnModel, self)._initialize()
            InitializeProperty.initialize_enable(self)
            Logs.InfoMessage.SimpleInfo(self, "TurnModel Initialized [ OK ]")

            return

        if InitializeProperty.check_status(self, InitializeState.STARTED):
            InitializeProperty.started(self)
            self.property('SignalProperty').property_enable()
            Logs.InfoMessage.SimpleInfo(self, "TurnModel Started [ OK ]")

            return

    def on_script(self):
        pass

    def on_event(self, event):
        pass


    def on_signal(self, signal):

        # AM1
        if signal.type == BattleLogic.ACTION_MODEL_SIGNAL and signal.subtype == "PRE_TURN":
            Logs.DebugMessage.SignalReceived(self, signal, "AM1<-BL2")

            status_list = ActionType.get_status_activation(signal.subtype)
            status_matched = ActionType.get_status_matched(self.current_character, status_list)
            ActionType.status_activation(self.current_character, status_matched)
            ActionType.status_expire(self.current_character, status_matched)

            emit_signal = pygame.event.Event(BattleLogic.ACTION_MODEL_RESPONSE, {"event": "ACTION_MODEL_RESPONSE", "subtype": "PRE_TURN"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "AM1->BL3")
            return

        # AM2
        if signal.type == BattleLogic.ACTION_MODEL_SIGNAL and signal.subtype == "PRE_DRAW":
            Logs.DebugMessage.SignalReceived(self, signal, "AM2<-BL4")

            status_list = ActionType.get_status_activation(signal.subtype)
            status_matched = ActionType.get_status_matched(self.current_character, status_list)
            ActionType.status_activation(self.current_character, status_matched)
            ActionType.status_expire(self.current_character, status_matched)

            emit_signal = pygame.event.Event(BattleLogic.ACTION_MODEL_RESPONSE, {"event": "ACTION_MODEL_RESPONSE", "subtype": "PRE_DRAW"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "AM2->BL5")
            return

        # AM3
        if signal.type == BattleLogic.ACTION_MODEL_SIGNAL and signal.subtype == "POST_DRAW":
            Logs.DebugMessage.SignalReceived(self, signal, "AM3<-BL6")

            status_list = ActionType.get_status_activation(signal.subtype)
            status_matched = ActionType.get_status_matched(self.current_character, status_list)
            ActionType.status_activation(self.current_character, status_matched)
            ActionType.status_expire(self.current_character, status_matched)

            emit_signal = pygame.event.Event(BattleLogic.ACTION_MODEL_RESPONSE, {"event": "ACTION_MODEL_RESPONSE", "subtype": "POST_DRAW"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "AM3->BL3")
            return

        # AM4
        if signal.type == BattleLogic.ACTION_MODEL_SIGNAL and signal.subtype == "STANDARD":
            Logs.DebugMessage.SignalReceived(self, signal, "AM4<-BL13")

            TurnModel.action_model_signal(self.current_character, self.confirmed_target, CardManager.create_battle_card(self.confirmed_card))

            emit_signal = pygame.event.Event(BattleLogic.ACTION_MODEL_RESPONSE, {"event": "ACTION_MODEL_RESPONSE", "subtype": "STANDARD"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "AM4->BL14")
            return

        # AM5
        if signal.type == BattleLogic.ACTION_MODEL_SIGNAL and signal.subtype == "POST_ACTION":
            Logs.DebugMessage.SignalReceived(self, signal, "AM5<-BL14")

            status_list = ActionType.get_status_activation(signal.subtype)
            status_matched = ActionType.get_status_matched(self.current_character, status_list)
            ActionType.status_activation(self.current_character, status_matched)
            ActionType.status_expire(self.current_character, status_matched)

            emit_signal = pygame.event.Event(BattleLogic.ACTION_MODEL_RESPONSE, {"event": "ACTION_MODEL_RESPONSE", "subtype": "POST_ACTION"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "AM5->BL8")
            return

        # ?AM100
        if signal.type == BattleLogic.ACTION_MODEL_SIGNAL and signal.subtype == "POST_TURN":
            Logs.DebugMessage.SignalReceived(self, signal, "?AM100<-?BL100")

            status_types = ActionType.get_status_activation(signal.subtype)
            status_matched = ActionType.get_status_matched(self.current_character, status_types)
            ActionType.status_activation(self.current_character, status_matched)
            ActionType.status_expire(self.current_character, status_matched)

            # Discarding current character hand at turn finish
            CardModel.discard_hand(self.current_character)
            print(f'Zdiscardowano hand {self.current_character.name}')
            print(f'ilość kart:\n hand: {len(self.current_character.hand)}\n draw_pile: {len(self.current_character.draw_pile)}\n discard_pile: {len(self.current_character.discard_pile)}')

            emit_signal = pygame.event.Event(BattleLogic.ACTION_MODEL_RESPONSE, {"event": "ACTION_MODEL_RESPONSE", "subtype": "POST_TURN"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "?AM100->?BL101")
            return

    @staticmethod
    def action_model_signal(caster, targets, card):

        target_status = None
        target_dmg = None
        caster_status = None
        caster_dmg = None

        # Temp solution
        caster.base_attributes.action_points -= card.ap_cost
        print(f'{caster.name}: \nAP:{caster.base_attributes.action_points}')

        for target in targets:
            ActionType.action_process(caster, target, card)
            print(f'{caster.name}: \nAP:{caster.base_attributes.action_points}')
            print(f'{target.name}: \nhp:{target.base_attributes.health}')
        # End temp

        # for target in targets:
        #     target_status, target_dmg, \
        #     caster_status, caster_dmg \
        #         = ActionType.action_process(caster, target, card)
        #
        #     # Pseudo code
        #     # target_signal: TARGET_SIGNAL(target, caster, card, target_status, target_dmg)
        #     # caster_signal: CASTER_SIGNAL(caster, target, card, caster_status, caster_dmg)
        #
        #     target_signal = pygame.event.Event(BattleCharacter.BATTLE_CHARACTER,
        #                                        {"event": "BATTLE_CHARACTER",
        #                                         "subtype": "TARGET_SIGNAL",
        #                                         "target": target,
        #                                         "caster": caster,
        #                                         "card": card,
        #                                         "target_status": target_status,
        #                                         "target_dmg": target_dmg,
        #                                         })
        #     pygame.event.post(target_signal)
        #
        # caster_signal = pygame.event.Event(BattleCharacter.BATTLE_CHARACTER,
        #                                    {"event": "BATTLE_CHARACTER",
        #                                     "subtype": "CASTER_SIGNAL",
        #                                     "caster": caster,
        #                                     "target": targets,
        #                                     "card": card,
        #                                     "caster_status": caster_status,
        #                                     "caster_dmg": caster_dmg,
        #                                     })
        # pygame.event.post(caster_signal)



