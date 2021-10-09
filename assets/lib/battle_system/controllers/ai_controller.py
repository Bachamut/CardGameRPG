import operator

import pygame
from property.initialize_property import InitializeProperty, InitializeState

from assets.lib.battle_system.action_utilities.action_process import ActionProcess
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
            Logs.InfoMessage.SimpleInfo(self, "AIController Initialized [ OK ]")

            return

        if InitializeProperty.check_is_ready(self, InitializeState.STARTED):
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

            best_card, best_character = self.action_calculation()

            self.confirmed_card = best_card
            self.confirmed_target.append(best_character)

            print(f'\nAI choosing action')

            emit_signal = pygame.event.Event(BattleLogic.AI_CONTROLLER_RESPONSE, {"event": "AI_CONTROLLER_RESPONSE", "subtype": "STANDARD"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "AIC1->BL13")
            return

    def action_calculation(self):

        cards_values = self.calculating_cards_values()

        best_card = None
        best_character = None
        best_value = None

        for card, collection in cards_values.items():

            temp_character = max(collection, key=collection.get)
            temp_value = collection[temp_character]

            if best_value is None or temp_value > best_value:
                best_card = card
                best_character = temp_character
                best_value = temp_value

        return best_card, best_character

    def calculating_cards_values(self):

        targets = self.battle_ally + self.battle_enemies
        cards_values = dict()

        preference_matrix = [1, 1, 1]

        for card in self.current_character.hand:

            battle_card = CardManager.create_battle_card(card)
            value_by_targets = self.card_value_by_affiliation(targets, battle_card)

            for target, value_matrix in value_by_targets.items():

                for index, value in enumerate(preference_matrix):
                    value_matrix[index] *= value

                value_by_targets[target] = sum(value_matrix)

            cards_values[card] = value_by_targets

        return cards_values

    def card_value_by_affiliation(self, targets, card):

        value_by_targets = dict()

        for target in targets:

            affiliation_matrix = self.affiliation_matrix(target)
            caster_matrix = self.caster_matrix()

            card_matrix = self.card_value_matrix(card, target)
            target_status_matrix = self.target_status_value_calculation(target, card)
            caster_status_matrix = self.caster_status_value_calculation(target, card)

            for index, value in enumerate(affiliation_matrix):

                card_matrix[index] *= value
                target_status_matrix[index] *= value

            for index, value in enumerate(caster_matrix):

                caster_status_matrix[index] *= value

            zipped_lists = zip(card_matrix, target_status_matrix, caster_status_matrix)
            target_sum = [x + y + z for (x, y, z) in zipped_lists]

            value_by_targets[target] = target_sum

        return value_by_targets

    def affiliation_matrix(self, target):

        if self.current_character.affiliation == "enemy" and target.affiliation == "enemy" or \
                self.current_character.affiliation == "ally" and target.affiliation == "ally":

            affiliation_matrix = [-1, 1, 1]

        elif self.current_character.affiliation == "enemy" and target.affiliation == "ally" or \
                self.current_character.affiliation == "ally" and target.affiliation == "enemy":

            affiliation_matrix = [1, -1, -1]

        return affiliation_matrix

    def caster_matrix(self):

        caster_matrix = [-1, 1, 1]
        return caster_matrix

    def card_value_matrix(self, card, target):

        value = ActionProcess.value_calculation(self.current_character, target, card)
        if card.card_type == "physical_attack":
            card_matrix = [value, 0, 0]
        if card.card_type == "heal":
            card_matrix = [0, value, 0]
        if card.card_type == "buff":
            card_matrix = [0, 0, value]

        return card_matrix

    def target_status_value_calculation(self, target, card):

        return self._status_value_calculation(target, card.target_status.items())

    def caster_status_value_calculation(self, target, card):

        return self._status_value_calculation(target, card.caster_status.items())

    def _status_value_calculation(self, target, card_status):

        status_matrix = list()
        sum_value = [0, 0, 0]
        for status_type, parameters in card_status:

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

            zipped_lists = zip(sum_value, status_matrix)
            sum_value = [x + y for (x, y) in zipped_lists]

        return sum_value

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
