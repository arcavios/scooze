import json
from datetime import date
from inspect import getmembers
from pprint import pprint

import pytest
from scooze.card import Card, FullCard, OracleCard
from scooze.enums import BorderColor, Color, Finish, Format, Game, Legality, Rarity
from scooze.models.card import CardModel, FullCardModel

# TODO(#65): WRITE TESTS FOR CARD OBJECT HERE

# TODO: remove NOTE s and TODO s from this file.
# Write tests for Card conversion. Write tests for normal Card behavior
# Write tests for CardModel conversion. Write tests for normal CardModel behavior
# Add a token to the test suite

# NOTE: these tests can be run with pytest -s so you can see the print statements
# NOTE: helpful little jq that can get you a card from one of the bulk files. You can get scryfall_id from
# image address on scryfall.com
# ╰─❯ cat data/bulk/oracle_cards.json | jq '.[] | select(.id == "371ceb58-f498-4616-a7f0-eb118fe2e4ff")' > ./data/bulk/card.json

# STUFF TO WORK THROUGH:
# 1. it seems like methods with underscores in the name aren't able to go from json -> Model -> Card object. Investigate.
# 2. we need to write code to get from Card -> json -> Card Model. This might be as easy as model_validate(**card.__dict__)
# 3. The tests need to actually check the values to see if they're what we expect. Use a few different cards to really touch on every field you can
# 4. The same tests should be done for Card and CardModel
# 5. Rename the card classes. This shit sucks.
#       Card and CardModel should be the ones you use the most and should just be called as such, idk.
#       The simpler ones should have the more annoying names imo
# 6. Fix the cards in the conftest and test_deckpart and test_deck to use regular Card instead of OracleCard (I think?)
# 7. Do we want to have CardFaces on the regular cards? probably not? idk
# 8. Figure out if Card.from_model() should use model_dump() or dict(). Investigate the key differences.


@pytest.fixture
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


# TODO: helper to print a card
def print_obj(obj):
    pprint(list(filter(lambda x: not x[0].endswith("__"), getmembers(obj))))


# region Fixtures


@pytest.fixture
def legalities_ancestral_recall() -> dict:
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


@pytest.fixture
def oracle_tales_of_master_seshiro() -> str:
    return (
        """(As this Saga enters and after your draw step, add a lore counter.)\n"""
        """I, II — Put a +1/+1 counter on target creature or Vehicle you control. It """
        """gains vigilance until end of turn.\n"""
        """III — Exile this Saga, then return it to the battlefield transformed under """
        """your control."""
    )


@pytest.fixture
def oracle_arlinn_the_packs_hope() -> str:
    return (
        """Daybound (If a player casts no spells during their own turn, it becomes """
        """night next turn.)\n"""
        """+1: Until your next turn, you may cast creature spells as though they had """
        """flash, and each creature you control enters the battlefield with an """
        """additional +1/+1 counter on it.\n"""
        """−3: Create two 2/2 green Wolf creature tokens."""
    )


@pytest.fixture
def oracle_arlinn_the_moons_fury() -> str:
    return (
        """Nightbound (If a player casts at least two spells during their own turn, it """
        """becomes day next turn.)\n"""
        """+2: Add {R}{G}.\n"""
        """0: Until end of turn, Arlinn, the Moon's Fury becomes a 5/5 Werewolf """
        """creature with trample, indestructible, and haste."""
    )


# region Card JSON Fixtures


@pytest.fixture
def json_ancestral_recall(cards_json) -> dict:
    return get_card_json(cards_json, "2398892d-28e9-4009-81ec-0d544af79d2b")


@pytest.fixture
def json_mystic_snake(cards_json) -> dict:
    return get_card_json(cards_json, "2d4bacd1-b602-4bcc-9aea-1229949a7d20")


@pytest.fixture
def json_ancestral_visions(cards_json) -> dict:
    return get_card_json(cards_json, "9079c93e-3da8-442a-89d2-609a3eac83b0")


# Digital
@pytest.fixture
def json_urzas_construction_drone(cards_json) -> dict:
    return get_card_json(cards_json, "bfa6bfa2-0aee-4623-a17e-a77898deb16d")


# Transform (Saga)
@pytest.fixture
def json_tales_of_master_seshiro(cards_json) -> dict:
    return get_card_json(cards_json, "512bc867-3a86-4da2-93f0-dd76d6a6f30d")


