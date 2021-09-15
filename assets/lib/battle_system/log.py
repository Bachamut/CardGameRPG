import colorama
from colorama import Back, Fore, Style
from datetime import datetime

colorama.init(autoreset=True)

class Logs:
    # LogMessage DebugMessage InfoMessage

    target_point_enable = False
    simple_info_enable = False
    signal_emit_enable = False
    signal_received_enable = False
    event_key_press_enable = True

    class InfoMessage:

        @staticmethod
        def TargetPoint(self, tag):

            if Logs.target_point_enable:
                time_stamp = datetime.now().time()
                message = print(f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} {self.__class__.__name__.upper()}:{Fore.RED}CALL_TARGET_POINT {Style.BRIGHT}"{tag}"')
                return message
            else:
                pass

        @staticmethod
        def SimpleInfo(self, tag):

            if Logs.simple_info_enable:
                time_stamp = datetime.now().time()
                message = print(f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET}{Fore.RED} {tag}{Fore.RESET}')
                return message
            else:
                pass

    class DebugMessage:

        @staticmethod
        def SignalEmit(self, signal, target=''):

            if Logs.signal_emit_enable:
                time_stamp = datetime.now().time()
                if target != '':
                    target = f' {Fore.YELLOW}"target": {target}{Fore.RESET}'
                message = print(f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} {self.__class__.__name__.upper()}:{Fore.YELLOW}EMIT: "event": {Style.BRIGHT}{signal.event}{Style.NORMAL}, "subtype": {Style.BRIGHT}{signal.subtype}{Style.NORMAL},{Fore.RESET} "type": {signal.type}{target}')
                return message
            else:
                pass

        @staticmethod
        def SignalReceived(self, signal, target=''):

            if Logs.signal_received_enable:
                time_stamp = datetime.now().time()
                if target != '':
                    target = f' "target": {Fore.CYAN}{target}{Fore.RESET}'
                message = print(f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} {self.__class__.__name__.upper()}:{Fore.CYAN}RECEIVED: "event": {Style.BRIGHT}{signal.event}{Style.NORMAL}, "subtype": {Style.BRIGHT}{signal.subtype}{Style.NORMAL},{Fore.RESET} "type": {signal.type}{target}')
                return message
            else:
                pass

        @staticmethod
        def EventKeyPress(self, event, text=''):

            if Logs.event_key_press_enable:
                time_stamp = datetime.now().time()
                if text != '':
                    text = f'{Fore.GREEN}{text}{Fore.GREEN}'
                message = print(f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} {self.__class__.__name__.upper()}:{Fore.CYAN}RECEIVED: "event": {Style.BRIGHT}{event.type}{Style.NORMAL},{Fore.RESET} {text}')
                return message
            else:
                pass

