import asyncio
import json
from collections import Counter
from datetime import date, datetime, timezone

import pytest
from asgi_lifespan import LifespanManager
from bson import ObjectId
from fastapi.testclient import TestClient
from httpx import AsyncClient
from scooze.card import OracleCard
from scooze.catalogs import Format, Legality
from scooze.config import CONFIG
from scooze.deck import Deck
from scooze.deckpart import DeckPart
from scooze.models.card import CardModel, CardModelData
from scooze.mongo import db

# Override config for testing
CONFIG.testing = True
CONFIG.mongo_db = "scooze_test"

from scooze.main import app

# These fixtures can be used in any tests in this directory.
# https://www.mtggoldfish.com/archetype/modern-4-5c-omnath
# It was chosen because it has many colors of cards, lots of words, and many types.


# region Database


@pytest.fixture(scope="session")
def cli():
    return db.client


@pytest.fixture(scope="session")
def scooze_test_db(cli):
    return cli[CONFIG.mongo_db]


@pytest.fixture(scope="session")
def event_loop():
    policy = asyncio.get_event_loop_policy()
    loop = policy.new_event_loop()
    yield loop
    loop.close()


@pytest.fixture(scope="session", autouse=True)
async def api_client():
    """API client fixture."""

    async with LifespanManager(app, startup_timeout=100, shutdown_timeout=100):
        server_name = "https://localhost"
        async with AsyncClient(app=app, base_url=server_name) as ac:
            # Yield client to tests
            yield ac
            # Done testing, clean test db
            for model in [CardModel]:
                await model.get_motor_collection().delete_many({})


# @pytest.fixture(scope="session")
# def today() -> date:
#     return datetime.now(timezone.utc).date()


# endregion


# # region Card JSON


# region Helpers


def get_card_json(cards_json: list[str], scryfall_id: str) -> dict:
    """
    Helper to get JSON for a particular card.
    """

    for json_str in cards_json:
        card_json = json.loads(json_str)
        if card_json["id"] == scryfall_id:
            return card_json


def get_cardmodel_from_json(card_json: dict) -> CardModel:
    card_data = CardModelData.model_validate(card_json)
    return CardModel.model_validate(card_data.model_dump(mode="json", by_alias=True))


# endregion

# region Card JSON


@pytest.fixture(scope="session")
def cards_json() -> list[str]:
    json_list = []

    with open("./data/test/test_cards.jsonl", "r", encoding="utf8") as json_file:
        json_list.extend(list(json_file))

    with open("./data/test/4c_cards.jsonl", "r", encoding="utf8") as json_file:
        json_list.extend(list(json_file))

    return json_list


# Creature
@pytest.fixture(scope="session")
def json_omnath_locus_of_creation(cards_json) -> dict:
    return get_card_json(cards_json, "4e4fb50c-a81f-44d3-93c5-fa9a0b37f617")


# Instant
@pytest.fixture(scope="session")
def json_ancestral_recall(cards_json) -> dict:
    return get_card_json(cards_json, "2398892d-28e9-4009-81ec-0d544af79d2b")


# Land
@pytest.fixture(scope="session")
def json_boseiju_who_endures(cards_json) -> dict:
    return get_card_json(cards_json, "2135ac5a-187b-4dc9-8f82-34e8d1603416")


# Artifact
@pytest.fixture(scope="session")
def json_chalice_of_the_void(cards_json) -> dict:
    return get_card_json(cards_json, "1f0d2e8e-c8f2-4b31-a6ba-6283fc8740d4")


# Token
@pytest.fixture(scope="session")
def json_snake_token(cards_json) -> dict:
    return get_card_json(cards_json, "153f01ac-8601-488f-8da7-72f392c0a3c6")


# Transforming Planeswalker
@pytest.fixture(scope="session")
def json_arlinn_the_packs_hope(cards_json) -> dict:
    return get_card_json(cards_json, "50d4b0df-a1d8-494f-a019-70ce34161320")


# Reversible
@pytest.fixture(scope="session")
def json_zndrsplt_eye_of_wisdom(cards_json) -> dict:
    return get_card_json(cards_json, "d5dfd236-b1da-4552-b94f-ebf6bb9dafdf")