# Transform (Planeswalker)
@pytest.fixture
def json_arlinn_the_packs_hope(cards_json) -> dict:
    return get_card_json(cards_json, "50d4b0df-a1d8-494f-a019-70ce34161320")


# Split (Aftermath)
@pytest.fixture
def json_driven_despair(cards_json) -> dict:
    return get_card_json(cards_json, "7713ba59-dd4c-4b49-93a7-292728df86b8")


# MDFC
@pytest.fixture
def json_turntimber_symbiosis(cards_json) -> dict:
    return get_card_json(cards_json, "61bd69ea-1e9e-46b0-b1a1-ed7fdbe3deb6")


# Flip
@pytest.fixture
def json_orochi_eggwatcher(cards_json) -> dict:
    return get_card_json(cards_json, "a4f4aa3b-c64a-4430-b1a2-a7fca87d0a22")


# endregion

# endregion


# region json -> Card Object

# region Card


def test_card_from_json_instant(json_ancestral_recall, legalities_ancestral_recall):
    card = Card.from_json(json_ancestral_recall)
    assert card.cmc == 1.0
    assert card.color_identity == {Color.BLUE}
    assert card.colors == {Color.BLUE}
    assert card.legalities == legalities_ancestral_recall
    assert card.mana_cost == "{U}"
    assert card.name == "Ancestral Recall"
    assert card.power is None
    assert card.toughness is None
    assert card.type_line == "Instant"


def test_card_from_json_creature(json_mystic_snake):
    card = Card.from_json(json_mystic_snake)
    assert card.color_identity == {Color.BLUE, Color.GREEN}
    assert card.colors == {Color.BLUE, Color.GREEN}
    assert card.power == "2"
    assert card.toughness == "2"
    assert card.type_line == "Creature — Snake"


# endregion

# region OracleCard


def test_oraclecard_from_json_transform_saga(json_tales_of_master_seshiro, oracle_tales_of_master_seshiro):
    card = OracleCard.from_json(json_tales_of_master_seshiro)
    assert len(card.card_faces) == 2
    assert card.type_line == "Enchantment — Saga // Enchantment Creature — Snake Warrior"
    front, back = card.card_faces

    ## Front
    assert front.cmc is None
    assert front.color_indicator is None
    assert front.colors == {Color.GREEN}
    assert front.loyalty is None
    assert front.mana_cost == "{4}{G}"
    assert front.name == "Tales of Master Seshiro"
    assert front.oracle_id is None
    assert front.oracle_text == oracle_tales_of_master_seshiro
    assert front.power is None
    assert front.toughness is None
    assert front.type_line == "Enchantment — Saga"

    ## Back
    assert back.cmc is None
    assert back.color_indicator == {Color.GREEN}
    assert back.colors == {Color.GREEN}
    assert back.loyalty is None
    assert back.mana_cost == ""
    assert back.name == "Seshiro's Living Legacy"
    assert back.oracle_id is None
    assert back.oracle_text == "Vigilance, haste"
    assert back.power == "5"
    assert back.toughness == "5"
    assert back.type_line == "Enchantment Creature — Snake Warrior"


def test_oraclecard_from_json_split_aftermath(json_driven_despair):
    # TODO: fill test
    pass


def test_oraclecard_from_json_mdfc(json_turntimber_symbiosis):
    # TODO: fill test
    pass


def test_oraclecard_from_json_flip(json_orochi_eggwatcher):
    # TODO: fill test
    pass


# endregion

# region FullCard


def test_fullcard_from_json_instant(json_ancestral_recall):
    # TODO: fill test (all fields from top level and non-card face related stuff)
    pass


