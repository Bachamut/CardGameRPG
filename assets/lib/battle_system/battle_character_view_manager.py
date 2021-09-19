import pygame
from property.initialize_property import InitializeProperty, InitializeState

from assets.lib.battle_system.battle_character_view import BattleCharacterView
from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.battle_system.log import Logs
from assets.lib.game_object_shared_resource import GameObjectSharedResource


class BattleCharacterViewManager(GameObjectSharedResource):

    battle_character_view_list = list()

    def __init__(self):
        super(BattleCharacterViewManager, self).__init__()

    def _initialize(self):

        if InitializeProperty.check_status(self, InitializeState.INITIALIZED):
            super(BattleCharacterViewManager, self)._initialize()
            InitializeProperty.initialize_enable(self)
            Logs.InfoMessage.SimpleInfo(self, "BattleCharacterViewManager Initialized [ OK ]")

            return

        if InitializeProperty.check_status(self, InitializeState.STARTED):
            InitializeProperty.started(self)
            self.property('SignalProperty').property_enable()
            Logs.InfoMessage.SimpleInfo(self, "BattleCharacterViewManager Started [ OK ]")

            return

    @staticmethod
    def register(battle_character_view):
        BattleCharacterViewManager.battle_character_view_list.append(battle_character_view)

    def on_script(self):
        pass

    def on_signal(self, signal):

        print(f'Waiting for Signal')

        # BChVMS1
        if signal.type == BattleLogic.CHARACTER_VIEW_MANAGER_SIGNAL and signal.subtype == "INITIAL":
            Logs.DebugMessage.SignalReceived(self, signal, "BChVMS1<-BLS1")

            # Create CharacterViews and register in BattleCharacterViewManager
            for battle_character in self.battle_ally + self.battle_enemies:
                battle_character_view = BattleCharacterView(battle_character)
                BattleCharacterViewManager.register(battle_character_view)

            self.property('SignalProperty').property_disable()

            emit_signal = pygame.event.Event(BattleLogic.CHARACTER_VIEW_MANAGER_RESPONSE, {"event": "CHARACTER_VIEW_MANAGER_RESPONSE", "subtype": "INITIAL"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.SignalEmit(self, emit_signal, "BChVMS1->BLS2")
            return
