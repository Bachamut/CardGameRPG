import colorama
from colorama import Back, Fore, Style
from datetime import datetime

colorama.init(autoreset=True)

class Logs:
    # LogMessage DebugMessage InfoMessage

    class InfoMessage:

        @staticmethod
        def TargetPoint(self, tag):

            time_stamp = datetime.now().time()
            message = print(f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} {self.__class__.__name__.upper()}:{Fore.RED}CALL_TARGET_POINT {Style.BRIGHT}"{tag}"')
            return message

    class DebugMessage:

        @staticmethod
        def SignalEmit(self, signal, target=''):

            time_stamp = datetime.now().time()
            if target != '':
                target = f' {Fore.YELLOW}"target": {target}{Fore.RESET}'

            message = print(f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} {self.__class__.__name__.upper()}:{Fore.YELLOW}EMIT: "event": {Style.BRIGHT}{signal.event}{Style.NORMAL}, "subtype": {Style.BRIGHT}{signal.subtype}{Style.NORMAL},{Fore.RESET} "type": {signal.type}{target}')
            return message

        @staticmethod
        def SignalReceived(self, signal, target=''):

            time_stamp = datetime.now().time()
            if target != '':
                target = f' "target": {Fore.CYAN}{target}{Fore.RESET}'

            message = print(f'{Fore.LIGHTBLACK_EX}[{time_stamp}]{Fore.RESET} {self.__class__.__name__.upper()}:{Fore.CYAN}RECEIVED: "event": {Style.BRIGHT}{signal.event}{Style.NORMAL}, "subtype": {Style.BRIGHT}{signal.subtype}{Style.NORMAL},{Fore.RESET} "type": {signal.type}{target}')
            return message