# Watermark
@pytest.fixture(scope="session")
def json_anaconda_7ed_foil(cards_json) -> dict:
    return get_card_json(cards_json, "2dccffce-5ebd-4aaa-be05-1c6537d211f4")


# Non-English
@pytest.fixture(scope="session")
def json_python_spanish(cards_json) -> dict:
    return get_card_json(cards_json, "973dbd10-708a-42d5-ba15-615104563f0f")


# Flavor Name / Text
@pytest.fixture(scope="session")
def json_elessar_the_elfstone(cards_json) -> dict:
    return get_card_json(cards_json, "a1f3fc27-b3ea-476c-be23-f1c30ef27f96")  # Cloudstone Curio


# Attraction
@pytest.fixture(scope="session")
def json_trash_bin(cards_json) -> dict:
    return get_card_json(cards_json, "f07c39f7-5c3e-40f6-b584-458b65282a7e")


# Variation / Variation Of
@pytest.fixture(scope="session")
def json_anaconda_portal(cards_json) -> dict:
    return get_card_json(cards_json, "6ffba7a5-8845-46f4-bb86-4722d6cbd4c1")


# endregion

# region CardModels


@pytest.fixture(scope="session")
def cardmodel_omnath(json_omnath_locus_of_creation) -> CardModel:
    return get_cardmodel_from_json(json_omnath_locus_of_creation)


# endregion

# def get_cardmodelout_from_json(card_json: dict) -> CardModel:
#     """
#     Helper to get a CardModel from some JSON.
#     """

#     model = CardModel.model_validate(card_json)
#     model.scooze_id = str(ObjectId())
#     return model


# # endregion


# # region Test Cards


# # Instant
# @pytest.fixture(scope="session")
# def json_ancestral_recall(cards_json) -> dict:
#     return get_card_json(cards_json, "2398892d-28e9-4009-81ec-0d544af79d2b")


# @pytest.fixture(scope="session")
# def model_ancestral_recall(json_ancestral_recall) -> CardModel:
#     return get_cardmodelout_from_json(json_ancestral_recall)


# # Creature
# @pytest.fixture(scope="session")
# def json_mystic_snake(cards_json) -> dict:
#     return get_card_json(cards_json, "2d4bacd1-b602-4bcc-9aea-1229949a7d20")


# # Costless
# @pytest.fixture(scope="session")
# def json_ancestral_visions(cards_json) -> dict:
#     return get_card_json(cards_json, "9079c93e-3da8-442a-89d2-609a3eac83b0")


# # Digital
# @pytest.fixture(scope="session")
# def json_urzas_construction_drone(cards_json) -> dict:
#     return get_card_json(cards_json, "bfa6bfa2-0aee-4623-a17e-a77898deb16d")


# # Transform (Saga)
# @pytest.fixture(scope="session")
# def json_tales_of_master_seshiro(cards_json) -> dict:
#     return get_card_json(cards_json, "512bc867-3a86-4da2-93f0-dd76d6a6f30d")


# # endregion


# # region Fixtures for Card and CardModel tests


@pytest.fixture()
def legalities_ancestral_recall() -> dict[Format, Legality]:
    return {
        Format.ALCHEMY: Legality.NOT_LEGAL,
        Format.BRAWL: Legality.NOT_LEGAL,
        Format.COMMANDER: Legality.BANNED,
        Format.DUEL: Legality.BANNED,
        Format.EXPLORER: Legality.NOT_LEGAL,
        Format.FUTURE: Legality.NOT_LEGAL,
        Format.GLADIATOR: Legality.NOT_LEGAL,
        Format.HISTORIC: Legality.NOT_LEGAL,
        Format.HISTORICBRAWL: Legality.NOT_LEGAL,
        Format.LEGACY: Legality.BANNED,
        Format.MODERN: Legality.NOT_LEGAL,
        Format.OATHBREAKER: Legality.BANNED,
        Format.OLDSCHOOL: Legality.NOT_LEGAL,
        Format.PAUPER: Legality.NOT_LEGAL,
        Format.PAUPERCOMMANDER: Legality.NOT_LEGAL,
        Format.PENNY: Legality.NOT_LEGAL,
        Format.PIONEER: Legality.NOT_LEGAL,
        Format.PREDH: Legality.BANNED,
        Format.PREMODERN: Legality.NOT_LEGAL,
        Format.STANDARD: Legality.NOT_LEGAL,
        Format.VINTAGE: Legality.RESTRICTED,
    }


