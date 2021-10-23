import colorama
from colorama import Back, Fore, Style
from datetime import datetime

colorama.init(autoreset=True)


class Logs:
    # LogMessage DebugMessage InfoMessage

    target_point_enable = False
    simple_info_enable = True
    deactivate_status_info_enable = True
    activate_status_info_enable = True
    signal_emit_enable = False
    signal_received_enable = False
    event_key_press_enable = False

    class AIControllerMessage:

        @staticmethod
        def ai_choice_info(self, card, characters):

            if Logs.deactivate_status_info_enable:
                time_stamp = datetime.now().time()
                message = print(f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} {self.__class__.__name__.upper()} choosen card: {card.card_name}, targets: {characters}')
                return message
            else:
                pass

    class ActionProcessMessage:

        @staticmethod
        def deactivate_status_info(tag, character, status, method_name):

            if Logs.deactivate_status_info_enable:
                time_stamp = datetime.now().time()
                message = print(f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} [{method_name}] {character.name}: {status.name} - {Fore.RED} {tag}{Fore.RESET}')
                return message
            else:
                pass

        @staticmethod
        def activate_status_info(character, status, method_name):

            if Logs.activate_status_info_enable:
                time_stamp = datetime.now().time()
                message = print(f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} [{method_name}] {character.name}: {status.name} - {Fore.RED}Aktywowano{Fore.RESET} (pozostałe duration: {status.duration})')
                return message
            else:
                pass

    class InfoMessage:

        @staticmethod
        def target_point(self, tag):

            if Logs.target_point_enable:
                time_stamp = datetime.now().time()
                message = print(f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} {self.__class__.__name__.upper()}:{Fore.RED}CALL_TARGET_POINT {Style.BRIGHT}"{tag}"')
                return message
            else:
                pass

        @staticmethod
        def simple_info(self, tag):

            if Logs.simple_info_enable:
                time_stamp = datetime.now().time()
                message = print(f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET}{Fore.RED} {tag}{Fore.RESET}')
                return message
            else:
                pass

    class DebugMessage:

        @staticmethod
        def signal_emit(self, signal, target=''):

            if Logs.signal_emit_enable:
                time_stamp = datetime.now().time()
                if target != '':
                    target = f' {Fore.YELLOW}"target": {target}{Fore.RESET}'
                message = print(f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} {self.__class__.__name__.upper()}:{Fore.YELLOW}EMIT: "event": {Style.BRIGHT}{signal.event}{Style.NORMAL}, "subtype": {Style.BRIGHT}{signal.subtype}{Style.NORMAL},{Fore.RESET} "type": {signal.type}{target}')
                return message
            else:
                pass

        @staticmethod
        def signal_received(self, signal, target=''):

            if Logs.signal_received_enable:
                time_stamp = datetime.now().time()
                if target != '':
                    target = f' "target": {Fore.CYAN}{target}{Fore.RESET}'
                message = print(f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} {self.__class__.__name__.upper()}:{Fore.CYAN}RECEIVED: "event": {Style.BRIGHT}{signal.event}{Style.NORMAL}, "subtype": {Style.BRIGHT}{signal.subtype}{Style.NORMAL},{Fore.RESET} "type": {signal.type}{target}')
                return message
            else:
                pass

        @staticmethod
        def event_key_press(self, event, text=''):

            if Logs.event_key_press_enable:
                time_stamp = datetime.now().time()
                if text != '':
                    text = f'{Fore.GREEN}{text}{Fore.GREEN}'
                message = print(f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} {self.__class__.__name__.upper()}:{Fore.CYAN}RECEIVED: "event": {Style.BRIGHT}{event.type}{Style.NORMAL},{Fore.RESET} {text}')
                return message
            else:
                pass

