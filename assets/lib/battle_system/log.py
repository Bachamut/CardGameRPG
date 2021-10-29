import colorama
from colorama import Back, Fore, Style
from datetime import datetime

colorama.init(autoreset=True)


class Logs:
    # LogMessage DebugMessage InfoMessage

    card_controller_message = True
    draw_card_info_enable = True
    discard_hand_info_enable = True
    arrow_card_select_info_enable = True
    card_selection_info_enable = True
    card_controller_simple_info_enable = True

    class CardControllerMessage:

        @staticmethod
        def draw_card_info(card, character):

            if Logs.draw_card_info_enable and Logs.card_controller_message:
                time_stamp = datetime.now().time()
                message = f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} {character.name} dobiera "{card.card_name}"'
                return print(message)
            else:
                pass

        @staticmethod
        def discard_hand_info(character):

            if Logs.discard_hand_info_enable and Logs.card_controller_message:
                time_stamp = datetime.now().time()
                message = f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} {character.name}: zdiscardowano hand\nilość kart:\n hand: {len(character.hand)}\n draw_pile: {len(character.draw_pile)}\n discard_pile: {len(character.discard_pile)}'
                return print(message)
            else:
                pass

        @staticmethod
        def arrow_card_select_info(self):

            if Logs.arrow_card_select_info_enable and Logs.card_controller_message:
                time_stamp = datetime.now().time()
                message = f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} {self.selected_card_index}: {self.current_character.hand[self.selected_card_index].card_name}'
                return print(message)
            else:
                pass

        @staticmethod
        def card_selection_info(self):

            if Logs.card_selection_info_enable and Logs.card_controller_message:
                time_stamp = datetime.now().time()
                message = f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} wybrana karta: {self.selected_card_index}: {self._battle_logic.confirmed_card.card_name}'
                return print(message)
            else:
                pass

        @staticmethod
        def card_controller_simple_info(self, tag):

            if Logs.card_controller_simple_info_enable and Logs.card_controller_message:
                time_stamp = datetime.now().time()
                message = f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} {tag}'
                return print(message)
            else:
                pass

    ai_controller_message = True
    ai_choice_info_enable = True

    class AIControllerMessage:

        @staticmethod
        def ai_choice_info(self, card, characters):

            if Logs.ai_choice_info_enable and Logs.ai_controller_message:
                time_stamp = datetime.now().time()
                targets = ', '.join(str(x.name) for x in characters)
                message = f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} {self.__class__.__name__.upper()}: {self.current_character.name} wybrał {card.card_name}, targets: {targets}'
                return print(message)
            else:
                pass

    action_process_message = True
    activate_status_info_enable = True
    deactivate_status_info_enable = True
    action_process_info_enable = True
    action_process_simple_info_enable = True

    class ActionProcessMessage:

        @staticmethod
        def activate_status_info(character, status, method_name):

            if Logs.activate_status_info_enable and Logs.action_process_message:
                time_stamp = datetime.now().time()
                message = f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} [{method_name}] {character.name}: {status.name} - {Fore.RED}Aktywowano{Fore.RESET} (pozostałe duration: {status.duration})'
                return print(message)
            else:
                pass

        @staticmethod
        def deactivate_status_info(tag, character, status, method_name):

            if Logs.deactivate_status_info_enable and Logs.action_process_message:
                time_stamp = datetime.now().time()
                message = f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} [{method_name}] {character.name}: {status.name} - {Fore.RED} {tag}{Fore.RESET}'
                return print(message)
            else:
                pass

        @staticmethod
        def action_process_info(caster, target, card, value, method_name):

            if Logs.action_process_info_enable and Logs.action_process_message:
                time_stamp = datetime.now().time()
                message = f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} [{method_name}] {caster.name}: używa "{card.card_name}" na {target.name}, zadaje {value} obrażeń!'
                return print(message)
            else:
                pass

        @staticmethod
        def action_process_simple_info(method_name, tag):

            if Logs.action_process_simple_info_enable and Logs.action_process_message:
                time_stamp = datetime.now().time()
                message = f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} [{method_name}] {tag})'
                return print(message)
            else:
                pass

    character_model_message = True
    add_status_info_enable = True
    remove_status_info_enable = True
    modify_battle_attributes_info_enable = True

    class CharacterModelMessage:

        @staticmethod
        def add_status_info(self, status, method_name):

            if Logs.add_status_info_enable and Logs.character_model_message:
                time_stamp = datetime.now().time()
                message = f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} [{method_name}] {self.name}: otrzymano status "{status.name}"'
                return print(message)
            else:
                pass

        @staticmethod
        def remove_status_info(self, status, method_name):

            if Logs.remove_status_info_enable and Logs.character_model_message:
                time_stamp = datetime.now().time()
                message = f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} [{method_name}] {self.name}: usunięto status "{status.name}"'
                return print(message)
            else:
                pass

        @staticmethod
        def modify_battle_attributes_info(self, attribute, value, method_name):

            if Logs.modify_battle_attributes_info_enable and Logs.character_model_message:
                time_stamp = datetime.now().time()
                message = f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} [{method_name}] {self.name}: battle_attributes.{attribute}:{getattr(self.battle_attributes, attribute)}'
                return print(message)
            else:
                pass

    info_message = True
    target_point_enable = False
    simple_info_enable = True

    class InfoMessage:

        @staticmethod
        def target_point(self, tag):

            if Logs.target_point_enable and Logs.info_message:
                time_stamp = datetime.now().time()
                message = f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} {self.__class__.__name__.upper()}:{Fore.RED}CALL_TARGET_POINT {Style.BRIGHT}"{tag}"'
                return print(message)
            else:
                pass

        @staticmethod
        def simple_info(self, tag):

            if Logs.simple_info_enable and Logs.info_message:
                time_stamp = datetime.now().time()
                message = f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET}{Fore.RED} {tag}{Fore.RESET}'
                return print(message)
            else:
                pass

    debug_message = True
    signal_emit_enable = False
    signal_received_enable = False
    event_key_press_enable = False

    class DebugMessage:

        @staticmethod
        def signal_emit(self, signal, target=''):

            if Logs.signal_emit_enable and Logs.debug_message:
                time_stamp = datetime.now().time()
                if target != '':
                    target = f' {Fore.YELLOW}"target": {target}{Fore.RESET}'
                message = f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} {self.__class__.__name__.upper()}:{Fore.YELLOW}EMIT: "event": {Style.BRIGHT}{signal.event}{Style.NORMAL}, "subtype": {Style.BRIGHT}{signal.subtype}{Style.NORMAL},{Fore.RESET} "type": {signal.type}{target}'
                return print(message)
            else:
                pass

        @staticmethod
        def signal_received(self, signal, target=''):

            if Logs.signal_received_enable:
                time_stamp = datetime.now().time()
                if target != '':
                    target = f' "target": {Fore.CYAN}{target}{Fore.RESET}'
                message = f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} {self.__class__.__name__.upper()}:{Fore.CYAN}RECEIVED: "event": {Style.BRIGHT}{signal.event}{Style.NORMAL}, "subtype": {Style.BRIGHT}{signal.subtype}{Style.NORMAL},{Fore.RESET} "type": {signal.type}{target}'
                return print(message)
            else:
                pass

        @staticmethod
        def event_key_press(self, event, text=''):

            if Logs.event_key_press_enable:
                time_stamp = datetime.now().time()
                if text != '':
                    text = f'{Fore.GREEN}{text}{Fore.GREEN}'
                message = f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} {self.__class__.__name__.upper()}:{Fore.CYAN}RECEIVED: "event": {Style.BRIGHT}{event.type}{Style.NORMAL},{Fore.RESET} {text}'
                return print(message)
            else:
                pass