def test_fullcard_from_json_transform_planeswalker(
    json_arlinn_the_packs_hope, oracle_arlinn_the_packs_hope, oracle_arlinn_the_moons_fury
):
    card = FullCard.from_json(json_arlinn_the_packs_hope)
    assert len(card.card_faces) == 2
    front, back = card.card_faces

    ## Front
    assert front.artist
    assert front.cmc is None
    assert front.color_indicator is None
    assert front.colors == {Color.RED, Color.GREEN}
    assert front.flavor_text is None
    assert front.illustration_id == "810f9359-c82f-4962-9f42-0d0a79ee4cae"

    # Image URIs
    assert front.image_uris.art_crop.startswith("https://cards.scryfall.io/art_crop/")
    assert front.image_uris.border_crop.startswith("https://cards.scryfall.io/border_crop/")
    assert front.image_uris.large.startswith("https://cards.scryfall.io/large/")
    assert front.image_uris.normal.startswith("https://cards.scryfall.io/normal/")
    assert front.image_uris.png.startswith("https://cards.scryfall.io/png/")
    assert front.image_uris.small.startswith("https://cards.scryfall.io/small/")

    assert front.layout is None
    assert front.loyalty == "4"
    assert front.mana_cost == "{2}{R}{G}"
    assert front.name == "Arlinn, the Pack's Hope"
    assert front.oracle_id is None
    assert front.oracle_text == oracle_arlinn_the_packs_hope
    assert front.power is None
    assert front.printed_name is None
    assert front.printed_text is None
    assert front.printed_type_line is None
    assert front.toughness is None
    assert front.type_line == "Legendary Planeswalker — Arlinn"
    assert front.watermark is None

    ## Back
    assert back.artist == "Anna Steinbauer"
    assert back.cmc is None
    assert back.color_indicator == {Color.RED, Color.GREEN}
    assert back.colors == {Color.RED, Color.GREEN}
    assert back.flavor_text is None
    assert back.illustration_id == "9d3b73cb-6d91-48f1-ab96-89971207556d"

    # ImageURIs
    assert back.image_uris.art_crop.startswith("https://cards.scryfall.io/art_crop/")
    assert back.image_uris.border_crop.startswith("https://cards.scryfall.io/border_crop/")
    assert back.image_uris.large.startswith("https://cards.scryfall.io/large/")
    assert back.image_uris.normal.startswith("https://cards.scryfall.io/normal/")
    assert back.image_uris.png.startswith("https://cards.scryfall.io/png/")
    assert back.image_uris.small.startswith("https://cards.scryfall.io/small/")
    assert back.layout is None
    assert back.loyalty == "4"
    assert back.mana_cost == ""
    assert back.name == "Arlinn, the Moon's Fury"
    assert back.oracle_id is None
    assert back.oracle_text == oracle_arlinn_the_moons_fury
    assert back.power is None
    assert back.printed_name is None
    assert back.printed_text is None
    assert back.printed_type_line is None
    assert back.toughness is None
    assert back.type_line == "Legendary Planeswalker — Arlinn"
    assert back.watermark is None


def test_fullcard_from_json_digital(json_urzas_construction_drone):
    # TODO: fill test
    card = FullCard.from_json(json_urzas_construction_drone)
    pass


# endregion

# endregion


# region json -> CardModel

# region CardModel


def test_cardmodel_from_json_instant(json_ancestral_recall, legalities_ancestral_recall):
    model = CardModel.model_validate(json_ancestral_recall)
    assert model.cmc == 1.0
    assert model.color_identity == {Color.BLUE}
    assert model.colors == {Color.BLUE}
    assert model.legalities == legalities_ancestral_recall
    assert model.mana_cost == "{U}"
    assert model.name == "Ancestral Recall"
    assert model.power == ""
    assert model.toughness == ""
    assert model.type_line == "Instant"


# TODO: add tests for the other cards

# endregion

# region FullCardModel


