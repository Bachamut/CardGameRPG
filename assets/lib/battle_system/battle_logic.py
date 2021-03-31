import pygame

from game_object.game_object import GameObject
from assets.lib.game_logic import GameLogic


class BattleLogic(GameObject):

    CURRENT_CHARACTER_SIGNAL = pygame.event.custom_type()
    STATUS_UPDATE_SIGNAL = pygame.event.custom_type()
    STATUS_RESET_SIGNAL = pygame.event.custom_type()

    _initialized = False
    started = False

    current_character = None
    current_target = None
    selected_target = None
    current_card = None
    selected_card = None

    ally = list()
    enemies = list()

    character_model_active = False
    card_model_active = False

    def __init__(self):
        super(BattleLogic, self).__init__()

        self.queue_model = None

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
            and len(GameObject.get_object_pool().select_with_label('QueueModel')) != 0 \
            and len(GameObject.get_object_pool().select_with_label('CardView')) != 0:

            BattleLogic.started = True
            # Generating party and initial character order
            character_model = GameObject.get_object_pool().select_with_label('CharacterModel')[0]
            character_model.create_ally()
            character_model.create_enemies()

            self.queue_model = GameObject.get_object_pool().select_with_label('QueueModel')[0]
            GameObject.add_new_object(self.queue_model)
            self.queue_model.setup_queue()

            queue = self.queue_model.get_queue()
            BattleLogic.current_character = queue[0]

            next_seed = self.queue_model.get_next_seed()

            # can be moved to get_next_seed()
            for key, values in self.queue_model.party.items():
                self.queue_model.party[key] = next_seed[key]

            self.queue_model.queue = queue

            print('')
            for key, value in self.queue_model.party.items():
                print(f'{key.name}: {value} | {self.queue_model.characters_speed[key]} +{self.queue_model.modifiers[key]}')

            card_model = GameObject.get_object_pool().select_with_label('CardModel')[0]
            for character in character_model.ally + character_model.enemies:
                card_model.create_battledeck(character)
                card_model.draw_hand(character)

            BattleLogic.character_model_active = False
            BattleLogic.card_model_active = True

            signal = pygame.event.Event(BattleLogic.CURRENT_CHARACTER_SIGNAL, {"event": "CHARACTER_CHANGED_SIGNAL"})
            pygame.event.post(signal)

            signal = pygame.event.Event(BattleLogic.STATUS_RESET_SIGNAL, {"event": "STATUS_RESET_SIGNAL"})
            pygame.event.post(signal)

        elif BattleLogic.started == True:
            # signal = pygame.event.Event(CHARACTER_CHANGED)
            # pygame.event.post(signal)
            pass

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:

                queue = self.queue_model.get_queue()

                BattleLogic.current_character = queue[0]

                next_seed = self.queue_model.get_next_seed()

                for key, values in self.queue_model.party.items():
                    self.queue_model.party[key] = next_seed[key]

                self.queue_model.queue.clear()
                self.queue_model.queue += queue

                print('')
                for key, value in self.queue_model.party.items():
                    print(f'{key.name}: {value} | {self.queue_model.characters_speed[key]} +{self.queue_model.modifiers[key]}')

                signal = pygame.event.Event(BattleLogic.CURRENT_CHARACTER_SIGNAL, {"event": "CHARACTER_CHANGED_SIGNAL"})
                pygame.event.post(signal)

                BattleLogic.ally[0].attributes.health += -20

                signal = pygame.event.Event(BattleLogic.STATUS_UPDATE_SIGNAL, {"event": "STATUS_UPDATE_SIGNAL"})
                pygame.event.post(signal)

                print(f'battle_logic current_character: {BattleLogic.current_character.name}')
                # _character_model = GameObject.get_object_pool().select_with_label("CharacterModel")[0]
                # print(f'character_model current_character: {_character_model.current_character.name}')
                _card_model = GameObject.get_object_pool().select_with_label("CardModel")[0]
                print(f'card_model current_character: {_card_model.current_character.name}')

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.queue_model.modifiers[BattleLogic.current_character] += 50

                print('')
                for key, value in self.queue_model.party.items():
                    print(f'{key.name}: {value} | {self.queue_model.characters_speed[key]} +{self.queue_model.modifiers[key]}')
