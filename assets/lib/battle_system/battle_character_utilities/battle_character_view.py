import pygame
from game_object.game_object import GameObject

from assets.lib.battle_system.battle_logic import BattleLogic


class BattleCharacterView(GameObject):

    def __init__(self):
        super(BattleCharacterView, self).__init__()

        self.add_property("SignalProperty")
        self.property("SignalProperty").property_enable()

    def initialize(self, battle_character):
        # reference to character
        self.character_model = battle_character
        self.character_model_hash = battle_character.object_hash

        print(f'name: {battle_character.name} hash: {battle_character.object_hash}')

        self.x = 4
        # self.property('SpriteProperty').surface = pygame.transform.scale(self.property('SpriteProperty').surface, (2720 * self.x, 96 * self.x))
        # self.property('SpriteProperty').rect = pygame.Rect(0, 0, 170 * self.x, 96 * self.x)

        self.property('SpriteProperty').surface = pygame.transform.scale(self.property('SpriteProperty').surface, (5100 * self.x, 96 * self.x))
        self.property('SpriteProperty').rect = pygame.Rect(0, 0, 170 * self.x, 96 * self.x)

    def on_script(self):

        # self.property('SpriteProperty').rect.left += 170 * self.x
        # if self.property('SpriteProperty').rect.left > 2720 * self.x - 170 * self.x:
        #
        #     self.property('SpriteProperty').rect.left = 0

        self.property('SpriteProperty').rect.left += 170 * self.x
        if self.property('SpriteProperty').rect.left > 5100 * self.x - 170 * self.x:

            self.property('SpriteProperty').rect.left = 0

    def on_signal(self, signal):

        if signal.type == BattleLogic.CHARACTER_VIEW_SIGNAL and signal.subtype == "TARGET":
            if signal.receiver.object_hash == self.character_model.object_hash:

                print(f'CHARACTER_VIEW_SIGNAL:TARGET processed on receiver')

                return

        if signal.type == BattleLogic.CHARACTER_VIEW_SIGNAL and signal.subtype == "CASTER":
            if signal.receiver.object_hash == self.character_model.object_hash:

                print(f'CHARACTER_VIEW_SIGNAL:CASTER processed on receiver')

                return
