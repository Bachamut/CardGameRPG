import pygame.time
from game_object.game_object import GameObject
from property.initialize_property import InitializeProperty, InitializeState
from resource_manager.resource_manager import ResourceManager
from scene_creator.scene_creator import SceneCreator

from assets.lib.battle_system.log import Logs


class ProjectController(GameObject):

    UNLOAD_START_SCENE_TIME_EVENT = pygame.event.custom_type()
    UNLOAD_END_SCENE_TIME_EVENT = pygame.event.custom_type()
    UNLOAD_BATTLE_SCENE_TIME_EVENT = pygame.event.custom_type()

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

            InitializeProperty.initialize_enable(self)
            Logs.InfoMessage.simple_info(self, "Project.Controller Initialized [ OK ]")

            return

        if InitializeProperty.check_is_ready(self, InitializeState.STARTED):
            InitializeProperty.started(self)
            self.property('EventProperty').property_enable()

            Logs.InfoMessage.simple_info(self, "Project.Controller Started [ OK ]")

            return

    def on_event(self, event):

        if event.type == ProjectController.UNLOAD_START_SCENE_TIME_EVENT:

            pygame.time.set_timer(ProjectController.UNLOAD_START_SCENE_TIME_EVENT, 0)
            SceneCreator.destroy(SceneCreator._scene)

            SceneCreator._scene = "battle_scene"
            SceneCreator.load_entity_config(SceneCreator._scene)
            SceneCreator.load_resource_config(SceneCreator._scene)
            scene_config = SceneCreator.get_scene_resources_config(SceneCreator._scene)
            ResourceManager.load_resources(scene_config)
            SceneCreator.create_scene(SceneCreator._scene)

        if event.type == ProjectController.UNLOAD_BATTLE_SCENE_TIME_EVENT:

            pygame.time.set_timer(ProjectController.UNLOAD_BATTLE_SCENE_TIME_EVENT, 0)
            SceneCreator.destroy(SceneCreator._scene)

            SceneCreator._scene = "end_scene"
            SceneCreator.load_entity_config(SceneCreator._scene)
            SceneCreator.load_resource_config(SceneCreator._scene)
            scene_config = SceneCreator.get_scene_resources_config(SceneCreator._scene)
            ResourceManager.load_resources(scene_config)
            SceneCreator.create_scene(SceneCreator._scene)

        if event.type == ProjectController.UNLOAD_END_SCENE_TIME_EVENT:

            pygame.time.set_timer(ProjectController.UNLOAD_END_SCENE_TIME_EVENT, 0)
            SceneCreator.destroy(SceneCreator._scene)

            SceneCreator._scene = "start_scene"
            SceneCreator.load_entity_config(SceneCreator._scene)
            SceneCreator.load_resource_config(SceneCreator._scene)
            scene_config = SceneCreator.get_scene_resources_config(SceneCreator._scene)
            ResourceManager.load_resources(scene_config)
            SceneCreator.create_scene(SceneCreator._scene)
