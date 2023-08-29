import json
from collections import Counter

import pytest
from scooze.card import OracleCard
from scooze.deck import Deck
from scooze.deckpart import DeckPart
from scooze.enums import Color, Format

# These fixtures can be used in any tests in this directory.
# https://www.mtggoldfish.com/archetype/modern-4-5c-omnath
# It was chosen because it has many colors of cards, lots of words, and many types.


# region Card JSON


@pytest.fixture(scope="session")
def cards_json() -> list[str]:
    with open("./data/test/test_cards.jsonl", "r") as json_file:
        json_list = list(json_file)

    return json_list


# NOTE: helper to get particular card_json
def get_card_json(cards_json: list[str], id: str) -> dict:
    for json_str in cards_json:
        card_json = json.loads(json_str)
        if card_json["id"] == id:
            return card_json


# Instant
@pytest.fixture(scope="session")
def json_ancestral_recall(cards_json) -> dict:
    return get_card_json(cards_json, "2398892d-28e9-4009-81ec-0d544af79d2b")


# Creature
@pytest.fixture(scope="session")
def json_mystic_snake(cards_json) -> dict:
    return get_card_json(cards_json, "2d4bacd1-b602-4bcc-9aea-1229949a7d20")


# Costless
@pytest.fixture(scope="session")
def json_ancestral_visions(cards_json) -> dict:
    return get_card_json(cards_json, "9079c93e-3da8-442a-89d2-609a3eac83b0")


# Digital
@pytest.fixture(scope="session")
def json_urzas_construction_drone(cards_json) -> dict:
    return get_card_json(cards_json, "bfa6bfa2-0aee-4623-a17e-a77898deb16d")


# Transform (Saga)
@pytest.fixture(scope="session")
def json_tales_of_master_seshiro(cards_json) -> dict:
    return get_card_json(cards_json, "512bc867-3a86-4da2-93f0-dd76d6a6f30d")


# Transform (Planeswalker)
@pytest.fixture(scope="session")
def json_arlinn_the_packs_hope(cards_json) -> dict:
    return get_card_json(cards_json, "50d4b0df-a1d8-494f-a019-70ce34161320")


# Reversible
@pytest.fixture(scope="session")
def json_zndrsplt_eye_of_wisdom(cards_json) -> dict:
    return get_card_json(cards_json, "d5dfd236-b1da-4552-b94f-ebf6bb9dafdf")


# Token
@pytest.fixture(scope="session")
def json_snake_token(cards_json) -> dict:
    return get_card_json(cards_json, "153f01ac-8601-488f-8da7-72f392c0a3c6")


# endregion


# region Simple Cards

# Cards are sorted alphabetically


@pytest.fixture
def card_aether_gust() -> OracleCard:
    return OracleCard(
        name="Aether Gust",
        cmc=2,
        colors=[Color.BLUE],
        type_line="Instant",
    )


@pytest.fixture
def card_boseiju_who_endures() -> OracleCard:
    return OracleCard(
        name="Boseiju, Who Endures",
        cmc=0,
        colors=[],
        type_line="Legendary Land",
    )


@pytest.fixture
def card_breeding_pool() -> OracleCard:
    return OracleCard(
        name="Breeding Pool",
        cmc=0,
        colors=[],
        type_line="Land - Forest Island",
    )


@pytest.fixture
def card_chalice_of_the_void() -> OracleCard:
    return OracleCard(
        name="Chalice of the Void",
        cmc=0,
        colors=[],
        type_line="Artifact",
    )


@pytest.fixture
def card_counterspell() -> OracleCard:
    return OracleCard(
        name="Counterspell",
        cmc=2,
        colors=[Color.BLUE],
        type_line="Instant",
    )


@pytest.fixture
def card_dovins_veto() -> OracleCard:
    return OracleCard(
        name="Dovin's Veto",
        cmc=2,
        colors=[Color.WHITE, Color.BLUE],
        type_line="Instant",
    )


@pytest.fixture
def card_dress_down() -> OracleCard:
    return OracleCard(
        name="Dress Down",
        cmc=2,
        colors=[Color.BLUE],
        type_line="Enchantment",
    )


@pytest.fixture
def card_flooded_strand() -> OracleCard:
    return OracleCard(
        name="Flooded Strand",
        cmc=0,
        colors=[],
        type_line="Land",
    )


@pytest.fixture
def card_flusterstorm() -> OracleCard:
    return OracleCard(
        name="Flusterstorm",
        cmc=1,
        colors=[Color.BLUE],
        type_line="Instant",
    )


