import pygame

from property.initialize_property import InitializeProperty, InitializeState
from resource_manager.resource_manager import ResourceManager
from scene_creator.scene_creator import SceneCreator

from assets.lib.battle_system.battle_character_utilities.battle_character_model import BattleCharacter
from assets.lib.card_utilities.card_manager import CardManager
from assets.lib.battle_system.log import Logs
from assets.lib.game_object_shared_resource import GameObjectSharedResource
from assets.lib.project_controller.project_controller import ProjectController


class BattleLogic(GameObjectSharedResource):

    BATTLE_LOGIC_SIGNAL = pygame.event.custom_type()

    QUEUE_CONTROLLER_SIGNAL = pygame.event.custom_type()
    ACTION_CONTROLLER_SIGNAL = pygame.event.custom_type()
    SHUFFLE_DECK_SIGNAL = pygame.event.custom_type()
    DRAW_CARD_SIGNAL = pygame.event.custom_type()
    CARD_CONTROLLER_SIGNAL = pygame.event.custom_type()
    ITEM_CONTROLLER_SIGNAL = pygame.event.custom_type()
    CHARACTER_CONTROLLER_SIGNAL = pygame.event.custom_type()
    CHARACTER_VIEW_CONTROLLER_SIGNAL = pygame.event.custom_type()
    AI_CONTROLLER_SIGNAL = pygame.event.custom_type()

    QUEUE_CONTROLLER_RESPONSE = pygame.event.custom_type()
    ACTION_CONTROLLER_RESPONSE = pygame.event.custom_type()
    SHUFFLE_DECK_RESPONSE = pygame.event.custom_type()
    DRAW_CARD_RESPONSE = pygame.event.custom_type()
    CARD_CONTROLLER_RESPONSE = pygame.event.custom_type()
    ITEM_CONTROLLER_RESPONSE = pygame.event.custom_type()
    CHARACTER_CONTROLLER_RESPONSE = pygame.event.custom_type()
    CHARACTER_VIEW_CONTROLLER_RESPONSE = pygame.event.custom_type()
    AI_CONTROLLER_RESPONSE = pygame.event.custom_type()

    CHARACTER_VIEW_SIGNAL = pygame.event.custom_type()
    CHARACTER_VIEW_RESPONSE = pygame.event.custom_type()

    BATTLE_LOST = pygame.event.custom_type()
    BATTLE_WON = pygame.event.custom_type()

    character_model_active = False
    card_model_active = False
    turn_model_active = False

    _initialized = False
    started = False

    def __init__(self):
        super(BattleLogic, self).__init__()

        self.queue_model = None

    def _initialize(self):

        if InitializeProperty.check_is_ready(self, InitializeState.NOT_INITIALIZED):
            super(BattleLogic, self)._initialize()

            # Load Card Assets from card_assets package
            SceneCreator._scene = "card_assets"
            SceneCreator.load_entity_config(SceneCreator._scene)
            SceneCreator.load_resource_config(SceneCreator._scene)
            scene_config = SceneCreator.get_scene_resources_config(SceneCreator._scene)
            ResourceManager.load_resources(scene_config)
            SceneCreator._scene = "battle_scene"

            InitializeProperty.initialize_enable(self)
            Logs.InfoMessage.simple_info(self, "BattleLogic Initialized [ OK ]")

            return

        if InitializeProperty.check_is_ready(self, InitializeState.STARTED):
            self.property('ScriptProperty').property_enable()
            self.property('EventProperty').property_enable()
            self.property('SignalProperty').property_enable()
            # InitializeProperty.started(self)
            self.property('InitializeProperty').property_disable()

            return

    def on_script(self):

        print(f'BATTLE_LOGIC:EMIT_SIGNAL: "event": "BATTLE_LOGIC_SIGNAL", "subtype": "INITIAL"')
        signal = pygame.event.Event(BattleLogic.BATTLE_LOGIC_SIGNAL, {"event": "BATTLE_LOGIC_SIGNAL", "subtype": "INITIAL"})
        pygame.event.post(signal)

        self.property('ScriptProperty').property_disable()

    def on_event(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                pass

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_s:
                    emit_signal = pygame.event.Event(ProjectController.START_CHARACTER_SHEET_SCENE_TIME_EVENT)
                    pygame.event.post(emit_signal)
                    return

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_c:
                emit_signal = pygame.event.Event(ProjectController.START_CARD_COLLECTION_SCENE_TIME_EVENT)
                pygame.event.post(emit_signal)
                return

    def on_signal(self, signal):

            # BATTLE_LOGIC INITIAL
            # BLS1
            if signal.type == BattleLogic.BATTLE_LOGIC_SIGNAL and signal.subtype == "INITIAL":
                Logs.DebugMessage.signal_received(self, signal, "BLS1<-INIT")

                Logs.InfoMessage.simple_info(self, "<START SETUP>")
                # BattleCharacters creation

                self.battle_ally = BattleCharacter.create_character_models(self._base_ally)
                print(f'Utworzono BattleCharacters:')
                for character in self.battle_ally:
                    print(f'- {character.name}')

                self.battle_enemies = BattleCharacter.create_character_models(self._base_enemies)
                print(f'Utworzono BattleCharacters:')
                for character in self.battle_enemies:
                    print(f'- {character.name}')

                # # Create CharacterViews and register in BattleCharacterViewManager
                # for battle_character in self.battle_ally + self.battle_enemies:
                #     battle_character_view = BattleCharacterView(battle_character)
                #     BattleCharacterViewManager.register(battle_character_view)

                # Populating battle_decks by BaseCards instances
                for character in (self.battle_ally + self.battle_enemies):
                    for card_id, amount in character.deck.items():
                        for i in range(0, amount):
                            basic_card = CardManager.create_base_card(card_id)
                            character.battle_deck.append(basic_card)
                            # Populating draw_pile as a working copy of battle_deck
                            character.draw_pile = character.battle_deck.copy()

                emit_signal = pygame.event.Event(BattleLogic.CHARACTER_VIEW_CONTROLLER_SIGNAL, {"event": "CHARACTER_VIEW_CONTROLLER_SIGNAL", "subtype": "INITIAL"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.signal_emit(self, emit_signal, "BLS1->BChVMS1")

                InitializeProperty.started(self)
                Logs.InfoMessage.simple_info(self, "BattleLogic Started [ OK ]")
                return

            # BLS2
            if signal.type == BattleLogic.CHARACTER_VIEW_CONTROLLER_RESPONSE and signal.subtype == "INITIAL":
                Logs.DebugMessage.signal_received(self, signal, "BLS2<-BChVMS1")

                emit_signal = pygame.event.Event(BattleLogic.QUEUE_CONTROLLER_SIGNAL, {"event": "QUEUE_CONTROLLER_SIGNAL", "subtype": "INITIAL"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.signal_emit(self, emit_signal, "BLS2->QCS1")
                return

            # BLS3
            if signal.type == BattleLogic.QUEUE_CONTROLLER_RESPONSE and signal.subtype == "INITIAL":
                Logs.DebugMessage.signal_received(self, signal, "BLS3<-QCS1")

                emit_signal = pygame.event.Event(BattleLogic.SHUFFLE_DECK_SIGNAL, {"event": "SHUFFLE_DECK_SIGNAL", "subtype": "INITIAL"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.signal_emit(self, emit_signal, "BLS3->CCS1")
                return

            # BLS4
            if signal.type == BattleLogic.SHUFFLE_DECK_RESPONSE and signal.subtype == "INITIAL":
                Logs.DebugMessage.signal_received(self, signal, "BL1<-CCS1")

                emit_signal = pygame.event.Event(BattleLogic.AI_CONTROLLER_SIGNAL, {"event": "AI_CONTROLLER_SIGNAL", "subtype": "INITIAL"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.signal_emit(self, emit_signal, "BLS4->AICS1")
                return

            # BATTLE_LOGIC TURN FLOW
            # BL1
            if signal.type == BattleLogic.AI_CONTROLLER_RESPONSE and signal.subtype == "INITIAL" or \
                    signal.type == BattleLogic.BATTLE_LOGIC_SIGNAL and signal.subtype == "END_TURN":

                if signal.type == BattleLogic.AI_CONTROLLER_RESPONSE and signal.subtype == "INITIAL":
                    Logs.DebugMessage.signal_received(self, signal, "BL1<-AICS1")
                    Logs.InfoMessage.simple_info(self, "<FINISH SETUP>")
                if signal.type == BattleLogic.BATTLE_LOGIC_SIGNAL and signal.subtype == "END_TURN":
                    Logs.DebugMessage.signal_received(self, signal, "BL1<-?BL101")

                Logs.InfoMessage.simple_info(self, "NASTĘPNA POSTAĆ")
                emit_signal = pygame.event.Event(BattleLogic.QUEUE_CONTROLLER_SIGNAL, {"event": "QUEUE_CONTROLLER_SIGNAL", "subtype": "STANDARD"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.signal_emit(self, emit_signal, "BL1->QC1")
                return

            # BL2
            if signal.type == BattleLogic.QUEUE_CONTROLLER_RESPONSE and signal.subtype == "STANDARD":
                Logs.DebugMessage.signal_received(self, signal, "BL2<-QC1")

                emit_signal = pygame.event.Event(BattleLogic.ACTION_CONTROLLER_SIGNAL, {"event": "ACTION_CONTROLLER_SIGNAL", "subtype": "PRE_TURN"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.signal_emit(self, emit_signal, "BL2->AC1")
                return

            # LOOP (DRAW)
            # BL3
            if signal.type == BattleLogic.ACTION_CONTROLLER_RESPONSE and signal.subtype == "PRE_TURN" or \
                    signal.type == BattleLogic.ACTION_CONTROLLER_RESPONSE and signal.subtype == "POST_DRAW":

                if signal.type == BattleLogic.ACTION_CONTROLLER_RESPONSE and signal.subtype == "PRE_TURN":
                    Logs.DebugMessage.signal_received(self, signal, "BL3<-AC1")
                if signal.type == BattleLogic.ACTION_CONTROLLER_RESPONSE and signal.subtype == "POST_DRAW":
                    Logs.DebugMessage.signal_received(self, signal, "BL3<-AC3")

                # IF Czy dobiera kartę?
                Logs.InfoMessage.simple_info(self, "CZY DOBIERA KARTĘ?")
                if len(self.current_character.hand) < self.current_character.card_draw:
                    # TAK
                    Logs.InfoMessage.simple_info(self, "TAK")
                    Logs.InfoMessage.simple_info(self, "[START LOOP DRAW]")

                    emit_signal = pygame.event.Event(BattleLogic.BATTLE_LOGIC_SIGNAL, {"event": "BATTLE_LOGIC_SIGNAL", "subtype": "NEED_DRAW"})
                    pygame.event.post(emit_signal)
                    Logs.DebugMessage.signal_emit(self, emit_signal, "BL3->BL3A")
                    return
                else:
                    # NIE
                    Logs.InfoMessage.simple_info(self, "NIE")
                    Logs.InfoMessage.simple_info(self, "[END LOOP DRAW]")

                    emit_signal = pygame.event.Event(BattleLogic.BATTLE_LOGIC_SIGNAL, {"event": "BATTLE_LOGIC_SIGNAL", "subtype": "END_DRAW"})
                    pygame.event.post(emit_signal)
                    Logs.DebugMessage.signal_emit(self, emit_signal, "BL3->BL7")
                    return

            # BL3A
            if signal.type == BattleLogic.BATTLE_LOGIC_SIGNAL and signal.subtype == "NEED_DRAW":
                Logs.DebugMessage.signal_received(self, signal, "BL3A<-BL3")

                # IF Czy postać ma karty w DrawPile?:
                Logs.InfoMessage.simple_info(self, "CZY POSTAĆ MA KARTY W DRAW PILE?")
                if len(self.current_character.draw_pile) < 1:
                    Logs.InfoMessage.simple_info(self, "NIE")

                    emit_signal = pygame.event.Event(BattleLogic.SHUFFLE_DECK_SIGNAL, {"event": "SHUFFLE_DECK_SIGNAL", "subtype": "STANDARD"})
                    pygame.event.post(emit_signal)
                    Logs.DebugMessage.signal_emit(self, emit_signal, "BL3A->CC2")
                    return
                if len(self.current_character.draw_pile) >= 1:
                    Logs.InfoMessage.simple_info(self, "TAK")

                    emit_signal = pygame.event.Event(BattleLogic.BATTLE_LOGIC_SIGNAL, {"event": "BATTLE_LOGIC_SIGNAL", "subtype": "NO_SHUFFLE"})
                    pygame.event.post(emit_signal)
                    Logs.DebugMessage.signal_emit(self, emit_signal, "BL3A->BL4")
                    return

            # BL4
            if signal.type == BattleLogic.SHUFFLE_DECK_RESPONSE and signal.subtype == "STANDARD" or \
                    signal.type == BattleLogic.BATTLE_LOGIC_SIGNAL and signal.subtype == "NO_SHUFFLE":

                if signal.type == BattleLogic.SHUFFLE_DECK_RESPONSE and signal.subtype == "STANDARD":
                    Logs.DebugMessage.signal_received(self, signal, "BL4<-CC2")
                if signal.type == BattleLogic.BATTLE_LOGIC_SIGNAL and signal.subtype == "NO_SHUFFLE":
                    Logs.DebugMessage.signal_received(self, signal, "BL4<-BL3A")

                emit_signal = pygame.event.Event(BattleLogic.ACTION_CONTROLLER_SIGNAL, {"event": "ACTION_CONTROLLER_SIGNAL", "subtype": "PRE_DRAW"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.signal_emit(self, emit_signal, "BL4->AC2")
                return

            # BL5
            if signal.type == BattleLogic.ACTION_CONTROLLER_RESPONSE and signal.subtype == "PRE_DRAW":
                Logs.DebugMessage.signal_received(self, signal, "BL5<-AC2")

                emit_signal = pygame.event.Event(BattleLogic.DRAW_CARD_SIGNAL, {"event": "DRAW_CARD_SIGNAL", "subtype": "STANDARD"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.signal_emit(self, emit_signal, "BL5->CC3")
                return

            # BL6
            if signal.type == BattleLogic.DRAW_CARD_RESPONSE and signal.subtype == "STANDARD":
                Logs.DebugMessage.signal_received(self, signal, "BL6<-CC3")

                emit_signal = pygame.event.Event(BattleLogic.ACTION_CONTROLLER_SIGNAL, {"event": "ACTION_CONTROLLER_SIGNAL", "subtype": "POST_DRAW"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.signal_emit(self, emit_signal, "BL6->AC3")
                return

            # BL7
            if signal.type == BattleLogic.BATTLE_LOGIC_SIGNAL and signal.subtype == "END_DRAW" or \
                    signal.type == BattleLogic.ACTION_CONTROLLER_RESPONSE and signal.subtype == "POST_ACTION":
                Logs.DebugMessage.signal_received(self, signal, "BL7<-BL3")
                # IF Czy postać może wykonać akcję?:
                Logs.InfoMessage.simple_info(self, "CZY POSTAĆ MOŻE WYKONAĆ AKCJĘ?")

                if self.current_character.battle_attribute("action_points") > 0:
                    Logs.InfoMessage.simple_info(self, "TAK")

                    emit_signal = pygame.event.Event(BattleLogic.BATTLE_LOGIC_SIGNAL, {"event": "BATTLE_LOGIC_SIGNAL", "subtype": "ACTION_EXECUTION"})
                    pygame.event.post(emit_signal)
                    Logs.DebugMessage.signal_emit(self, emit_signal, "BL7->BL8")
                    return

                else:
                    Logs.InfoMessage.simple_info(self, "NIE")

                    emit_signal = pygame.event.Event(BattleLogic.BATTLE_LOGIC_SIGNAL, {"event": "BATTLE_LOGIC_SIGNAL", "subtype": "NO_ACTION"})
                    pygame.event.post(emit_signal)
                    Logs.DebugMessage.signal_emit(self, emit_signal, "BL8->?BL100")
                    return

            # BL8
            if signal.type == BattleLogic.BATTLE_LOGIC_SIGNAL and signal.subtype == "ACTION_EXECUTION":
                Logs.DebugMessage.signal_received(self, signal, "BL8<-BL7")

                # IF Czy jest tura AI?:
                Logs.InfoMessage.simple_info(self, "CZY JEST TURA AI?")
                # answer = True
                if not self.current_character.character_type == "npc":
                # if not answer:
                    Logs.InfoMessage.simple_info(self, "NIE")

                    emit_signal = pygame.event.Event(BattleLogic.BATTLE_LOGIC_SIGNAL, {"event": "BATTLE_LOGIC_SIGNAL", "subtype": "PLAYER_ACTION"})
                    pygame.event.post(emit_signal)
                    Logs.DebugMessage.signal_emit(self, emit_signal, "BL8->BL9")
                    return

                else:
                    Logs.InfoMessage.simple_info(self, "TAK")

                    emit_signal = pygame.event.Event(BattleLogic.AI_CONTROLLER_SIGNAL, {"event": "AI_CONTROLLER_SIGNAL", "subtype": "STANDARD"})
                    pygame.event.post(emit_signal)
                    Logs.DebugMessage.signal_emit(self, emit_signal, "BL8->AIC1")

                    return

            # PLAYER ACTION
            # BL9
            if signal.type == BattleLogic.BATTLE_LOGIC_SIGNAL and signal.subtype == "PLAYER_ACTION":
                Logs.DebugMessage.signal_received(self, signal, "BL9<-BL8")

                # Wybór czy używamy kartę czy przedmiot.
                Logs.InfoMessage.simple_info(self, "WYBIERZ KARTĘ LUB PRZEDMIOT")
                card = True
                item = False
                if card:
                    Logs.InfoMessage.simple_info(self, "UŻYTA KARTA")
                    emit_signal = pygame.event.Event(BattleLogic.CARD_CONTROLLER_SIGNAL, {"event": "CARD_CONTROLLER_SIGNAL", "subtype": "STANDARD"})
                    pygame.event.post(emit_signal)
                    Logs.DebugMessage.signal_emit(self, emit_signal, "BL9->CC4")
                    return

                # Nie ma ItemController
                if item:
                    Logs.InfoMessage.simple_info(self, "UŻYTY PRZEDMIOT")
                    emit_signal = pygame.event.Event(BattleLogic.ITEM_CONTROLLER_SIGNAL, {"event": "ITEM_CONTROLLER_SIGNAL", "subtype": "STANDARD"})
                    pygame.event.post(emit_signal)
                    Logs.DebugMessage.signal_emit(self, emit_signal, "BL9->IC1")
                    return

            # BL12
            if signal.type == BattleLogic.CARD_CONTROLLER_RESPONSE and signal.subtype == "STANDARD" or \
                    signal.type == BattleLogic.ITEM_CONTROLLER_RESPONSE and signal.subtype == "STANDARD":

                if signal.type == BattleLogic.CARD_CONTROLLER_RESPONSE and signal.subtype == "STANDARD":
                    Logs.DebugMessage.signal_received(self, signal, "BL12<-CC4")
                if signal.type == BattleLogic.ITEM_CONTROLLER_RESPONSE and signal.subtype == "STANDARD":
                    Logs.DebugMessage.signal_received(self, signal, "BL12<-IC1")

                emit_signal = pygame.event.Event(BattleLogic.CHARACTER_CONTROLLER_SIGNAL, {"event": "CHARACTER_CONTROLLER_SIGNAL", "subtype": "STANDARD"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.signal_emit(self, emit_signal, "BL12->ChC1")
                return

            # BL13
            if signal.type == BattleLogic.CHARACTER_CONTROLLER_RESPONSE and signal.subtype == "STANDARD" or \
                    signal.type == BattleLogic.AI_CONTROLLER_RESPONSE and signal.subtype == "STANDARD":

                if signal.type == BattleLogic.CHARACTER_CONTROLLER_RESPONSE and signal.subtype == "STANDARD":
                    Logs.DebugMessage.signal_received(self, signal, "BL13<-ChC1")
                if signal.type == BattleLogic.AI_CONTROLLER_RESPONSE and signal.subtype == "STANDARD":
                    Logs.DebugMessage.signal_received(self, signal, "BL13<-AIC1")


                emit_signal = pygame.event.Event(BattleLogic.ACTION_CONTROLLER_SIGNAL, {"event": "ACTION_CONTROLLER_SIGNAL", "subtype": "STANDARD"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.signal_emit(self, emit_signal, "BL13->AC4")
                return

            # BL14
            if signal.type == BattleLogic.ACTION_CONTROLLER_RESPONSE and signal.subtype == "STANDARD":
                Logs.DebugMessage.signal_received(self, signal, "BL14<-AC4")

                emit_signal = pygame.event.Event(BattleLogic.ACTION_CONTROLLER_SIGNAL, {"event": "ACTION_CONTROLLER_SIGNAL", "subtype": "POST_ACTION"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.signal_emit(self, emit_signal, "BL14->AC5")
                return

            # ?BL100
            if signal.type == BattleLogic.BATTLE_LOGIC_SIGNAL and signal.subtype == "NO_ACTION":
                Logs.DebugMessage.signal_received(self, signal, "?BL100<-BL8")

                emit_signal = pygame.event.Event(BattleLogic.ACTION_CONTROLLER_SIGNAL, {"event": "ACTION_CONTROLLER_SIGNAL", "subtype": "POST_TURN"})
                pygame.event.post(emit_signal)
                Logs.DebugMessage.signal_emit(self, emit_signal, "?#BL100->?AC100")
                return

            # ?BL101
            if signal.type == BattleLogic.ACTION_CONTROLLER_RESPONSE and signal.subtype == "POST_TURN" or \
                    signal.type == BattleLogic.BATTLE_LOST and signal.subtype == "STANDARD" or \
                    signal.type == BattleLogic.BATTLE_WON and signal.subtype == "STANDARD":

                if signal.type == BattleLogic.ACTION_CONTROLLER_RESPONSE and signal.subtype == "POST_TURN":
                    Logs.DebugMessage.signal_received(self, signal, "?BL101<-?AC100")
                if signal.type == BattleLogic.BATTLE_LOST and signal.subtype == "STANDARD":
                    Logs.DebugMessage.signal_received(self, signal, "?BL101<-?ActionProcess: battle_lost")
                if signal.type == BattleLogic.BATTLE_WON and signal.subtype == "STANDARD":
                    Logs.DebugMessage.signal_received(self, signal, "?BL101<-?ActionProcess: battle_won")

                # IF Czy walka zakończona?:
                Logs.InfoMessage.simple_info(self, "CZY WALKA ZAKOŃCZONA?")

                if signal.type == BattleLogic.BATTLE_LOST and signal.subtype == "STANDARD" or \
                        signal.type == BattleLogic.BATTLE_WON and signal.subtype == "STANDARD":
                    Logs.InfoMessage.simple_info(self, "TAK")

                    emit_signal = pygame.event.Event(BattleLogic.BATTLE_LOGIC_SIGNAL, {"event": "BATTLE_LOGIC_SIGNAL", "subtype": "DESTROY_VIEW"})
                    pygame.event.post(emit_signal)
                    Logs.DebugMessage.signal_emit(self, emit_signal, "?BL101->BChVC2")

                    if signal.type == BattleLogic.BATTLE_LOST and signal.subtype == "STANDARD":

                        # pygame.time.set_timer(ProjectController.UNLOAD_BATTLE_SCENE_TIME_EVENT, 1)

                        emit_signal = pygame.event.Event(ProjectController.START_END_SCENE_TIME_EVENT, {"event": "START_END_SCENE_TIME_EVENT", "subtype": "BATTLE_LOST"})
                        pygame.event.post(emit_signal)
                        return

                    elif signal.type == BattleLogic.BATTLE_WON and signal.subtype == "STANDARD":

                        # pygame.time.set_timer(ProjectController.UNLOAD_BATTLE_SCENE_TIME_EVENT, 1)

                        emit_signal = pygame.event.Event(ProjectController.START_BATTLE_SUMMARY_SCENE_TIME_EVENT, {"event": "START_BATTLE_SUMMARY_SCENE_TIME_EVENT", "subtype": "BATTLE_WON"})
                        pygame.event.post(emit_signal)
                        return

                else:
                    Logs.InfoMessage.simple_info(self, "NIE")

                    emit_signal = pygame.event.Event(BattleLogic.BATTLE_LOGIC_SIGNAL, {"event": "BATTLE_LOGIC_SIGNAL", "subtype": "END_TURN"})
                    pygame.event.post(emit_signal)
                    Logs.DebugMessage.signal_emit(self, emit_signal, "?BL101->BL1")
                    return

