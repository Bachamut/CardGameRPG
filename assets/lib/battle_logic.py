import pygame

from assets.lib.game_logic import GameLogic
from game_object.game_object import GameObject

CHARACTER_CHANGED = pygame.event.custom_type()

class BattleLogic(GameObject):


    _initialized = False
    started = False
    current_character = None
    current_target = None
    selected_card = None

    character_model_active = False
    card_model_active = False

    def __init__(self):
        super(BattleLogic, self).__init__()

    def _initialize(self):
        BattleLogic._initialized = True

    def on_script(self):
        if not self._initialized and GameLogic._initialized:
            self._initialize()
        else:
            pass

        if BattleLogic.started == False \
            and len(GameObject.get_object_pool().select_with_label('CharacterModel')) != 0 \
            and len(GameObject.get_object_pool().select_with_label('CardModel')) != 0 \
            and len(GameObject.get_object_pool().select_with_label('CardView')) != 0:

            BattleLogic.started = True
            # Generating party and initial character order
            character_model = GameObject.get_object_pool().select_with_label('CharacterModel')[0]
            character_model.create_party()
            character_model.create_enemies()

            # WIP
            character_model.queue_model.create_queue()
            BattleLogic.current_character = character_model.queue_model.update_queue()

            card_model = GameObject.get_object_pool().select_with_label('CardModel')[0]
            for character in character_model.units:
                card_model.create_battledeck(character)
                card_model.draw_hand(character)

            BattleLogic.character_model_active = False
            BattleLogic.card_model_active = True

            signal = pygame.event.Event(CHARACTER_CHANGED)
            pygame.event.post(signal)

        elif BattleLogic.started == True:
            # signal = pygame.event.Event(CHARACTER_CHANGED)
            # pygame.event.post(signal)
            pass

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:

                character_model = GameObject.get_object_pool().select_with_label('CharacterModel')[0]
                # WIP
                BattleLogic.current_character = character_model.queue_model.update_queue()

                signal = pygame.event.Event(CHARACTER_CHANGED)
                pygame.event.post(signal)
