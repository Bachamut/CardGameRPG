from object_creator.object_creator import ObjectCreator
from property.initialize_property import InitializeProperty, InitializeState

from assets.lib.battle_system.battle_character_utilities.battle_character_view import BattleCharacterView
from assets.lib.battle_system.log import Logs
from assets.lib.battle_system.view_controllers.battle_character_view_manager import BattleCharacterViewManager
from assets.lib.game_object_shared_resource import GameObjectSharedResource
from assets.lib.ui.container import Container


class BattleCharacterViewController(GameObjectSharedResource):

    battle_character_view_list = BattleCharacterViewManager.battle_character_view_list

    def __init__(self):
        super(BattleCharacterViewController, self).__init__()

    def _initialize(self):

        if InitializeProperty.check_is_ready(self, InitializeState.INITIALIZED):
            super(BattleCharacterViewController, self)._initialize()
            InitializeProperty.initialize_enable(self)
            Logs.InfoMessage.simple_info(self, "BattleCharacterView.Controller Initialized [ OK ]")

            return

        if InitializeProperty.check_is_ready(self, InitializeState.STARTED):

            view_container = Container()
            view_container.property('TransformProperty').position.x = 200
            view_container.property('TransformProperty').position.y = 200

            players = ObjectCreator.create_entity('battle_scene', 'Players')
            players.initialize(self.battle_ally[0])
            view_container.attach_child(players)

            players.change_set('attack')
            # players.set_alpha(50)
            players.scale(4)

            enemies = ObjectCreator.create_entity('battle_scene', 'Enemies')
            view_container.attach_child(enemies)
            enemies.property('TransformProperty').position.x = 550

            InitializeProperty.started(self)
            self.property('SignalProperty').property_enable()
            Logs.InfoMessage.simple_info(self, "BattleCharacterView.Controller Started [ OK ]")

            return

    @staticmethod
    def register(battle_character_view):
        BattleCharacterViewController.battle_character_view_list.append(battle_character_view)

    def on_script(self):
        pass

    def on_signal(self, signal):

        pass
