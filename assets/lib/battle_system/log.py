class Logs():

    class DebugMessage():


        @staticmethod
        def SignalEmit(self, signal):

            message = print(f'NOWE! {self.__class__.__name__.upper()}:EMIT: "event": {signal.event}, "subtype": {signal.subtype}, "type": {signal.type}')
            return message

        @staticmethod
        def SignalReceived(self, signal):

            message = print(f'NOWE! {self.__class__.__name__.upper()}:RECEIVED: "event": {signal.event}, "subtype": {signal.subtype}, "type": {signal.type}')
            return message


