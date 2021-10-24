import colorama
from colorama import Back, Fore, Style
from datetime import datetime

colorama.init(autoreset=True)


class Logs:
    # LogMessage DebugMessage InfoMessage

    card_controller_message = True
    draw_card_info_enable = True

    class CardControllerMessage:

        @staticmethod
        def draw_card_info(card, character):

            if Logs.draw_card_info_enable and Logs.card_controller_message:
                time_stamp = datetime.now().time()
                message = f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} {character.name} dobiera "{card.card_name}"'
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

