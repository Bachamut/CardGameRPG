import pygame

from assets.lib.game_logic import GameLogic
from game_object.game_object import GameObject
from lib.queue_model import QueueModel

CHARACTER_CHANGED_SIGNAL = pygame.event.custom_type()

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

        self.queue_model = None
        self.queue_view = None

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

            self.queue_model = QueueModel()
            self.queue_model.setup_queue(character_model.party + character_model.enemies)

            queue = self.queue_model.get_queue(
                self.queue_model.party,
                self.queue_model.characters_speed,
                self.queue_model.modifiers
            )

            BattleLogic.current_character = queue[0]

            next_seed = QueueModel.get_next_seed(
                self.queue_model.party,
                self.queue_model.characters_speed,
                self.queue_model.modifiers
            )

            for key, values in self.queue_model.party.items():
                self.queue_model.party[key] = next_seed[key]

            self.queue_view = queue

            print('')
            for key, value in self.queue_model.party.items():
                print(f'{key.name}: {value} | {self.queue_model.characters_speed[key]} +{self.queue_model.modifiers[key]}')

            # WIP
            # character_model.queue_model.create_queue()
            # BattleLogic.current_character = character_model.queue_model.update_queue()

            card_model = GameObject.get_object_pool().select_with_label('CardModel')[0]
            for character in character_model.party + character_model.enemies:
                card_model.create_battledeck(character)
                card_model.draw_hand(character)

            BattleLogic.character_model_active = False
            BattleLogic.card_model_active = True

            signal = pygame.event.Event(CHARACTER_CHANGED_SIGNAL)
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

                queue = self.queue_model.get_queue(
                    self.queue_model.party,
                    self.queue_model.characters_speed,
                    self.queue_model.modifiers)

                BattleLogic.current_character = queue[0]

                next_seed = QueueModel.get_next_seed(
                    self.queue_model.party,
                    self.queue_model.characters_speed,
                    self.queue_model.modifiers
                )

                for key, values in self.queue_model.party.items():
                    self.queue_model.party[key] = next_seed[key]

                self.queue_view = queue

                print('')
                for key, value in self.queue_model.party.items():
                    print(f'{key.name}: {value} | {self.queue_model.characters_speed[key]} +{self.queue_model.modifiers[key]}')

                signal = pygame.event.Event(CHARACTER_CHANGED_SIGNAL)
                pygame.event.post(signal)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.queue_model.modifiers[BattleLogic.current_character] += 50

                print('')
                for key, value in self.queue_model.party.items():
                    print(f'{key.name}: {value} | {self.queue_model.characters_speed[key]} +{self.queue_model.modifiers[key]}')