@pytest.fixture
def card_force_of_negation() -> OracleCard:
    return OracleCard(
        name="Force of Negation",
        cmc=3,
        colors=[Color.BLUE],
        type_line="Instant",
    )


@pytest.fixture
def card_forest() -> OracleCard:
    return OracleCard(
        name="Forest",
        cmc=0,
        colors=[],
        type_line="Basic Land - Forest",
    )


@pytest.fixture
def card_hallowed_fountain() -> OracleCard:
    return OracleCard(
        name="Hallowed Fountain",
        cmc=0,
        colors=[],
        type_line="Land - Plains Island",
    )


@pytest.fixture
def card_hallowed_moonlight() -> OracleCard:
    return OracleCard(
        name="Hallowed Moonlight",
        cmc=2,
        colors=[Color.WHITE],
        type_line="Instant",
    )


@pytest.fixture
def card_island() -> OracleCard:
    return OracleCard(
        name="Island",
        cmc=0,
        colors=[],
        type_line="Basic Land - Island",
    )


@pytest.fixture
def card_kaheera_the_orphanguard() -> OracleCard:
    return OracleCard(
        name="Kaheera, the Orphanguard",
        cmc=3,
        colors=[Color.WHITE, Color.GREEN],
        type_line="Legendary Creature - Cat Beast",
    )


@pytest.fixture
def card_leyline_binding() -> OracleCard:
    return OracleCard(
        name="Leyline Binding",
        cmc=6,
        colors=[Color.WHITE],
        type_line="Enchantment",
    )


@pytest.fixture
def card_minamo_school_at_waters_edge() -> OracleCard:
    return OracleCard(
        name="Minamo, School at Water's Edge",
        cmc=0,
        colors=[],
        type_line="Legendary Land",
    )


@pytest.fixture
def card_misty_rainforest() -> OracleCard:
    return OracleCard(
        name="Misty Rainforest",
        cmc=0,
        colors=[],
        type_line="Land",
    )


@pytest.fixture
def card_omnath_locus_of_creation() -> OracleCard:
    return OracleCard(
        name="Omnath, Locus of Creation",
        cmc=4,
        colors=[Color.WHITE, Color.BLUE, Color.RED, Color.GREEN],
        type_line="Legendary Creature - Elemental",
    )


@pytest.fixture
def card_otawara_soaring_city() -> OracleCard:
    return OracleCard(
        name="Otawara, Soaring City",
        cmc=0,
        colors=[],
        type_line="Legendary Land",
    )


@pytest.fixture
def card_plains() -> OracleCard:
    return OracleCard(
        name="Plains",
        cmc=0,
        colors=[],
        type_line="Basic Land - Plains",
    )


@pytest.fixture
def card_prismatic_ending() -> OracleCard:
    return OracleCard(
        name="Prismatic Ending",
        cmc=1,
        colors=[Color.WHITE],
        type_line="Sorcery",
    )


@pytest.fixture
def card_raugrin_triome() -> OracleCard:
    return OracleCard(
        name="Raugrin Triome",
        cmc=0,
        colors=[],
        type_line="Land - Island Mountain Plains",
    )


@pytest.fixture
def card_sacred_foundry() -> OracleCard:
    return OracleCard(
        name="Sacred Foundry",
        cmc=0,
        colors=[],
        type_line="Land - Mountain Plains",
    )


@pytest.fixture
def card_solitude() -> OracleCard:
    return OracleCard(
        name="Solitude",
        cmc=5,
        colors=[Color.WHITE],
        type_line="Creature - Elemental",
    )


@pytest.fixture
def card_spell_pierce() -> OracleCard:
    return OracleCard(
        name="Spell Pierce",
        cmc=1,
        colors=[Color.BLUE],
        type_line="Instant",
    )


@pytest.fixture
def card_steam_vents() -> OracleCard:
    return OracleCard(
        name="Steam Vents",
        cmc=0,
        colors=[],
        type_line="Land - Island Mountain",
    )


@pytest.fixture
def card_stern_scolding() -> OracleCard:
    return OracleCard(
        name="Stern Scolding",
        cmc=1,
        colors=[Color.BLUE],
        type_line="Instant",
    )


@pytest.fixture
def card_subtlety() -> OracleCard:
    return OracleCard(
        name="Subtlety",
        cmc=4,
        colors=[Color.BLUE],
        type_line="Creature - Elemental",
    )


@pytest.fixture
def card_supreme_verdict() -> OracleCard:
    return OracleCard(
        name="Supreme Verdict",
        cmc=4,
        colors=[Color.WHITE, Color.BLUE],
        type_line="Sorcery",
    )


