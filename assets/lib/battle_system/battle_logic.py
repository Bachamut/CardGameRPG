import pygame

from game_object.game_object import GameObject

from assets.lib.battle_system.battle_character import BattleCharacter
from assets.lib.battle_system.character_view_init import CharacterView
from assets.lib.character_utilities.character import BaseCharacter
from assets.lib.game_logic import GameLogic
from resource_manager.shared_resource import SharedResource
from assets.lib.battle_system.log import Logs


class BattleLogic(GameObject):

    BATTLE_LOGIC_SIGNAL = pygame.event.custom_type()

    QUEUE_MODEL_SIGNAL = pygame.event.custom_type()
    ACTION_MODEL_SIGNAL = pygame.event.custom_type()
    SHUFFLE_DECK_SIGNAL = pygame.event.custom_type()
    DRAW_CARD_SIGNAL = pygame.event.custom_type()
    CARD_MODEL_SIGNAL = pygame.event.custom_type()
    ITEM_MODEL_SIGNAL = pygame.event.custom_type()
    CHARACTER_MODEL_SIGNAL = pygame.event.custom_type()

    QUEUE_MODEL_RESPONSE = pygame.event.custom_type()
    ACTION_MODEL_RESPONSE = pygame.event.custom_type()
    SHUFFLE_DECK_RESPONSE = pygame.event.custom_type()
    DRAW_CARD_RESPONSE = pygame.event.custom_type()
    CARD_MODEL_RESPONSE = pygame.event.custom_type()
    ITEM_MODEL_RESPONSE = pygame.event.custom_type()
    CHARACTER_MODEL_RESPONSE = pygame.event.custom_type()

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
    def battle_ally(self):
        return self._battle_ally.take()

    @battle_ally.setter
    def battle_ally(self, ally):
        self._battle_ally.set(ally)

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

        self._battle_ally = SharedResource()
        self._battle_ally.set(list())

        self._enemies = SharedResource()
        self._enemies.set(list())


        _game_logic = GameObject.get_object_pool().select_with_label("GameLogic")[0]
        self._base_ally= _game_logic.party
        self._base_enemies = _game_logic.enemies

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

            print(f'BATTLE_LOGIC:EMIT_SIGNAL: "event": "BATTLE_LOGIC_SIGNAL", "subtype": "INITIAL"')
            signal = pygame.event.Event(BattleLogic.BATTLE_LOGIC_SIGNAL, {"event": "BATTLE_LOGIC_SIGNAL", "subtype": "INITIAL"})
            pygame.event.post(signal)


        elif BattleLogic.started == True:
            # signal = pygame.event.Event(CHARACTER_CHANGED)
            # pygame.event.post(signal)
            pass

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                pass

    def on_signal(self, signal):
        if BattleLogic._initialized:

            # BATTLE_LOGIC INITIAL
            # BL0
            if signal.type == BattleLogic.BATTLE_LOGIC_SIGNAL and signal.subtype == "INITIAL":
                Logs.DebugMessage.SignalReceived(self, signal, "BL0<-INIT")

                # # battlecharacters creation

                self.battle_ally = BattleCharacter.create_character_models(self._base_ally)
                print(f'Utworzono BattleCharacters:')
                for character in self.battle_ally:
                    print(f'- {character.name}')


                # characterviews creation
                view_list = CharacterView.create_character_view(self.battle_ally)
                print(f'stworzono CharacterView {view_list}')

                emit_signal = pygame.event.Event(BattleLogic.SHUFFLE_DECK_SIGNAL, {"event": "SHUFFLE_DECK_SIGNAL", "subtype": "INITIAL"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.SignalEmit(self, emit_signal, "BL0->CM1")
                return

            # BATTLE_LOGIC FLOW
            # BL1
            if signal.type == BattleLogic.SHUFFLE_DECK_RESPONSE and signal.subtype == "INITIAL" or \
                    signal.type == BattleLogic.BATTLE_LOGIC_SIGNAL and signal.subtype == "END_TURN":

                if signal.type == BattleLogic.SHUFFLE_DECK_RESPONSE and signal.subtype == "INITIAL":
                    Logs.DebugMessage.SignalReceived(self, signal, "BL1<-CM1")
                if signal.type == BattleLogic.BATTLE_LOGIC_SIGNAL and signal.subtype == "END_TURN":
                    Logs.DebugMessage.SignalReceived(self, signal, "BL1<-?BL101")

                Logs.InfoMessage.SimpleInfo(self, "NASTĘPNA POSTAĆ")
                emit_signal = pygame.event.Event(BattleLogic.QUEUE_MODEL_SIGNAL, {"event": "QUEUE_MODEL_SIGNAL", "subtype": "STANDARD"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.SignalEmit(self, emit_signal, "BL1->QM1")
                return

            # BL2
            if signal.type == BattleLogic.QUEUE_MODEL_RESPONSE and signal.subtype == "STANDARD":
                Logs.DebugMessage.SignalReceived(self, signal, "BL2<-QM1")

                emit_signal = pygame.event.Event(BattleLogic.ACTION_MODEL_SIGNAL, {"event": "ACTION_MODEL_SIGNAL", "subtype": "PRE_TURN"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.SignalEmit(self, emit_signal, "BL2->AM1")
                return

            # LOOP (DRAW)
            # BL3
            if signal.type == BattleLogic.ACTION_MODEL_RESPONSE and signal.subtype == "PRE_TURN" or \
                    signal.type == BattleLogic.ACTION_MODEL_RESPONSE and signal.subtype == "POST_DRAW":

                if signal.type == BattleLogic.ACTION_MODEL_RESPONSE and signal.subtype == "PRE_TURN":
                    Logs.DebugMessage.SignalReceived(self, signal, "BL3<-AM1")
                if signal.type == BattleLogic.ACTION_MODEL_RESPONSE and signal.subtype == "POST_DRAW":
                    Logs.DebugMessage.SignalReceived(self, signal, "BL3<-AM3")

                # IF Czy dobiera kartę?
                Logs.InfoMessage.SimpleInfo(self, "CZY DOBIERA KARTĘ?")
                draw = False
                if draw:
                    # TAK
                    Logs.InfoMessage.SimpleInfo(self, "TAK")
                    Logs.InfoMessage.SimpleInfo(self, "[START LOOP DRAW]")

                    emit_signal = pygame.event.Event(BattleLogic.BATTLE_LOGIC_SIGNAL, {"event": "BATTLE_LOGIC_SIGNAL", "subtype": "NEED_DRAW"})
                    pygame.event.post(emit_signal)
                    Logs.DebugMessage.SignalEmit(self, emit_signal, "BL3->BL3A")
                    return
                else:
                    # NIE
                    Logs.InfoMessage.SimpleInfo(self, "NIE")
                    Logs.InfoMessage.SimpleInfo(self, "[END LOOP DRAW]")

                    emit_signal = pygame.event.Event(BattleLogic.BATTLE_LOGIC_SIGNAL, {"event": "BATTLE_LOGIC_SIGNAL", "subtype": "END_DRAW"})
                    pygame.event.post(emit_signal)
                    Logs.DebugMessage.SignalEmit(self, emit_signal, "BL3->BL7")
                    return

            # BL3A
            if signal.type == BattleLogic.BATTLE_LOGIC_SIGNAL and signal.subtype == "NEED_DRAW":
                Logs.DebugMessage.SignalReceived(self, signal, "BL3A<-BL3")

                # IF Czy postać ma karty w DrawPile?:
                Logs.InfoMessage.SimpleInfo(self, "CZY POSTAĆ MA KARTY W DRAW PILE?")
                answer = False
                if answer:
                    Logs.InfoMessage.SimpleInfo(self, "NIE")

                    emit_signal = pygame.event.Event(BattleLogic.SHUFFLE_DECK_SIGNAL, {"event": "SHUFFLE_DECK_SIGNAL", "subtype": "STANDARD"})
                    pygame.event.post(emit_signal)
                    Logs.DebugMessage.SignalEmit(self, emit_signal, "BL3A->CM2")
                    return
                else:
                    Logs.InfoMessage.SimpleInfo(self, "TAK")

                    emit_signal = pygame.event.Event(BattleLogic.BATTLE_LOGIC_SIGNAL, {"event": "BATTLE_LOGIC_SIGNAL", "subtype": "NO_SHUFFLE"})
                    pygame.event.post(emit_signal)
                    Logs.DebugMessage.SignalEmit(self, emit_signal, "BL3A->BL4")
                    return

            # BL4
            if signal.type == BattleLogic.SHUFFLE_DECK_RESPONSE and signal.subtype == "STANDARD" or \
                    signal.type == BattleLogic.BATTLE_LOGIC_SIGNAL and signal.subtype == "NO_SHUFFLE":

                if signal.type == BattleLogic.SHUFFLE_DECK_RESPONSE and signal.subtype == "STANDARD":
                    Logs.DebugMessage.SignalReceived(self, signal, "BL4<-CM2")
                if signal.type == BattleLogic.BATTLE_LOGIC_SIGNAL and signal.subtype == "NO_SHUFFLE":
                    Logs.DebugMessage.SignalReceived(self, signal, "BL4<-BL3A")

                emit_signal = pygame.event.Event(BattleLogic.ACTION_MODEL_SIGNAL, {"event": "ACTION_MODEL_SIGNAL", "subtype": "PRE_DRAW"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.SignalEmit(self, emit_signal, "BL4->AM2")
                return

            # BL5
            if signal.type == BattleLogic.ACTION_MODEL_RESPONSE and signal.subtype == "PRE_DRAW":
                Logs.DebugMessage.SignalReceived(self, signal, "BL5<-AM2")

                emit_signal = pygame.event.Event(BattleLogic.DRAW_CARD_SIGNAL, {"event": "DRAW_CARD_SIGNAL", "subtype": "STANDARD"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.SignalEmit(self, emit_signal, "BL5->CM3")
                return

            # BL6
            if signal.type == BattleLogic.DRAW_CARD_RESPONSE and signal.subtype == "STANDARD":
                Logs.DebugMessage.SignalReceived(self, signal, "BL6<-CM3")

                emit_signal = pygame.event.Event(BattleLogic.ACTION_MODEL_SIGNAL, {"event": "ACTION_MODEL_SIGNAL", "subtype": "POST_DRAW"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.SignalEmit(self, emit_signal, "BL6->AM3")
                return

            # BL7
            if signal.type == BattleLogic.BATTLE_LOGIC_SIGNAL and signal.subtype == "END_DRAW":
                Logs.DebugMessage.SignalReceived(self, signal, "BL7<-BL3")

                # IF Czy jest tura AI?:
                Logs.InfoMessage.SimpleInfo(self, "CZY JEST TURA AI?")
                answer=True
                if answer:
                    Logs.InfoMessage.SimpleInfo(self, "NIE")

                    emit_signal = pygame.event.Event(BattleLogic.BATTLE_LOGIC_SIGNAL, {"event": "BATTLE_LOGIC_SIGNAL", "subtype": "PLAYER_TURN"})
                    pygame.event.post(emit_signal)
                    Logs.DebugMessage.SignalEmit(self, emit_signal, "BL7->BL8")
                    return

                else:
                    return

            # PLAYER TURN
            # BL8
            if signal.type == BattleLogic.BATTLE_LOGIC_SIGNAL and signal.subtype == "PLAYER_TURN" or \
                    signal.type == BattleLogic.ACTION_MODEL_RESPONSE and signal.subtype == "POST_ACTION":

                if signal.type == BattleLogic.BATTLE_LOGIC_SIGNAL and signal.subtype == "PLAYER_TURN":
                    Logs.DebugMessage.SignalReceived(self, signal, "BL8<-BL7")
                if signal.type == BattleLogic.ACTION_MODEL_RESPONSE and signal.subtype == "POST_ACTION":
                    Logs.DebugMessage.SignalReceived(self, signal, "BL8<-AM5")

                # IF Czy postać może wykonać akcję?:
                Logs.InfoMessage.SimpleInfo(self, "CZY POSTAĆ MOŻE WYKONAĆ AKCJĘ?")
                answer = True
                if answer:
                    Logs.InfoMessage.SimpleInfo(self, "TAK")

                    emit_signal = pygame.event.Event(BattleLogic.BATTLE_LOGIC_SIGNAL, {"event": "BATTLE_LOGIC_SIGNAL", "subtype": "PLAYER_ACTION"})
                    pygame.event.post(emit_signal)
                    Logs.DebugMessage.SignalEmit(self, emit_signal, "BL8->BL9")
                    return

                else:
                    Logs.InfoMessage.SimpleInfo(self, "NIE")

                    emit_signal = pygame.event.Event(BattleLogic.BATTLE_LOGIC_SIGNAL, {"event": "BATTLE_LOGIC_SIGNAL", "subtype": "PLAYER_NO_ACTION"})
                    pygame.event.post(emit_signal)
                    Logs.DebugMessage.SignalEmit(self, emit_signal, "BL8->?BL100")
                    return

            # PLAYER ACTION
            # BL9
            if signal.type == BattleLogic.BATTLE_LOGIC_SIGNAL and signal.subtype == "PLAYER_ACTION":
                Logs.DebugMessage.SignalReceived(self, signal, "BL9<-BL8")

                # Wybór czy używamy kartę czy przedmiot.
                Logs.InfoMessage.SimpleInfo(self, "WYBIERZ KARTĘ LUB PRZEDMIOT")
                card = True
                item = False
                if card:
                    Logs.InfoMessage.SimpleInfo(self, "UŻYTA KARTA")
                    emit_signal = pygame.event.Event(BattleLogic.CARD_MODEL_SIGNAL, {"event": "CARD_MODEL_SIGNAL", "subtype": "STANDARD"})
                    pygame.event.post(emit_signal)
                    Logs.DebugMessage.SignalEmit(self, emit_signal, "BL9->CM4")
                    return

                # Nie ma ItemModel
                if item:
                    Logs.InfoMessage.SimpleInfo(self, "UŻYTY PRZEDMIOT")
                    emit_signal = pygame.event.Event(BattleLogic.ITEM_MODEL_SIGNAL, {"event": "ITEM_MODEL_SIGNAL", "subtype": "STANDARD"})
                    pygame.event.post(emit_signal)
                    Logs.DebugMessage.SignalEmit(self, emit_signal, "BL9->IM1")
                    return

            # BL12
            if signal.type == BattleLogic.CARD_MODEL_RESPONSE and signal.subtype == "STANDARD" or \
                    signal.type == BattleLogic.ITEM_MODEL_RESPONSE and signal.subtype == "STANDARD":

                if signal.type == BattleLogic.CARD_MODEL_RESPONSE and signal.subtype == "STANDARD":
                    Logs.DebugMessage.SignalReceived(self, signal, "BL12<-CM4")
                if signal.type == BattleLogic.ITEM_MODEL_RESPONSE and signal.subtype == "STANDARD":
                    Logs.DebugMessage.SignalReceived(self, signal, "BL12<-IM1")

                emit_signal = pygame.event.Event(BattleLogic.CHARACTER_MODEL_SIGNAL, {"event": "CHARACTER_MODEL_SIGNAL", "subtype": "STANDARD"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.SignalEmit(self, emit_signal, "BL12->CM1")
                return

            # BL13
            if signal.type == BattleLogic.CHARACTER_MODEL_RESPONSE and signal.subtype == "STANDARD":
                Logs.DebugMessage.SignalReceived(self, signal, "BL13<-ChM1")

                emit_signal = pygame.event.Event(BattleLogic.ACTION_MODEL_SIGNAL, {"event": "ACTION_MODEL_SIGNAL", "subtype": "STANDARD"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.SignalEmit(self, emit_signal, "BL13->AM4")
                return

            # BL14
            if signal.type == BattleLogic.ACTION_MODEL_RESPONSE and signal.subtype == "STANDARD":
                Logs.DebugMessage.SignalReceived(self, signal, "BL14<-AM4")

                emit_signal = pygame.event.Event(BattleLogic.ACTION_MODEL_SIGNAL, {"event": "ACTION_MODEL_SIGNAL", "subtype": "POST_ACTION"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.SignalEmit(self, emit_signal, "BL14->AM5")
                return

            # ?BL100
            if signal.type == BattleLogic.BATTLE_LOGIC_SIGNAL and signal.subtype == "PLAYER_NO_ACTION":
                Logs.DebugMessage.SignalReceived(self, signal, "?BL100<-BL8")

                emit_signal = pygame.event.Event(BattleLogic.ACTION_MODEL_SIGNAL, {"event": "ACTION_MODEL_SIGNAL", "subtype": "POST_TURN"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.SignalEmit(self, emit_signal, "?#BL100->?AM100")
                return

            # ?BL101
            if signal.type == BattleLogic.ACTION_MODEL_RESPONSE and signal.subtype == "POST_TURN":
                Logs.DebugMessage.SignalReceived(self, signal, "?BL101<-?AM100")

                # IF Czy walka zakończona?:
                Logs.InfoMessage.SimpleInfo(self, "CZY WALKA ZAKOŃCZONA?")

                answer = False
                if answer:
                    Logs.InfoMessage.SimpleInfo(self, "TAK")

                    emit_signal = pygame.event.Event(BattleLogic.BATTLE_LOGIC_SIGNAL, {"event": "BATTLE_LOGIC_SIGNAL", "subtype": "END_BATTLE"})
                    pygame.event.post(emit_signal)
                    Logs.DebugMessage.SignalEmit(self, emit_signal, "?BL101->!!!END BATTLE!!!")
                    return

                else:
                    Logs.InfoMessage.SimpleInfo(self, "NIE")

                    emit_signal = pygame.event.Event(BattleLogic.BATTLE_LOGIC_SIGNAL, {"event": "BATTLE_LOGIC_SIGNAL", "subtype": "END_TURN"})
                    pygame.event.post(emit_signal)
                    Logs.DebugMessage.SignalEmit(self, emit_signal, "?BL101->BL1")
                    return