@pytest.fixture()
def legalities_snake_token() -> dict[Format, Legality]:
    return {
        Format.ALCHEMY: Legality.NOT_LEGAL,
        Format.BRAWL: Legality.NOT_LEGAL,
        Format.COMMANDER: Legality.NOT_LEGAL,
        Format.DUEL: Legality.NOT_LEGAL,
        Format.EXPLORER: Legality.NOT_LEGAL,
        Format.FUTURE: Legality.NOT_LEGAL,
        Format.GLADIATOR: Legality.NOT_LEGAL,
        Format.HISTORIC: Legality.NOT_LEGAL,
        Format.HISTORICBRAWL: Legality.NOT_LEGAL,
        Format.LEGACY: Legality.NOT_LEGAL,
        Format.MODERN: Legality.NOT_LEGAL,
        Format.OATHBREAKER: Legality.NOT_LEGAL,
        Format.OLDSCHOOL: Legality.NOT_LEGAL,
        Format.PAUPER: Legality.NOT_LEGAL,
        Format.PAUPERCOMMANDER: Legality.NOT_LEGAL,
        Format.PENNY: Legality.NOT_LEGAL,
        Format.PIONEER: Legality.NOT_LEGAL,
        Format.PREDH: Legality.NOT_LEGAL,
        Format.PREMODERN: Legality.NOT_LEGAL,
        Format.STANDARD: Legality.NOT_LEGAL,
        Format.VINTAGE: Legality.NOT_LEGAL,
    }


@pytest.fixture()
def legalities_zndrsplt_eye_of_wisdom() -> dict[Format, Legality]:
    return {
        Format.ALCHEMY: Legality.NOT_LEGAL,
        Format.BRAWL: Legality.NOT_LEGAL,
        Format.COMMANDER: Legality.LEGAL,
        Format.DUEL: Legality.LEGAL,
        Format.EXPLORER: Legality.NOT_LEGAL,
        Format.FUTURE: Legality.NOT_LEGAL,
        Format.GLADIATOR: Legality.NOT_LEGAL,
        Format.HISTORIC: Legality.NOT_LEGAL,
        Format.HISTORICBRAWL: Legality.NOT_LEGAL,
        Format.LEGACY: Legality.LEGAL,
        Format.MODERN: Legality.NOT_LEGAL,
        Format.OATHBREAKER: Legality.LEGAL,
        Format.OLDSCHOOL: Legality.NOT_LEGAL,
        Format.PAUPER: Legality.NOT_LEGAL,
        Format.PAUPERCOMMANDER: Legality.NOT_LEGAL,
        Format.PENNY: Legality.NOT_LEGAL,
        Format.PIONEER: Legality.NOT_LEGAL,
        Format.PREDH: Legality.NOT_LEGAL,
        Format.PREMODERN: Legality.NOT_LEGAL,
        Format.STANDARD: Legality.NOT_LEGAL,
        Format.VINTAGE: Legality.LEGAL,
    }


# @pytest.fixture(scope="session")
# def oracle_tales_of_master_seshiro() -> str:
#     return (
#         "(As this Saga enters and after your draw step, add a lore counter.)\n"
#         "I, II — Put a +1/+1 counter on target creature or Vehicle you control. It "
#         "gains vigilance until end of turn.\n"
#         "III — Exile this Saga, then return it to the battlefield transformed under "
#         "your control."
#     )


@pytest.fixture()
def oracle_arlinn_daybound() -> str:
    return (
        "Daybound (If a player casts no spells during their own turn, it becomes "
        "night next turn.)\n"
        "+1: Until your next turn, you may cast creature spells as though they had "
        "flash, and each creature you control enters the battlefield with an "
        "additional +1/+1 counter on it.\n"
        "−3: Create two 2/2 green Wolf creature tokens."
    )


