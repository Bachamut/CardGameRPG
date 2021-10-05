import pygame
from property.initialize_property import InitializeProperty, InitializeState

from assets.lib.battle_system.action_utilities.action_process import ActionProcess
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

        # AIC1
        if signal.type == BattleLogic.AI_CONTROLLER_SIGNAL and signal.subtype == "STANDARD":
            Logs.DebugMessage.SignalReceived(self, signal, "AIC1<-BL8")

            possible_targets = self.possible_targets()
            focus_factor = self.focus_factor()
            cards_values = self.cards_values()

            print(f'AI choosing action')

            # Setting target and card
            self.confirmed_target.append(possible_targets[0])
            self.confirmed_card = self.current_character.hand[0]

            emit_signal = pygame.event.Event(BattleLogic.AI_CONTROLLER_RESPONSE, {"event": "AI_CONTROLLER_RESPONSE", "subtype": "STANDARD"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "AIC1->BL13")
            return

    def possible_targets(self):

        targets = list()

        if self.current_character.affiliation == "enemy":
            targets = self.battle_ally
        elif self.current_character.affiliation == "ally":
            targets = self.battle_enemies
        return targets

    def focus_factor(self):

        focus_factor = dict()
        targets = self.possible_targets()
        for target in targets:

            health_percentage = (target.battle_attributes.health / target.battle_attributes.health)

            health_factor = health_percentage * (100 - target.battle_attributes.physical_resist) / 100
            focus_factor[target.name] = health_factor

        return focus_factor

    def card_dmg_value(self, card):

        value_by_targets = dict()
        targets = self.possible_targets()
        for target in targets:

            value = ActionProcess.value_calculation(self.current_character, target, card)
            # Check if ap_cost is not 0
            value_by_targets[target] = value

        return value_by_targets

    def cards_values(self):

        cards_values = dict()
        for card in self.current_character.hand:

            card_value = self.card_dmg_value(card)

            cards_values[card] = card_value

        return cards_values

    def card_target_status_values(self, card):

        card_target_status_values = list()
        status_matrix = list()
        for status_type, parameters in card.target_status.items():

            if status_type == "bleed_1":
                status_value = parameters['value'] * parameters['duration'] * 2
                status_matrix = [status_value, 0, 0]
            if status_type == "poison_1":
                status_value = parameters['value'] * parameters['duration'] * 3
                status_matrix = [status_value, 0, 0]
            if status_type == "stun_1":
                status_value = parameters['value'] * parameters['duration'] * 5
                status_matrix = [0, 0, status_value]
            if status_type == "harden_1":
                status_value = parameters['value'] * parameters['duration'] / 5
                status_matrix = [0, 0, status_value]
            if status_type == "regeneration_1":
                status_value = parameters['value'] * parameters['duration'] * 2
                status_matrix = [0, status_value, 0]

            card_target_status_values.append(status_matrix)

        return card_target_status_values

    def card_caster_status_values(self, card):

        card_caster_status_values = list()
        status_matrix = list()

        for status_type, parameters in card.caster_status.items():

            if status_type == "bleed_1":
                status_value = parameters['value'] * parameters['duration'] * 2
                status_matrix = [status_value, 0, 0]
            if status_type == "poison_1":
                status_value = parameters['value'] * parameters['duration'] * 3
                status_matrix = [status_value, 0, 0]
            if status_type == "stun_1":
                status_value = parameters['value'] * parameters['duration'] * 5
                status_matrix = [0, 0, status_value]
            if status_type == "harden_1":
                status_value = parameters['value'] * parameters['duration'] / 5
                status_matrix = [0, 0, status_value]
            if status_type == "regeneration_1":
                status_value = parameters['value'] * parameters['duration'] * 2
                status_matrix = [0, status_value, 0]

            card_caster_status_values.append(status_matrix)

        return card_caster_status_values

    def card_target_own_value(self, card):

        card_target_own_value = list()


    def values_by_targets(self, card):

        values_by_targets = dict()
        for target in self.battle_ally + self.battle_enemies:

            card_matrix = list()
            value = ActionProcess.value_calculation(self.current_character, target, card)
            if card.sort == "dmg":
                card_matrix = [value, 0 , 0]
            if card.sort == "heal":
                card_matrix = [0, value, 0]

            values_by_targets[target] = card_matrix

        return values_by_targets






