import pygame

from assets.lib.battle_system.action_types import ActionType
from assets.lib.battle_system.battle_character import BattleCharacter
from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.battle_system.card_model import CardModel
from assets.lib.battle_system.character_model import CharacterModel
from assets.lib.battle_system.log import Logs
from assets.lib.battle_system.status import Status
from assets.lib.card_utilities.card import Card
from assets.lib.game_logic import GameLogic
from game_object.game_object import GameObject

from assets.lib.game_object_battle_shared import GameObjectBattleShared


class TurnModel(GameObjectBattleShared):


    _initialized = False
    # active = BattleLogic.turn_model_active

    def __init__(self):
        super(TurnModel, self).__init__()

    def _initialize(self):
        super(TurnModel, self)._initialize()
        TurnModel._initialized = True
        print("TurnModel initialized")

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

        # AM1
        if signal.type == BattleLogic.ACTION_MODEL_SIGNAL and signal.subtype == "PRE_TURN":
            Logs.DebugMessage.SignalReceived(self, signal, "AM1<-BL2")

            emit_signal = pygame.event.Event(BattleLogic.ACTION_MODEL_RESPONSE, {"event": "ACTION_MODEL_RESPONSE", "subtype": "PRE_TURN"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "AM1->BL3")
            return

        # AM2
        if signal.type == BattleLogic.ACTION_MODEL_SIGNAL and signal.subtype == "PRE_DRAW":
            Logs.DebugMessage.SignalReceived(self, signal, "AM2<-BL4")

            emit_signal = pygame.event.Event(BattleLogic.ACTION_MODEL_RESPONSE, {"event": "ACTION_MODEL_RESPONSE", "subtype": "PRE_DRAW"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "AM2->BL5")
            return

        # AM3
        if signal.type == BattleLogic.ACTION_MODEL_SIGNAL and signal.subtype == "POST_DRAW":
            Logs.DebugMessage.SignalReceived(self, signal, "AM3<-BL6")

            emit_signal = pygame.event.Event(BattleLogic.ACTION_MODEL_RESPONSE, {"event": "ACTION_MODEL_RESPONSE", "subtype": "POST_DRAW"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "AM3->BL3")
            return

        # AM4
        if signal.type == BattleLogic.ACTION_MODEL_SIGNAL and signal.subtype == "STANDARD":
            Logs.DebugMessage.SignalReceived(self, signal, "AM4<-BL13")


            self.current_character = self.battle_ally[0]

            self.current_target = list()
            target = self.battle_ally[1]
            self.current_target.append(target)

            # self.current_card =

            TurnModel.action_model_signal(self.current_character, self.current_target, self.current_card)

            emit_signal = pygame.event.Event(BattleLogic.ACTION_MODEL_RESPONSE, {"event": "ACTION_MODEL_RESPONSE", "subtype": "STANDARD"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "AM4->BL14")
            return

    # AM5
        if signal.type == BattleLogic.ACTION_MODEL_SIGNAL and signal.subtype == "POST_ACTION":
            Logs.DebugMessage.SignalReceived(self, signal, "AM5<-BL14")

            emit_signal = pygame.event.Event(BattleLogic.ACTION_MODEL_RESPONSE, {"event": "ACTION_MODEL_RESPONSE", "subtype": "POST_ACTION"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "AM5->BL8")
            return

        # ?AM100
        if signal.type == BattleLogic.ACTION_MODEL_SIGNAL and signal.subtype == "POST_TURN":
            Logs.DebugMessage.SignalReceived(self, signal, "?AM100<-?BL100")

            emit_signal = pygame.event.Event(BattleLogic.ACTION_MODEL_RESPONSE, {"event": "ACTION_MODEL_RESPONSE", "subtype": "POST_TURN"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "?AM100->?BL101")
            return

    def current_action(self):
        if self.current_card.ap_cost <= self.current_character.action_points:
            print(f'Możesz użyć karty')

            TurnModel.action_process(self.current_character, self.current_target, self.current_card)

        if self.current_card.ap_cost > self.current_character.action_points:
            print(f'Nie masz wystarczającej ilości AP')

    @staticmethod
    def action_model_signal(caster, targets, card):

        target_status = None
        target_dmg = None
        caster_status = None
        caster_dmg = None

        for target in targets:
            target_status, target_dmg, \
            caster_status, caster_dmg \
                = TurnModel.action_process(caster, target, card)

            # target_signal: TARGET_SIGNAL(target, caster, card, target_status, target_dmg)
            # caster_signal: CASTER_SIGNAL(caster, target, card, caster_status, caster_dmg)

            target_signal = pygame.event.Event(BattleCharacter.BATTLE_CHARACTER,
                                               {"event": "BATTLE_CHARACTER",
                                                "subtype": "TARGET_SIGNAL",
                                                "target": target,
                                                "caster": caster,
                                                "card": card,
                                                "target_status": target_status,
                                                "target_dmg": target_dmg,
                                                })
            pygame.event.post(target_signal)

        caster_signal = pygame.event.Event(BattleCharacter.BATTLE_CHARACTER,
                                           {"event": "BATTLE_CHARACTER",
                                            "subtype": "CASTER_SIGNAL",
                                            "caster": caster,
                                            "target": targets,
                                            "card": card,
                                            "caster_status": caster_status,
                                            "caster_dmg": caster_dmg,
                                            })
        pygame.event.post(caster_signal)

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


