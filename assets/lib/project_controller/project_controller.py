import pygame.time
from game_object.game_object import GameObject
from game_object.object_state import ObjectState
from property.initialize_property import InitializeProperty, InitializeState
from resource_manager.resource_manager import ResourceManager
from scene_creator.scene_creator import SceneCreator


from assets.lib.battle_system.log import Logs


class ProjectController(GameObject):

    START_CHARACTER_SHEET_SCENE_TIME_EVENT = pygame.event.custom_type()
    START_BATTLE_SUMMARY_SCENE_TIME_EVENT = pygame.event.custom_type()
    START_MAIN_MENU_SCENE_TIME_EVENT = pygame.event.custom_type()
    START_BATTLE_SCENE_SCENE_TIME_EVENT = pygame.event.custom_type()
    START_END_SCENE_TIME_EVENT = pygame.event.custom_type()
    START_CARD_COLLECTION_SCENE_TIME_EVENT = pygame.event.custom_type()
    START_PAUSE_MENU_SCENE_TIME_EVENT = pygame.event.custom_type()

    def __init__(self):
        super(ProjectController, self).__init__()

    def _initialize(self):

        if InitializeProperty.check_is_ready(self, InitializeState.INITIALIZED):

            SceneCreator._scene = "battle_scene"
            SceneCreator.load_entity_config(SceneCreator._scene)
            SceneCreator.load_resource_config(SceneCreator._scene)
            scene_config = SceneCreator.get_scene_resources_config(SceneCreator._scene)
            ResourceManager.load_resources(scene_config)
            SceneCreator.create_scene(SceneCreator._scene)
            # SceneCreator.set_state(ObjectState.Suspended)

            InitializeProperty.initialize_enable(self)
            Logs.InfoMessage.simple_info(self, "Project.Controller Initialized [ OK ]")

            return

        if InitializeProperty.check_is_ready(self, InitializeState.STARTED):
            InitializeProperty.started(self)
            self.property('EventProperty').property_enable()
            self.property('InitializeProperty').property_disable()
            Logs.InfoMessage.simple_info(self, "Project.Controller Started [ OK ]")

            return

    def on_event(self, event):

        if event.type == ProjectController.START_END_SCENE_TIME_EVENT:

            pygame.time.set_timer(ProjectController.START_END_SCENE_TIME_EVENT, 0)
            SceneCreator.destroy(SceneCreator._scene)

            ProjectController.load_scene("end_scene")

        if event.type == ProjectController.START_CHARACTER_SHEET_SCENE_TIME_EVENT:

            pygame.time.set_timer(ProjectController.START_CHARACTER_SHEET_SCENE_TIME_EVENT, 0)
            SceneCreator.destroy(SceneCreator._scene)

            ProjectController.load_scene("character_sheet_scene")

        if event.type == ProjectController.START_BATTLE_SUMMARY_SCENE_TIME_EVENT:

            pygame.time.set_timer(ProjectController.START_BATTLE_SUMMARY_SCENE_TIME_EVENT, 0)
            SceneCreator.destroy(SceneCreator._scene)

            ProjectController.load_scene("battle_summary_scene")

        if event.type == ProjectController.START_MAIN_MENU_SCENE_TIME_EVENT:

            pygame.time.set_timer(ProjectController.START_MAIN_MENU_SCENE_TIME_EVENT, 0)
            SceneCreator.destroy(SceneCreator._scene)

            ProjectController.load_scene("main_menu_scene")

        if event.type == ProjectController.START_BATTLE_SCENE_SCENE_TIME_EVENT:

            pygame.time.set_timer(ProjectController.START_BATTLE_SCENE_SCENE_TIME_EVENT, 0)
            SceneCreator.destroy(SceneCreator._scene)

            ProjectController.load_scene("battle_scene")

        if event.type == ProjectController.START_CARD_COLLECTION_SCENE_TIME_EVENT:

            pygame.time.set_timer(ProjectController.START_CARD_COLLECTION_SCENE_TIME_EVENT, 0)
            SceneCreator.destroy(SceneCreator._scene)

            ProjectController.load_scene("card_collection_scene")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_p:

                pygame.time.set_timer(ProjectController.START_PAUSE_MENU_SCENE_TIME_EVENT, 0)
                # SceneCreator.destroy(SceneCreator._scene)
                SceneCreator.set_state(ObjectState.Stopped)

                # ProjectController.load_scene("pause_menu_scene")

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_o:

                pygame.time.set_timer(ProjectController.START_BATTLE_SCENE_SCENE_TIME_EVENT, 0)
                # SceneCreator.destroy(SceneCreator._scene)
                SceneCreator.set_state(ObjectState.Active)

                # ProjectController.load_scene("pause_menu_scene")

    @staticmethod
    def load_scene(scene_name):

        SceneCreator._scene = scene_name
        SceneCreator.load_entity_config(SceneCreator._scene)
        SceneCreator.load_resource_config(SceneCreator._scene)
        scene_config = SceneCreator.get_scene_resources_config(SceneCreator._scene)
        ResourceManager.load_resources(scene_config)
        SceneCreator.create_scene(SceneCreator._scene)
