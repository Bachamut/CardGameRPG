import pygame
from object_creator.object_creator import ObjectCreator
from property.initialize_property import InitializeProperty, InitializeState

from assets.lib.battle_system.battle_character_utilities.battle_character_view import BattleCharacterView
from assets.lib.battle_system.battle_logic import BattleLogic
from assets.lib.battle_system.log import Logs
from assets.lib.battle_system.view_controllers.battle_character_view_manager import BattleCharacterViewManager
from assets.lib.game_object_shared_resource import GameObjectSharedResource
from assets.lib.ui.container import Container


class BattleCharacterViewController(GameObjectSharedResource):

    def __init__(self):
        super(BattleCharacterViewController, self).__init__()

        self.change = False
        self.main_container = Container()
        self.left_container = Container()
        self.right_container = Container()

        self.main_container.attach_child(self.left_container)
        self.main_container.attach_child(self.right_container)

        self.battle_character_view_list = list()
        self.battle_character_field = dict()

    def _initialize(self):

        if InitializeProperty.check_is_ready(self, InitializeState.INITIALIZED):
            super(BattleCharacterViewController, self)._initialize()

            # Setup containers
            self.main_container.property('TransformProperty').position.x = 130
            self.main_container.property('TransformProperty').position.y = 150
            self.right_container.property('TransformProperty').position.x = 450

            # Setup Board Fields on left Container
            for index in range(0, 3):

                field_name = f'field_0{index}'
                container = Container()
                self.left_container.attach_child(container)
                container.property('TransformProperty').position.y = index * -45

                self.battle_character_field[field_name] = container

            # Setup Board Fields on left Container
            for index in range(3, 6):

                field_name = f'field_0{index}'
                container = Container()
                self.right_container.attach_child(container)
                container.property('TransformProperty').position.y = (index - 3) * 45

                self.battle_character_field[field_name] = container


            InitializeProperty.initialize_enable(self)
            self.property('SignalProperty').property_enable()
            Logs.InfoMessage.simple_info(self, "BattleCharacterView.Controller Initialized [ OK ]")

            return

    def register(self, battle_character_view):
        self.battle_character_view_list.append(battle_character_view)

    def on_script(self):

        for character_view in self.battle_character_view_list:
            if character_view.property('SpriteSheetAnimationProperty').frame >= character_view.max_frames:
                # self.animation_reset = True
                character_view.change_set(character_view.default_set)
                character_view.scale(4)

            # testing
            if character_view.animation_queue:
                if character_view.property('SpriteSheetAnimationProperty').frame >= character_view.max_frames - 1:

                    if character_view.animation_queue[0].action_type == "basic_attack" or \
                            character_view.animation_queue[0].action_type == "counter_attack":
                        character_view.change_set('melee')
                        character_view.scale(4)
                        character_view.animation_queue.remove(character_view.animation_queue[0])

                    elif character_view.animation_queue[0].action_type == "bow_attack":
                        character_view.change_set('ranged')
                        character_view.scale(4)
                        character_view.animation_queue.remove(character_view.animation_queue[0])

                    elif character_view.animation_queue[0].action_type == "self_skill":
                        character_view.change_set('shield')
                        character_view.scale(4)
                        character_view.animation_queue.remove(character_view.animation_queue[0])

                    elif character_view.animation_queue[0].action_type == "special_attack":
                        character_view.change_set('leap')
                        character_view.scale(4)
                        character_view.animation_queue.remove(character_view.animation_queue[0])

                else:
                    print(f'trwa animacja')


        # if self.change is False:
        #
        #     character = self.battle_character_view_list[0]
        #     character.change_set('idle')
        #     character.scale(4)
        #
        #     self.change = True

        # if self.animation_reset is False:
        #
        #     if self.players.property('SpriteSheetAnimationProperty').frame >= self.players.max_frames:
        #
        #         self.animation_reset = True
        #         self.players.change_set('leap')
        #         self.players.scale(4)
        #
        # if self.animation_reset is True:
        #
        #     if self.players.property('SpriteSheetAnimationProperty').frame >= self.players.max_frames:
        #
        #         self.animation_reset = False
        #         self.players.change_set('attack')
        #         self.players.scale(4)

        pass

    def on_signal(self, signal):

        # BChVCS1
        if signal.type == BattleLogic.CHARACTER_VIEW_CONTROLLER_SIGNAL and signal.subtype == "INITIAL":
            Logs.DebugMessage.signal_received(self, signal, "BChVCS1<-BLS1")

            self.character_view_setup(self.battle_ally, 0)

            self.character_view_setup(self.battle_enemies, 3)

            # self.property('SignalProperty').property_disable()
            InitializeProperty.started(self)
            # self.property('SignalProperty').property_enable()
            self.property('ScriptProperty').property_enable()
            Logs.InfoMessage.simple_info(self, "BattleCharacterView.Controller Started [ OK ]")

            emit_signal = pygame.event.Event(BattleLogic.CHARACTER_VIEW_CONTROLLER_RESPONSE, {"event": "CHARACTER_VIEW_CONTROLLER_RESPONSE", "subtype": "INITIAL"})
            pygame.event.post(emit_signal)
            Logs.DebugMessage.signal_emit(self, emit_signal, "BChVCS1->BLS2")

            return

        # BChVC1
        if signal.type == BattleLogic.CHARACTER_VIEW_CONTROLLER_SIGNAL and signal.subtype == "STANDARD":
            Logs.DebugMessage.signal_received(self, signal, "BChVC1<-BLS1")

            action_scenario = signal.action_scenario
            for animation_block in action_scenario:

                for character_view in self.battle_character_view_list:
                    if character_view.character_model == animation_block.caster:
                        character_view.animation_queue.append(animation_block)
            #             if animation_block.action == "physical_attack":
            #                 character_view.change_set('melee')
            #
            #             elif animation_block.action == "self_skill":
            #                 character_view.change_set('run')
            #
            #
            #             character_view.scale(4)
            #
            #         if character_view.character_model == animation_block.target:
            #             character_view.change_set('death')
            #             character_view.scale(4)

            return

        # BChVC2
        if signal.type == BattleLogic.BATTLE_LOGIC_SIGNAL and signal.subtype == "DESTROY_VIEW":
            Logs.DebugMessage.signal_received(self, signal, "BChVC1<-?BL101")

            self.destroy_character_view()

            return

    def character_view_setup(self, team, initial_index):

        index = initial_index
        # Create CharacterViews and register in BattleCharacterViewManager
        for battle_character in team:
            package, set_resource = battle_character.set_resource.split('/')
            battle_character_view = BattleCharacterView().initialize(battle_character, {'package': package, 'set_resource': set_resource})
            battle_character_view.default_set = 'idle'
            self.register(battle_character_view)
            field_index = f'field_0{index}'
            index += 1
            self.battle_character_field[field_index].attach_child(battle_character_view)
            battle_character_view.property('SpriteSheetAnimationProperty').scale(4)

    def destroy_character_view(self):

        # self.battle_character_view_list.clear()
        # self.battle_character_field.clear()
        self.main_container.property('TransformProperty').position.y = 1000

        # for character_view in self.battle_character_view_list:
        #
        #     character_view.change_set('death')
        #     character_view.scale(4)

