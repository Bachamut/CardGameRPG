from game_object.game_object import GameObject
from property.initialize_property import InitializeProperty, InitializeState

from assets.lib.battle_system.log import Logs


class BattleSummaryScreenController(GameObject):

    def __init__(self):
        super(BattleSummaryScreenController, self).__init__()

    def _initialize(self):

        if InitializeProperty.check_is_ready(self, InitializeState.INITIALIZED):
            InitializeProperty.initialize_enable(self)
            Logs.InfoMessage.simple_info(self, "BattleSumaryScreen.Controller Initialized [ OK ]")

            return

        if InitializeProperty.check_is_ready(self, InitializeState.STARTED):
            InitializeProperty.started(self)
            self.property('EventProperty').property_enable()
            self.property('InitializeProperty').property_disable()
            Logs.InfoMessage.simple_info(self, "BattleSumaryScreen.Controller Started [ OK ]")

            return

    def on_event(self, event):

        pass