@pytest.fixture()
def oracle_arlinn_nightbound() -> str:
    return (
        "Nightbound (If a player casts at least two spells during their own turn, it "
        "becomes day next turn.)\n"
        "+2: Add {R}{G}.\n"
        "0: Until end of turn, Arlinn, the Moon's Fury becomes a 5/5 Werewolf "
        "creature with trample, indestructible, and haste."
    )


@pytest.fixture()
def oracle_zndrsplt_eye_of_wisdom() -> str:
    return (
        "Partner with Okaun, Eye of Chaos (When this creature enters the "
        "battlefield, target player may put Okaun into their hand from their "
        "library, then shuffle.)\n"
        "At the beginning of combat on your turn, flip a coin until you lose a "
        "flip.\n"
        "Whenever a player wins a coin flip, draw a card."
    )


# # endregion


# # region Test OracleCards


# # Cards are sorted alphabetically


# @pytest.fixture(scope="session")
# def card_aether_gust(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "783da808-6698-4e55-9fac-430a6effe2b1")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_boseiju_who_endures(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "2135ac5a-187b-4dc9-8f82-34e8d1603416")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_breeding_pool(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "bb54233c-0844-4965-9cde-e8a4ef3e11b8")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_chalice_of_the_void(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "1f0d2e8e-c8f2-4b31-a6ba-6283fc8740d4")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_counterspell(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "8493131c-0a7b-4be6-a8a2-0b425f4f67fb")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_dovins_veto(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "5d6b5054-2224-4f68-9d82-3ed17c5dacc4")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_dress_down(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "04f9f061-67b8-4427-9fcb-b3ccfee8fc5d")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_flooded_strand(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "8c2996d9-3287-4480-8c04-7a378e37e3cf")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_flusterstorm(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "f900eeb7-7c45-44bc-ad3a-0bbe594ecf50")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_force_of_negation(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "1825a719-1b2a-4af9-9cd2-7cb497cd0317")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_forest(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "ecd6d8fb-780c-446c-a8bf-93386b22fe95")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_hallowed_fountain(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "f97a6d34-03ab-49f1-b02e-405b733f8843")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_hallowed_moonlight(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "94fd0c0f-4a6a-47cf-9f50-df0bbf19aae4")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_island(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "bd4b4da4-83f6-4280-880b-b6033308f2a2")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_kaheera_the_orphanguard(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "d4ebed0b-8060-4a7b-a060-5cfcd2172b16")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_leyline_binding(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "3c3ac3dd-35db-447f-8674-37b4680a1ef7")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_minamo_school_at_waters_edge(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "7536292c-da25-41c8-ba28-1e35758a7f3d")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_misty_rainforest(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "88231c0d-0cc8-44ec-bf95-81d1710ac141")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_omnath_locus_of_creation(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "4e4fb50c-a81f-44d3-93c5-fa9a0b37f617")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_otawara_soaring_city(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "486d7edc-d983-41f0-8b78-c99aecd72996")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_plains(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "c9cd4d57-8c51-4fcf-8a9f-5d6a61c33e3d")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_prismatic_ending(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "825969b9-3c70-4fca-8cab-696e9ca7cdb2")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_raugrin_triome(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "02138fbb-3962-4348-8d31-faaefba0b8b2")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_sacred_foundry(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "b7b598d0-535d-477d-a33d-d6a10ff5439a")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_solitude(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "47a6234f-309f-4e03-9263-66da48b57153")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_spell_pierce(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "35b8a9db-d126-4038-abb1-74dcc5b36136")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_steam_vents(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "b8ebe3cf-7143-453a-b0ef-2f5bdaac3185")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_stern_scolding(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "3ca1e1de-b916-445f-b3b2-0f4d0cc7ceeb")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_subtlety(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "701256d5-1389-48b7-9581-d6037209bd06")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_supreme_verdict(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "20b5fe42-929c-406d-9377-40b49f9d2e2c")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_teferi_time_raveler(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "5cb76266-ae50-4bbc-8f96-d98f309b02d3")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_temple_garden(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "2b9b0195-beda-403e-bc27-7ae3be9f318c")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_the_one_ring(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "d5806e68-1054-458e-866d-1f2470f682b2")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_veil_of_summer(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "aa686c34-1c11-469f-93c2-f9891aea521f")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_wear_tear(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "e01cc65a-0e38-4f41-b9ed-796ef0355d0b")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_windswept_heath(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "e7b28650-cddc-4878-b1d1-b5a764f4df49")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_wrenn_and_six(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "5bd498cc-a609-4457-9325-6888d59ca36f")
#     return OracleCard.from_json(card_json)


