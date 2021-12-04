from game_object.game_object import GameObject
from property.initialize_property import InitializeProperty, InitializeState

from assets.lib.battle_system.log import Logs


class CharacterSheetScreenController(GameObject):

    def __init__(self):
        super(CharacterSheetScreenController, self).__init__()

    def _initialize(self):

        if InitializeProperty.check_is_ready(self, InitializeState.INITIALIZED):
            InitializeProperty.initialize_enable(self)
            Logs.InfoMessage.simple_info(self, "CharacterSheetScreen.Controller Initialized [ OK ]")

            return

        if InitializeProperty.check_is_ready(self, InitializeState.STARTED):
            InitializeProperty.started(self)
            self.property('EventProperty').property_enable()
            Logs.InfoMessage.simple_info(self, "CharacterSheetScreen.Controller Started [ OK ]")

            return

    def on_event(self, event):

        pass
