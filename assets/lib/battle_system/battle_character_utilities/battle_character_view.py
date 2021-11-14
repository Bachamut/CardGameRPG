import pygame
from game_object.game_object import GameObject

from assets.lib.battle_system.battle_logic import BattleLogic


class BattleCharacterView(GameObject):

    def __init__(self):
        super(BattleCharacterView, self).__init__()

        self.add_property('SpriteSheetAnimationProperty')
        self.add_property('BlitProperty')
        self.add_property('TransformProperty')
        self.add_property('ScriptProperty')
        self.add_property('SignalProperty')
        self.property('SignalProperty').property_enable()

        self._scale = 1
        self.active_set = None
        self.frame = 0
        self.max_frames = 0
        self.alphe = 256

    def initialize(self, battle_character, set_resource):
        # reference to character
        self.character_model = battle_character
        self.character_model_hash = battle_character.object_hash

        # print(f'name: {battle_character.name} hash: {battle_character.object_hash}')

        self.property('SpriteSheetAnimationProperty').configure(set_resource)
        self.active_set = self.property('SpriteSheetAnimationProperty').active_set
        self.frame = self.property('SpriteSheetAnimationProperty').frame
        self.max_frames = self.property('SpriteSheetAnimationProperty').max_frames

        return self

    def change_set(self, animation_set):

        self.property('SpriteSheetAnimationProperty').change_set(animation_set)

    def scale(self, scale):

        self._scale = scale
        self.property('SpriteSheetAnimationProperty').scale(self._scale)

    def set_alpha(self, alpha):

        self.alphe = alpha
        self.property('SpriteSheetAnimationProperty').set_alpha(alpha)

    def on_script(self):

        self.property('SpriteSheetAnimationProperty').next_frame()

    def on_signal(self, signal):

        if signal.type == BattleLogic.CHARACTER_VIEW_SIGNAL and signal.subtype == "TARGET":
            if signal.receiver.object_hash == self.character_model.object_hash:

                print(f'CHARACTER_VIEW_SIGNAL:TARGET processed on receiver')

                return

        if signal.type == BattleLogic.CHARACTER_VIEW_SIGNAL and signal.subtype == "CASTER":
            if signal.receiver.object_hash == self.character_model.object_hash:

                print(f'CHARACTER_VIEW_SIGNAL:CASTER processed on receiver')

                return
