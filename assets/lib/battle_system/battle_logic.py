import pygame

from game_object.game_object import GameObject
from assets.lib.game_logic import GameLogic
from resource_manager.shared_resource import SharedResource


class BattleLogic(GameObject):

    CURRENT_CHARACTER_SIGNAL = pygame.event.custom_type()
    CURRENT_CARD_SIGNAL = pygame.event.custom_type()
    STATUS_UPDATE_SIGNAL = pygame.event.custom_type()
    STATUS_RESET_SIGNAL = pygame.event.custom_type()
    CHARACTER_ACTIVE_SIGNAL = pygame.event.custom_type()
    TURN_ACTIVE_SIGNAL = pygame.event.custom_type()
    TARGET_SELECTED_SIGNAL = pygame.event.custom_type()

    character_model_active = False
    card_model_active = False
    turn_model_active = False

    _initialized = False
    started = False

    # SharedResources definitions

    @property
    def current_character(self):
        return self._current_character.take()

    @current_character.setter
    def current_character(self, character):
        self._current_character.set(character)

    @property
    def current_target(self):
        return self._current_target.take()

    @current_target.setter
    def current_target(self, character):
        self._current_target.set(character)

    @property
    def selected_target(self):
        return self._selected_target.take()

    @selected_target.setter
    def selected_target(self, target):
        self._selected_target.set(target)

    @property
    def current_card(self):
        return self._current_card.take()

    @current_card.setter
    def current_card(self, card):
        self._current_card.set(card)

    @property
    def selected_card(self):
        return self._selected_card.take()

    @selected_card.setter
    def selected_card(self, card):
        self._selected_card.set(card)

    @property
    def ally(self):
        return self._ally.take()

    @ally.setter
    def ally(self, ally):
        self._ally.set(ally)

    @property
    def enemies(self):
        return self._enemies.take()

    @enemies.setter
    def enemies(self, enemies):
        self._enemies.set(enemies)

    # end SharedResources


    def __init__(self):
        super(BattleLogic, self).__init__()

        self.queue_model = None

        ###
        self._current_character = SharedResource()
        self._current_target = SharedResource()
        self._selected_target = SharedResource()
        self._current_card = SharedResource()
        self._selected_card = SharedResource()

        self._ally = SharedResource()
        self._ally.set(list())

        self._enemies = SharedResource()
        self._enemies.set(list())

        ###

    def _initialize(self):
        BattleLogic._initialized = True
        print("BattleLogic initialized")

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
            self.current_character = queue[0]

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
            BattleLogic.turn_model_active = False

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

                # After one Turn update AP seeds for each Character i battle
                for key, values in self.queue_model.party.items():
                    self.queue_model.party[key] = next_seed[key]

                # Re-write Queue sequence to generated one
                self.queue_model.queue.clear()
                self.queue_model.queue += queue

                print('')
                for key, value in self.queue_model.party.items():
                    print(f'{key.name}: {value} | {self.queue_model.characters_speed[key]} +{self.queue_model.modifiers[key]}')

                BattleLogic.character_model_active = False
                BattleLogic.card_model_active = True
                BattleLogic.turn_model_active = False

                signal = pygame.event.Event(BattleLogic.CURRENT_CHARACTER_SIGNAL, {"event": "CHARACTER_CHANGED_SIGNAL"})
                pygame.event.post(signal)

                signal = pygame.event.Event(BattleLogic.STATUS_UPDATE_SIGNAL, {"event": "STATUS_UPDATE_SIGNAL"})
                pygame.event.post(signal)

                print(f'battle_logic current_character: {self.current_character.name}')

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                self.queue_model.modifiers[BattleLogic.current_character] += 10

                print('')
                for key, value in self.queue_model.party.items():
                    print(f'{key.name}: {value} | {self.queue_model.characters_speed[key]} +{self.queue_model.modifiers[key]}')

    def on_signal(self, signal):
        if BattleLogic._initialized:
            if signal.type == BattleLogic.CURRENT_CARD_SIGNAL:
                print(f'odebrano sygnał "CURRENT_CARD_SIGNAL"')

                BattleLogic.character_model_active = False
                BattleLogic.card_model_active = False
                BattleLogic.turn_model_active = False

                # Call CHARACTER_ACTIVE_SIGNAL to the CharacterModel to choose target
                signal = pygame.event.Event(BattleLogic.CHARACTER_ACTIVE_SIGNAL, {"event": "CHARACTER_ACTIVE_SIGNAL"})
                pygame.event.post(signal)

            if signal.type == BattleLogic.TARGET_SELECTED_SIGNAL:
                print(f'odebrano sygnał "TARGET_SELECTED_SIGNAL"')

                BattleLogic.character_model_active = False
                BattleLogic.card_model_active = False
                BattleLogic.turn_model_active = False

                signal = pygame.event.Event(BattleLogic.TURN_ACTIVE_SIGNAL)
                pygame.event.post(signal)
