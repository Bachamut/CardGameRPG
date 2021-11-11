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

        self.players = None
        self.animation_reset = False

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

            self.players = ObjectCreator.create_entity('battle_scene', 'Players')
            self.players.initialize(self.battle_ally[0])
            view_container.attach_child(self.players)

            self.players.change_set('attack')
            self.players.scale(4)

            enemies = ObjectCreator.create_entity('battle_scene', 'Enemies')
            view_container.attach_child(enemies)
            enemies.property('TransformProperty').position.x = 550

            InitializeProperty.started(self)
            self.property('SignalProperty').property_enable()
            self.property('ScriptProperty').property_enable()
            Logs.InfoMessage.simple_info(self, "BattleCharacterView.Controller Started [ OK ]")

            return

    @staticmethod
    def register(battle_character_view):
        BattleCharacterViewController.battle_character_view_list.append(battle_character_view)

    def on_script(self):

        if self.animation_reset is False:

            if self.players.property('SpriteSheetAnimationProperty').frame >= self.players.max_frames:

                self.animation_reset = True
                self.players.change_set('idle')
                self.players.scale(4)

        if self.animation_reset is True:

            if self.players.property('SpriteSheetAnimationProperty').frame >= self.players.max_frames - 1:

                self.animation_reset = False
                self.players.change_set('attack')
                self.players.scale(4)

    def on_signal(self, signal):

        pass
