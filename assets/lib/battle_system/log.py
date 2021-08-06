class Logs:
    # LogMessage DebugMessage InfoMessage

    class InfoMessage:

        @staticmethod
        def TargetPoint(self, tag):

            message = print(f'{self.__class__.__name__.upper()}:CALL_TARGET_POINT "{tag}"')
            return message

    class DebugMessage:

        @staticmethod
        def SignalEmit(self, signal):

            message = print(f'{self.__class__.__name__.upper()}:EMIT: "event": {signal.event}, "subtype": {signal.subtype}, "type": {signal.type}')
            return message

        @staticmethod
        def SignalReceived(self, signal):

            message = print(f'{self.__class__.__name__.upper()}:RECEIVED: "event": {signal.event}, "subtype": {signal.subtype}, "type": {signal.type}')
            return message