@pytest.fixture
def card_teferi_time_raveler() -> OracleCard:
    return OracleCard(
        name="Teferi, Time Raveler",
        cmc=3,
        colors=[Color.WHITE, Color.BLUE],
        type_line="Legendary Planeswalker - Teferi",
    )


@pytest.fixture
def card_temple_garden() -> OracleCard:
    return OracleCard(
        name="Temple Garden",
        cmc=0,
        colors=[],
        type_line="Land - Forest Plains",
    )


@pytest.fixture
def card_the_one_ring() -> OracleCard:
    return OracleCard(
        name="The One Ring",
        cmc=4,
        colors=[],
        type_line="Legendary Artifact",
    )


@pytest.fixture
def card_veil_of_summer() -> OracleCard:
    return OracleCard(
        name="Veil of Summer",
        cmc=1,
        colors=[Color.GREEN],
        type_line="Instant",
    )


@pytest.fixture
def card_wear_tear() -> OracleCard:
    return OracleCard(
        name="Wear // Tear",
        cmc=3,
        colors=[Color.WHITE, Color.RED],
        type_line="Instant // Instant",
    )


@pytest.fixture
def card_windswept_heath() -> OracleCard:
    return OracleCard(
        name="Windswept Heath",
        cmc=0,
        colors=[],
        type_line="Land",
    )


@pytest.fixture
def card_wrenn_and_six() -> OracleCard:
    return OracleCard(
        name="Wrenn and Six",
        cmc=2,
        colors=[Color.RED, Color.GREEN],
        type_line="Legendary Planeswalker - Wrenn",
    )


@pytest.fixture
def card_zagoth_triome() -> OracleCard:
    return OracleCard(
        name="Zagoth Triome",
        cmc=0,
        colors=[],
        type_line="Land - Swamp Forest Island",
    )


# endregion


# region DeckParts


@pytest.fixture
def archetype_modern_4c() -> str:
    return "Four-color Control"


@pytest.fixture
def main_modern_4c(
    card_boseiju_who_endures,
    card_breeding_pool,
    card_counterspell,
    card_dress_down,
    card_flooded_strand,
    card_force_of_negation,
    card_forest,
    card_hallowed_fountain,
    card_island,
    card_leyline_binding,
    card_minamo_school_at_waters_edge,
    card_misty_rainforest,
    card_omnath_locus_of_creation,
    card_otawara_soaring_city,
    card_plains,
    card_prismatic_ending,
    card_raugrin_triome,
    card_sacred_foundry,
    card_solitude,
    card_spell_pierce,
    card_steam_vents,
    card_stern_scolding,
    card_subtlety,
    card_teferi_time_raveler,
    card_temple_garden,
    card_the_one_ring,
    card_windswept_heath,
    card_wrenn_and_six,
    card_zagoth_triome,
) -> DeckPart:
    main_cards = Counter(
        {
            # Creature
            card_omnath_locus_of_creation: 3,
            card_subtlety: 1,
            card_solitude: 4,
            # Planeswalker
            card_wrenn_and_six: 4,
            card_teferi_time_raveler: 4,
            # Sorcery
            card_prismatic_ending: 3,
            # Instant
            card_spell_pierce: 1,
            card_stern_scolding: 1,
            card_counterspell: 4,
            card_force_of_negation: 2,
            # Artifact
            card_the_one_ring: 4,
            # Enchantment
            card_dress_down: 1,
            card_leyline_binding: 4,
            # Land
            card_boseiju_who_endures: 1,
            card_breeding_pool: 1,
            card_flooded_strand: 4,
            card_forest: 1,
            card_hallowed_fountain: 1,
            card_island: 2,
            card_minamo_school_at_waters_edge: 1,
            card_misty_rainforest: 4,
            card_otawara_soaring_city: 1,
            card_plains: 1,
            card_raugrin_triome: 1,
            card_sacred_foundry: 1,
            card_steam_vents: 1,
            card_temple_garden: 1,
            card_windswept_heath: 2,
            card_zagoth_triome: 1,
        }
    )

    return DeckPart(main_cards)