def test_fullcardmodel_from_json_instant(json_ancestral_recall, legalities_ancestral_recall):
    model = FullCardModel.model_validate(json_ancestral_recall)
    pprint(model.model_dump())
    assert model.all_parts is None
    assert model.arena_id is None
    assert model.artist == "Ryan Pancoast"
    assert model.attraction_lights is None
    assert model.booster == True
    assert model.border_color == BorderColor.BLACK
    assert model.card_back_id == "0aeebaf5-8c7d-4636-9e82-8c27447861f7"
    assert model.card_faces is None
    assert model.cardmarket_id is None
    assert model.cmc == 1.0
    assert model.collector_number == "1"
    assert model.color_identity == {Color.BLUE}
    assert model.color_indicator is None
    assert model.colors == {Color.BLUE}
    assert model.content_warning == False
    assert model.digital == True
    assert model.edhrec_rank is None
    assert model.finishes == {Finish.NONFOIL, Finish.FOIL}
    assert model.flavor_name is None
    assert model.flavor_text is None
    assert model.frame == "2015"
    assert model.frame_effects is None
    assert model.full_art == False
    assert model.games == {Game.MTGO}
    assert model.hand_modifier is None
    assert model.highres_image == True
    assert model.illustation_id == ""
    assert model.image_status == "highres_scan"

    # ImageURIs
    assert model.image_uris.art_crop.startswith("https://cards.scryfall.io/art_crop/")
    assert model.image_uris.border_crop.startswith("https://cards.scryfall.io/border_crop/")
    assert model.image_uris.large.startswith("https://cards.scryfall.io/large/")
    assert model.image_uris.normal.startswith("https://cards.scryfall.io/normal/")
    assert model.image_uris.png.startswith("https://cards.scryfall.io/png/")
    assert model.image_uris.small.startswith("https://cards.scryfall.io/small/")

    assert model.keywords == set()
    assert model.lang == "en"
    assert model.layout == "normal"
    assert model.legalities == legalities_ancestral_recall
    assert model.life_modifier is None
    assert model.loyalty is None
    assert model.mana_cost == "{U}"
    assert model.mtgo_foil_id == 53178
    assert model.mtgo_id == 53177
    assert model.multiverse_ids == [382841]
    assert model.name == "Ancestral Recall"
    assert model.oracle_id == "550c74d4-1fcb-406a-b02a-639a760a4380"
    assert model.oracle_text == "Target player draws three cards."
    assert model.oversized == False
    assert model.penny_rank is None
    assert model.power == ""
    assert model.preview is None
    assert model.prices is not None  # TODO: is this the best way to do this?

    #  'prices': {'eur': None,
    #             'tix': 1.9,
    #             'usd': None,
    #             'usd_etched': None,
    #             'usd_foil': None},

    assert model.printed_name is None
    assert model.printed_text is None
    assert model.printed_type_line is None
    assert model.prints_search_uri.startswith("https://api.scryfall.com/cards/")
    assert model.produced_mana is None
    assert model.promo == False
    assert model.promo_types is None

    # PurchaseURIs
    assert model.purchase_uris["cardhoarder"].startswith("https://www.cardhoarder.com/")
    assert model.purchase_uris["cardmarket"].startswith("https://www.cardmarket.com/")
    assert model.purchase_uris["tcgplayer"].startswith("https://www.tcgplayer.com/")

    assert model.rarity == Rarity.BONUS

    # RelatedURIs
    assert model.related_uris["edhrec"].startswith("https://edhrec.com/")
    assert model.related_uris["gatherer"].startswith("https://gatherer.wizards.com/")
    assert model.related_uris["tcgplayer_infinite_articles"].startswith("https://infinite.tcgplayer.com/")
    assert model.related_uris["tcgplayer_infinite_decks"].startswith("https://infinite.tcgplayer.com/")

    assert model.released_at == date(year=2014, month=6, day=16)
    assert model.reprint == True
    assert model.reserved == True
    assert model.rulings_uri.startswith("https://api.scryfall.com/cards/")
    assert model.scryfall_id == "2398892d-28e9-4009-81ec-0d544af79d2b"
    assert model.scryfall_set_uri.startswith("https://scryfall.com/sets/")
    assert model.scryfall_uri.startswith("https://scryfall.com/card/")
    assert model.security_stamp == "oval"
    assert model.set == "vma"
    assert model.set_id == "a944551a-73fa-41cd-9159-e8d0e4674403"
    assert model.set_name == "Vintage Masters"
    assert model.set_search_uri.startswith("https://api.scryfall.com/cards/search?")
    assert model.set_type == "masters"
    assert model.set_uri.startswith("https://api.scryfall.com/sets/")
    assert model.story_spotlight == False
    assert model.tcgplayer_etched_id is None
    assert model.tcgplayer_id is None
    assert model.textless == False
    assert model.toughness == ""
    assert model.type_line == "Instant"
    assert model.uri.startswith("https://api.scryfall.com/cards/")
    assert model.variation == False
    assert model.variation_of is None
    assert model.watermark is None


# TODO: add tests for the other cards

# endregion

# endregion


# region CardModel -> Card Object

# region CardModel -> Card


def test_card_from_cardmodel_instant(json_ancestral_recall):
    pass


# TODO: add tests for the other cards

# endregion

# region FullCardModel -> FullCard

# TODO: add tests for the other cards

# endregion

# endregion