# @pytest.fixture(scope="session")
# def card_zagoth_triome(cards_json) -> OracleCard:
#     card_json = get_card_json(cards_json, "cc520518-2063-4b57-a0d4-10cf62a7175e")
#     return OracleCard.from_json(card_json)


# # endregion


# # region DeckParts


# @pytest.fixture
# def archetype_modern_4c() -> str:
#     return "Four-color Control"


# @pytest.fixture
# def main_modern_4c(
#     card_boseiju_who_endures,
#     card_breeding_pool,
#     card_counterspell,
#     card_dress_down,
#     card_flooded_strand,
#     card_force_of_negation,
#     card_forest,
#     card_hallowed_fountain,
#     card_island,
#     card_leyline_binding,
#     card_minamo_school_at_waters_edge,
#     card_misty_rainforest,
#     card_omnath_locus_of_creation,
#     card_otawara_soaring_city,
#     card_plains,
#     card_prismatic_ending,
#     card_raugrin_triome,
#     card_sacred_foundry,
#     card_solitude,
#     card_spell_pierce,
#     card_steam_vents,
#     card_stern_scolding,
#     card_subtlety,
#     card_teferi_time_raveler,
#     card_temple_garden,
#     card_the_one_ring,
#     card_windswept_heath,
#     card_wrenn_and_six,
#     card_zagoth_triome,
# ) -> DeckPart[OracleCard]:
#     main_cards = Counter[OracleCard](
#         {
#             # Creature
#             card_omnath_locus_of_creation: 3,
#             card_subtlety: 1,
#             card_solitude: 4,
#             # Planeswalker
#             card_wrenn_and_six: 4,
#             card_teferi_time_raveler: 4,
#             # Sorcery
#             card_prismatic_ending: 3,
#             # Instant
#             card_spell_pierce: 1,
#             card_stern_scolding: 1,
#             card_counterspell: 4,
#             card_force_of_negation: 2,
#             # Artifact
#             card_the_one_ring: 4,
#             # Enchantment
#             card_dress_down: 1,
#             card_leyline_binding: 4,
#             # Land
#             card_boseiju_who_endures: 1,
#             card_breeding_pool: 1,
#             card_flooded_strand: 4,
#             card_forest: 1,
#             card_hallowed_fountain: 1,
#             card_island: 2,
#             card_minamo_school_at_waters_edge: 1,
#             card_misty_rainforest: 4,
#             card_otawara_soaring_city: 1,
#             card_plains: 1,
#             card_raugrin_triome: 1,
#             card_sacred_foundry: 1,
#             card_steam_vents: 1,
#             card_temple_garden: 1,
#             card_windswept_heath: 2,
#             card_zagoth_triome: 1,
#         }
#     )

#     return DeckPart[OracleCard](main_cards)


