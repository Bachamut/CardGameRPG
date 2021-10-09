from object_creator.object_creator import ObjectCreator
from property.initialize_property import InitializeProperty, InitializeState

from assets.lib.battle_system.log import Logs
from assets.lib.battle_system.view_controllers.battle_character_view_manager import BattleCharacterViewManager
from assets.lib.game_object_shared_resource import GameObjectSharedResource


class BattleCharacterViewController(GameObjectSharedResource):

    battle_character_view_list = BattleCharacterViewManager.battle_character_view_list

    def __init__(self):
        super(BattleCharacterViewController, self).__init__()

    def _initialize(self):

        if InitializeProperty.check_is_ready(self, InitializeState.INITIALIZED):
            super(BattleCharacterViewController, self)._initialize()
            InitializeProperty.initialize_enable(self)
            Logs.InfoMessage.SimpleInfo(self, "BattleCharacterView.Controller Initialized [ OK ]")

            return

        if InitializeProperty.check_is_ready(self, InitializeState.STARTED):

            entity = ObjectCreator.create_entity('Players')

            InitializeProperty.started(self)
            self.property('SignalProperty').property_enable()
            Logs.InfoMessage.SimpleInfo(self, "BattleCharacterView.Controller Started [ OK ]")

            return

    @staticmethod
    def register(battle_character_view):
        BattleCharacterViewController.battle_character_view_list.append(battle_character_view)

    def on_script(self):
        pass

    def on_signal(self, signal):

        print(f'Waiting for Signal')

        pass