@pytest.fixture
def main_modern_4c_str(
    card_boseiju_who_endures,
    card_breeding_pool,
    card_counterspell,
    card_dress_down,
    card_flooded_strand,
    card_force_of_negation,
    card_forest,
    card_hallowed_fountain,
    card_island,
    card_leyline_binding,
    card_minamo_school_at_waters_edge,
    card_misty_rainforest,
    card_omnath_locus_of_creation,
    card_otawara_soaring_city,
    card_plains,
    card_prismatic_ending,
    card_raugrin_triome,
    card_sacred_foundry,
    card_solitude,
    card_spell_pierce,
    card_steam_vents,
    card_stern_scolding,
    card_subtlety,
    card_teferi_time_raveler,
    card_temple_garden,
    card_the_one_ring,
    card_windswept_heath,
    card_wrenn_and_six,
    card_zagoth_triome,
) -> str:
    return (
        # Creature
        f"3 {card_omnath_locus_of_creation.name}\n"
        f"1 {card_subtlety.name}\n"
        f"4 {card_solitude.name}\n"
        # Planeswalker
        f"4 {card_wrenn_and_six.name}\n"
        f"4 {card_teferi_time_raveler.name}\n"
        # Sorcery
        f"3 {card_prismatic_ending.name}\n"
        # Instant
        f"1 {card_spell_pierce.name}\n"
        f"1 {card_stern_scolding.name}\n"
        f"4 {card_counterspell.name}\n"
        f"2 {card_force_of_negation.name}\n"
        # Artifact
        f"4 {card_the_one_ring.name}\n"
        # Enchantment
        f"1 {card_dress_down.name}\n"
        f"4 {card_leyline_binding.name}\n"
        # Land
        f"1 {card_boseiju_who_endures.name}\n"
        f"1 {card_breeding_pool.name}\n"
        f"4 {card_flooded_strand.name}\n"
        f"1 {card_forest.name}\n"
        f"1 {card_hallowed_fountain.name}\n"
        f"2 {card_island.name}\n"
        f"1 {card_minamo_school_at_waters_edge.name}\n"
        f"4 {card_misty_rainforest.name}\n"
        f"1 {card_otawara_soaring_city.name}\n"
        f"1 {card_plains.name}\n"
        f"1 {card_raugrin_triome.name}\n"
        f"1 {card_sacred_foundry.name}\n"
        f"1 {card_steam_vents.name}\n"
        f"1 {card_temple_garden.name}\n"
        f"2 {card_windswept_heath.name}\n"
        f"1 {card_zagoth_triome.name}\n"
    )


@pytest.fixture
def side_modern_4c(
    card_aether_gust,
    card_boseiju_who_endures,
    card_chalice_of_the_void,
    card_dovins_veto,
    card_dress_down,
    card_flusterstorm,
    card_hallowed_moonlight,
    card_kaheera_the_orphanguard,
    card_prismatic_ending,
    card_supreme_verdict,
    card_veil_of_summer,
    card_wear_tear,
) -> DeckPart:
    side_cards = Counter(
        {
            card_aether_gust: 1,
            card_boseiju_who_endures: 1,
            card_chalice_of_the_void: 2,
            card_dovins_veto: 1,
            card_dress_down: 1,
            card_flusterstorm: 1,
            card_hallowed_moonlight: 2,
            card_kaheera_the_orphanguard: 1,
            card_prismatic_ending: 1,
            card_supreme_verdict: 1,
            card_veil_of_summer: 2,
            card_wear_tear: 1,
        }
    )

    return DeckPart(side_cards)


@pytest.fixture
def side_modern_4c_str(
    card_aether_gust,
    card_boseiju_who_endures,
    card_chalice_of_the_void,
    card_dovins_veto,
    card_dress_down,
    card_flusterstorm,
    card_hallowed_moonlight,
    card_kaheera_the_orphanguard,
    card_prismatic_ending,
    card_supreme_verdict,
    card_veil_of_summer,
    card_wear_tear,
) -> str:
    return (
        f"1 {card_aether_gust.name}\n"
        f"1 {card_boseiju_who_endures.name}\n"
        f"2 {card_chalice_of_the_void.name}\n"
        f"1 {card_dovins_veto.name}\n"
        f"1 {card_dress_down.name}\n"
        f"1 {card_flusterstorm.name}\n"
        f"2 {card_hallowed_moonlight.name}\n"
        f"1 {card_kaheera_the_orphanguard.name}\n"
        f"1 {card_prismatic_ending.name}\n"
        f"1 {card_supreme_verdict.name}\n"
        f"2 {card_veil_of_summer.name}\n"
        f"1 {card_wear_tear.name}\n"
    )


# endregion

# region Deck


@pytest.fixture
def deck_modern_4c(archetype_modern_4c, main_modern_4c, side_modern_4c) -> Deck:
    return Deck(archetype=archetype_modern_4c, format=Format.MODERN, main=main_modern_4c, side=side_modern_4c)


# endregion