# @pytest.fixture
# def main_modern_4c_str(
#     card_boseiju_who_endures,
#     card_breeding_pool,
#     card_counterspell,
#     card_dress_down,
#     card_flooded_strand,
#     card_force_of_negation,
#     card_forest,
#     card_hallowed_fountain,
#     card_island,
#     card_leyline_binding,
#     card_minamo_school_at_waters_edge,
#     card_misty_rainforest,
#     card_omnath_locus_of_creation,
#     card_otawara_soaring_city,
#     card_plains,
#     card_prismatic_ending,
#     card_raugrin_triome,
#     card_sacred_foundry,
#     card_solitude,
#     card_spell_pierce,
#     card_steam_vents,
#     card_stern_scolding,
#     card_subtlety,
#     card_teferi_time_raveler,
#     card_temple_garden,
#     card_the_one_ring,
#     card_windswept_heath,
#     card_wrenn_and_six,
#     card_zagoth_triome,
# ) -> str:
#     return (
#         # Creature
#         f"3 {card_omnath_locus_of_creation.name}\n"
#         f"1 {card_subtlety.name}\n"
#         f"4 {card_solitude.name}\n"
#         # Planeswalker
#         f"4 {card_wrenn_and_six.name}\n"
#         f"4 {card_teferi_time_raveler.name}\n"
#         # Sorcery
#         f"3 {card_prismatic_ending.name}\n"
#         # Instant
#         f"1 {card_spell_pierce.name}\n"
#         f"1 {card_stern_scolding.name}\n"
#         f"4 {card_counterspell.name}\n"
#         f"2 {card_force_of_negation.name}\n"
#         # Artifact
#         f"4 {card_the_one_ring.name}\n"
#         # Enchantment
#         f"1 {card_dress_down.name}\n"
#         f"4 {card_leyline_binding.name}\n"
#         # Land
#         f"1 {card_boseiju_who_endures.name}\n"
#         f"1 {card_breeding_pool.name}\n"
#         f"4 {card_flooded_strand.name}\n"
#         f"1 {card_forest.name}\n"
#         f"1 {card_hallowed_fountain.name}\n"
#         f"2 {card_island.name}\n"
#         f"1 {card_minamo_school_at_waters_edge.name}\n"
#         f"4 {card_misty_rainforest.name}\n"
#         f"1 {card_otawara_soaring_city.name}\n"
#         f"1 {card_plains.name}\n"
#         f"1 {card_raugrin_triome.name}\n"
#         f"1 {card_sacred_foundry.name}\n"
#         f"1 {card_steam_vents.name}\n"
#         f"1 {card_temple_garden.name}\n"
#         f"2 {card_windswept_heath.name}\n"
#         f"1 {card_zagoth_triome.name}\n"
#     )


# @pytest.fixture
# def side_modern_4c(
#     card_aether_gust,
#     card_boseiju_who_endures,
#     card_chalice_of_the_void,
#     card_dovins_veto,
#     card_dress_down,
#     card_flusterstorm,
#     card_hallowed_moonlight,
#     card_kaheera_the_orphanguard,
#     card_prismatic_ending,
#     card_supreme_verdict,
#     card_veil_of_summer,
#     card_wear_tear,
# ) -> DeckPart[OracleCard]:
#     side_cards = Counter[OracleCard](
#         {
#             card_aether_gust: 1,
#             card_boseiju_who_endures: 1,
#             card_chalice_of_the_void: 2,
#             card_dovins_veto: 1,
#             card_dress_down: 1,
#             card_flusterstorm: 1,
#             card_hallowed_moonlight: 2,
#             card_kaheera_the_orphanguard: 1,
#             card_prismatic_ending: 1,
#             card_supreme_verdict: 1,
#             card_veil_of_summer: 2,
#             card_wear_tear: 1,
#         }
#     )

#     return DeckPart[OracleCard](side_cards)


# @pytest.fixture
# def side_modern_4c_str(
#     card_aether_gust,
#     card_boseiju_who_endures,
#     card_chalice_of_the_void,
#     card_dovins_veto,
#     card_dress_down,
#     card_flusterstorm,
#     card_hallowed_moonlight,
#     card_kaheera_the_orphanguard,
#     card_prismatic_ending,
#     card_supreme_verdict,
#     card_veil_of_summer,
#     card_wear_tear,
# ) -> str:
#     return (
#         f"1 {card_aether_gust.name}\n"
#         f"1 {card_boseiju_who_endures.name}\n"
#         f"2 {card_chalice_of_the_void.name}\n"
#         f"1 {card_dovins_veto.name}\n"
#         f"1 {card_dress_down.name}\n"
#         f"1 {card_flusterstorm.name}\n"
#         f"2 {card_hallowed_moonlight.name}\n"
#         f"1 {card_kaheera_the_orphanguard.name}\n"
#         f"1 {card_prismatic_ending.name}\n"
#         f"1 {card_supreme_verdict.name}\n"
#         f"2 {card_veil_of_summer.name}\n"
#         f"1 {card_wear_tear.name}\n"
#     )


# # endregion


# # region Deck


# @pytest.fixture
# def deck_modern_4c(archetype_modern_4c, main_modern_4c, side_modern_4c) -> Deck[OracleCard]:
#     return Deck[OracleCard](
#         archetype=archetype_modern_4c, format=Format.MODERN, main=main_modern_4c, side=side_modern_4c
#     )


# # endregion
