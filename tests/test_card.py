from datetime import date

import pytest
from scooze.card import Card, FullCard, OracleCard
from scooze.enums import (
    BorderColor,
    Color,
    Component,
    Finish,
    Format,
    Frame,
    FrameEffect,
    Game,
    ImageStatus,
    Language,
    Layout,
    Legality,
    Rarity,
    SecurityStamp,
    SetType,
)
from scooze.models.card import CardModel, FullCardModel

# TODO: remove NOTE s and TODO s from this file.
# helpful little jq that can get you a card from one of the bulk files. You can get scryfall_id from the card's json
# ╰─❯ cat data/bulk/oracle_cards.json | jq '.[] | select(.id == "371ceb58-f498-4616-a7f0-eb118fe2e4ff")' > ./data/bulk/card.json

# STUFF TO WORK THROUGH:
# TODO:
#  - Move fixtures to conftest or similar. We don't want to get_card_from_json every time
#  - Split up Card vs CardModel tests into the right test files
# Notes about further coverage:
#  - Need a card with a watermark I think
#  - Need a card with `printed_name` `printed_type_line` `printed_text`
#  - Need a card with `flavor_name` and `flavor_text`
#  - Need a card with `attraction_lights`
#  - Need a card with `variation` and `variation_of`

# region Fixtures


@pytest.fixture
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


@pytest.fixture
def legalities_token() -> dict[Format, Legality]:
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


@pytest.fixture
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


@pytest.fixture
def oracle_tales_of_master_seshiro() -> str:
    return (
        "(As this Saga enters and after your draw step, add a lore counter.)\n"
        "I, II — Put a +1/+1 counter on target creature or Vehicle you control. It "
        "gains vigilance until end of turn.\n"
        "III — Exile this Saga, then return it to the battlefield transformed under "
        "your control."
    )


@pytest.fixture
def oracle_arlinn_the_packs_hope() -> str:
    return (
        "Daybound (If a player casts no spells during their own turn, it becomes "
        "night next turn.)\n"
        "+1: Until your next turn, you may cast creature spells as though they had "
        "flash, and each creature you control enters the battlefield with an "
        "additional +1/+1 counter on it.\n"
        "−3: Create two 2/2 green Wolf creature tokens."
    )


@pytest.fixture
def oracle_arlinn_the_moons_fury() -> str:
    return (
        "Nightbound (If a player casts at least two spells during their own turn, it "
        "becomes day next turn.)\n"
        "+2: Add {R}{G}.\n"
        "0: Until end of turn, Arlinn, the Moon's Fury becomes a 5/5 Werewolf "
        "creature with trample, indestructible, and haste."
    )


@pytest.fixture
def oracle_zndrsplt_eye_of_wisdom() -> str:
    return (
        "Partner with Okaun, Eye of Chaos (When this creature enters the "
        "battlefield, target player may put Okaun into their hand from their "
        "library, then shuffle.)\n"
        "At the beginning of combat on your turn, flip a coin until you lose a "
        "flip.\n"
        "Whenever a player wins a coin flip, draw a card."
    )


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


def test_card_from_json_costless(json_ancestral_visions):
    card = Card.from_json(json_ancestral_visions)
    assert card.cmc == 0.0
    assert card.color_identity == {Color.BLUE}
    assert card.colors == {Color.BLUE}
    assert card.mana_cost == ""
    assert card.type_line == "Sorcery"


def test_card_from_json_token(json_snake_token, legalities_token):
    card = Card.from_json(json_snake_token)
    assert card.cmc == 0.0
    assert card.color_identity == {Color.BLUE, Color.GREEN}
    assert card.colors == {Color.BLUE, Color.GREEN}
    assert card.legalities == legalities_token
    assert card.mana_cost == ""
    assert card.name == "Snake"
    assert card.power == "1"
    assert card.toughness == "1"
    assert card.type_line == "Token Creature — Snake"


# endregion

# region OracleCard


def test_oraclecard_from_json_instant(json_ancestral_recall, legalities_ancestral_recall):
    card = OracleCard.from_json(json_ancestral_recall)
    assert card.card_faces is None
    assert card.cmc == 1.0
    assert card.color_identity == {Color.BLUE}
    assert card.color_indicator is None
    assert card.colors == {Color.BLUE}
    assert card.edhrec_rank is None
    assert card.hand_modifier is None
    assert card.keywords == set()
    assert card.legalities == legalities_ancestral_recall
    assert card.life_modifier is None
    assert card.loyalty is None
    assert card.mana_cost == "{U}"
    assert card.name == "Ancestral Recall"
    assert card.oracle_id == "550c74d4-1fcb-406a-b02a-639a760a4380"
    assert card.oracle_text == "Target player draws three cards."
    assert card.penny_rank is None
    assert card.power is None
    assert card.prints_search_uri.startswith("https://api.scryfall.com/cards/search?")
    assert card.produced_mana is None
    assert card.reserved == True
    assert card.rulings_uri.startswith("https://api.scryfall.com/cards/")
    assert card.toughness is None
    assert card.type_line == "Instant"


def test_oraclecard_from_json_costless(json_ancestral_visions):
    card = OracleCard.from_json(json_ancestral_visions)
    assert card.color_indicator == {Color.BLUE}
    assert card.keywords == {"Suspend"}


def test_oraclecard_from_json_transform_saga(json_tales_of_master_seshiro, oracle_tales_of_master_seshiro):
    card = OracleCard.from_json(json_tales_of_master_seshiro)
    assert len(card.card_faces) == 2
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


# endregion

# region FullCard


def test_fullcard_from_json_instant(json_ancestral_recall, legalities_ancestral_recall):
    card = FullCard.from_json(json_ancestral_recall)
    assert card.all_parts is None
    assert card.arena_id is None
    assert card.artist == "Ryan Pancoast"
    assert card.artist_ids == ["89cc9475-dda2-4d13-bf88-54b92867a25c"]
    assert card.attraction_lights is None
    assert card.booster == True
    assert card.border_color == BorderColor.BLACK
    assert card.card_back_id == "0aeebaf5-8c7d-4636-9e82-8c27447861f7"
    assert card.card_faces is None
    assert card.cardmarket_id is None
    assert card.cmc == 1.0
    assert card.collector_number == "1"
    assert card.color_identity == {Color.BLUE}
    assert card.color_indicator is None
    assert card.colors == {Color.BLUE}
    assert card.content_warning is None
    assert card.digital == True
    assert card.edhrec_rank is None
    assert card.finishes == {Finish.NONFOIL, Finish.FOIL}
    assert card.flavor_name is None
    assert card.flavor_text is None
    assert card.frame == Frame._2015
    assert card.frame_effects is None
    assert card.full_art == False
    assert card.games == {Game.MTGO}
    assert card.hand_modifier is None
    assert card.highres_image == True
    assert card.illustration_id == "95c5ab6f-fcce-4e21-9e02-cc1d922adfae"
    assert card.image_status == ImageStatus.HIGHRES_SCAN

    # ImageUris
    assert card.image_uris.art_crop.startswith("https://cards.scryfall.io/art_crop/")
    assert card.image_uris.border_crop.startswith("https://cards.scryfall.io/border_crop/")
    assert card.image_uris.large.startswith("https://cards.scryfall.io/large/")
    assert card.image_uris.normal.startswith("https://cards.scryfall.io/normal/")
    assert card.image_uris.png.startswith("https://cards.scryfall.io/png/")
    assert card.image_uris.small.startswith("https://cards.scryfall.io/small/")

    assert card.keywords == set()
    assert card.lang == Language.ENGLISH
    assert card.layout == Layout.NORMAL
    assert card.legalities == legalities_ancestral_recall
    assert card.life_modifier is None
    assert card.loyalty is None
    assert card.mana_cost == "{U}"
    assert card.mtgo_foil_id == 53178
    assert card.mtgo_id == 53177
    assert card.multiverse_ids == [382841]
    assert card.name == "Ancestral Recall"
    assert card.oracle_id == "550c74d4-1fcb-406a-b02a-639a760a4380"
    assert card.oracle_text == "Target player draws three cards."
    assert card.oversized == False
    assert card.penny_rank is None
    assert card.power is None
    assert card.preview is None

    # Prices
    assert card.prices.eur is None
    assert card.prices.eur_foil is None
    assert card.prices.tix == 1.9
    assert card.prices.usd is None
    assert card.prices.usd_etched is None
    assert card.prices.usd_foil is None

    assert card.printed_name is None
    assert card.printed_text is None
    assert card.printed_type_line is None
    assert card.prints_search_uri.startswith("https://api.scryfall.com/cards/search?")
    assert card.produced_mana is None
    assert card.promo == False
    assert card.promo_types is None

    # PurchaseUris
    assert card.purchase_uris["cardhoarder"].startswith("https://www.cardhoarder.com/")
    assert card.purchase_uris["cardmarket"].startswith("https://www.cardmarket.com/")
    assert card.purchase_uris["tcgplayer"].startswith("https://www.tcgplayer.com/")

    assert card.rarity == Rarity.BONUS

    # RelatedUris
    assert card.related_uris["edhrec"].startswith("https://edhrec.com/")
    assert card.related_uris["gatherer"].startswith("https://gatherer.wizards.com/")
    assert card.related_uris["tcgplayer_infinite_articles"].startswith("https://infinite.tcgplayer.com/")
    assert card.related_uris["tcgplayer_infinite_decks"].startswith("https://infinite.tcgplayer.com/")

    assert card.released_at == date(year=2014, month=6, day=16)
    assert card.reprint == True
    assert card.reserved == True
    assert card.rulings_uri.startswith("https://api.scryfall.com/cards/")
    assert card.scryfall_id == "2398892d-28e9-4009-81ec-0d544af79d2b"
    assert card.scryfall_set_uri.startswith("https://scryfall.com/sets/")
    assert card.scryfall_uri.startswith("https://scryfall.com/card/")
    assert card.security_stamp == SecurityStamp.OVAL
    assert card.set == "vma"
    assert card.set_id == "a944551a-73fa-41cd-9159-e8d0e4674403"
    assert card.set_name == "Vintage Masters"
    assert card.set_search_uri.startswith("https://api.scryfall.com/cards/search?")
    assert card.set_type == SetType.MASTERS
    assert card.set_uri.startswith("https://api.scryfall.com/sets/")
    assert card.story_spotlight == False
    assert card.tcgplayer_etched_id is None
    assert card.tcgplayer_id is None
    assert card.textless == False
    assert card.toughness is None
    assert card.type_line == "Instant"
    assert card.uri.startswith("https://api.scryfall.com/cards/")
    assert card.variation == False
    assert card.variation_of is None
    assert card.watermark is None


def test_fullcard_from_json_transform_planeswalker(
    json_arlinn_the_packs_hope, oracle_arlinn_the_packs_hope, oracle_arlinn_the_moons_fury
):
    card = FullCard.from_json(json_arlinn_the_packs_hope)
    assert len(card.card_faces) == 2
    front, back = card.card_faces

    ## Front
    assert front.artist == "Anna Steinbauer"
    assert front.artist_id == "3516496c-c279-4b56-8239-720683d03ae0"
    assert front.cmc is None
    assert front.color_indicator is None
    assert front.colors == {Color.RED, Color.GREEN}
    assert front.flavor_text is None
    assert front.illustration_id == "810f9359-c82f-4962-9f42-0d0a79ee4cae"

    # Image Uris
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
    assert back.artist_id == "3516496c-c279-4b56-8239-720683d03ae0"
    assert back.cmc is None
    assert back.color_indicator == {Color.RED, Color.GREEN}
    assert back.colors == {Color.RED, Color.GREEN}
    assert back.flavor_text is None
    assert back.illustration_id == "9d3b73cb-6d91-48f1-ab96-89971207556d"

    # ImageUris
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
    card = FullCard.from_json(json_urzas_construction_drone)
    assert card.digital == True
    assert card.games == {Game.ARENA}
    assert card.highres_image == False
    assert card.image_status == ImageStatus.LOWRES
    assert card.keywords == {"Conjure", "Seek"}


def test_fullcard_from_json_reversible(
    json_zndrsplt_eye_of_wisdom, legalities_zndrsplt_eye_of_wisdom, oracle_zndrsplt_eye_of_wisdom
):
    card = FullCard.from_json(json_zndrsplt_eye_of_wisdom)

    # all_parts (RelatedCards)
    assert len(card.all_parts) == 2
    r1, r2 = card.all_parts
    # RelatedCard 1
    assert r1.component == Component.COMBO_PIECE
    assert r1.name == "Zndrsplt, Eye of Wisdom // Zndrsplt, Eye of Wisdom"
    assert r1.scryfall_id == "e25ce640-baf5-442b-8b75-d05dd9fb20dd"
    assert r1.type_line == "Legendary Creature — Homunculus // Legendary Creature — Homunculus"
    assert r1.uri.startswith("https://api.scryfall.com/cards/")
    # RelatedCard 2
    assert r2.component == Component.COMBO_PIECE
    assert r2.name == "Okaun, Eye of Chaos // Okaun, Eye of Chaos"
    assert r2.scryfall_id == "8421ad46-dc7f-4b66-800b-e41c30835300"
    assert r2.type_line == "Legendary Creature — Cyclops Berserker // Legendary Creature — Cyclops Berserker"
    assert r2.uri.startswith("https://api.scryfall.com/cards/")

    assert card.arena_id is None
    assert card.artist == "Alexis Ziritt"
    assert card.artist_ids == ["add4cc84-9254-4c0b-8fcd-af4a238bdbd5"]
    assert card.attraction_lights is None
    assert card.booster == False
    assert card.border_color == BorderColor.BORDERLESS
    assert card.card_back_id is None

    assert len(card.card_faces) == 2
    front, back = card.card_faces

    ## Front
    assert front.artist == "Alexis Ziritt"
    assert front.artist_id == "add4cc84-9254-4c0b-8fcd-af4a238bdbd5"
    assert front.cmc == 5.0
    assert front.color_indicator is None
    assert front.colors == {Color.BLUE}
    assert front.flavor_text is None
    assert front.illustration_id == "6d336a32-95a6-4a15-964c-358f11500f0a"

    # ImageUris
    assert front.image_uris.art_crop.startswith("https://cards.scryfall.io/art_crop/")
    assert front.image_uris.border_crop.startswith("https://cards.scryfall.io/border_crop/")
    assert front.image_uris.large.startswith("https://cards.scryfall.io/large/")
    assert front.image_uris.normal.startswith("https://cards.scryfall.io/normal/")
    assert front.image_uris.png.startswith("https://cards.scryfall.io/png/")
    assert front.image_uris.small.startswith("https://cards.scryfall.io/small/")

    assert front.layout == Layout.NORMAL
    assert front.loyalty is None
    assert front.mana_cost == "{4}{U}"
    assert front.name == "Zndrsplt, Eye of Wisdom"
    assert front.oracle_id == "502849a6-8e65-40f3-b348-a41c4f939768"
    assert front.oracle_text == oracle_zndrsplt_eye_of_wisdom
    assert front.power == "1"
    assert front.printed_name is None
    assert front.printed_text is None
    assert front.printed_type_line is None
    assert front.toughness == "4"
    assert front.type_line == "Legendary Creature — Homunculus"
    assert front.watermark is None

    ## Back
    assert back.artist == "Alexis Ziritt"
    assert back.artist_id == "add4cc84-9254-4c0b-8fcd-af4a238bdbd5"
    assert back.cmc == 5.0
    assert back.color_indicator is None
    assert back.colors == {Color.BLUE}
    assert back.flavor_text is None
    assert back.illustration_id == "c5e6cb8f-c7bd-4ba7-988f-1332bd6d595b"

    # ImageUris
    assert back.image_uris.art_crop.startswith("https://cards.scryfall.io/art_crop/")
    assert back.image_uris.border_crop.startswith("https://cards.scryfall.io/border_crop/")
    assert back.image_uris.large.startswith("https://cards.scryfall.io/large/")
    assert back.image_uris.normal.startswith("https://cards.scryfall.io/normal/")
    assert back.image_uris.png.startswith("https://cards.scryfall.io/png/")
    assert back.image_uris.small.startswith("https://cards.scryfall.io/small/")

    assert back.layout == Layout.NORMAL
    assert back.loyalty is None
    assert back.mana_cost == "{4}{U}"
    assert back.name == "Zndrsplt, Eye of Wisdom"
    assert back.oracle_id == "502849a6-8e65-40f3-b348-a41c4f939768"
    assert back.oracle_text == oracle_zndrsplt_eye_of_wisdom
    assert back.power == "1"
    assert back.printed_name is None
    assert back.printed_text is None
    assert back.printed_type_line is None
    assert back.toughness == "4"
    assert back.type_line == "Legendary Creature — Homunculus"
    assert back.watermark is None

    assert card.cardmarket_id is None
    assert card.cmc is None
    assert card.collector_number == "379"
    assert card.color_identity == {Color.BLUE}
    assert card.color_indicator is None
    assert card.colors is None
    assert card.content_warning is None
    assert card.digital == False
    assert card.edhrec_rank == 8719
    assert card.finishes == {Finish.FOIL}
    assert card.flavor_name is None
    assert card.flavor_text is None
    assert card.frame == Frame._2015
    assert card.frame_effects == {FrameEffect.INVERTED, FrameEffect.LEGENDARY}
    assert card.full_art == False
    assert card.games == {Game.PAPER}
    assert card.hand_modifier is None
    assert card.highres_image == True
    assert card.illustration_id is None
    assert card.image_status == ImageStatus.HIGHRES_SCAN
    assert card.image_uris is None
    assert card.keywords == {"Partner", "Partner with"}
    assert card.lang == Language.ENGLISH
    assert card.layout == Layout.REVERSIBLE_CARD
    assert card.legalities == legalities_zndrsplt_eye_of_wisdom
    assert card.life_modifier is None
    assert card.loyalty is None
    assert card.mana_cost is None
    assert card.mtgo_foil_id is None
    assert card.mtgo_id is None
    assert card.multiverse_ids == []
    assert card.name == "Zndrsplt, Eye of Wisdom // Zndrsplt, Eye of Wisdom"
    assert card.oracle_id is None
    assert card.oracle_text is None
    assert card.oversized == False
    assert card.penny_rank is None
    assert card.power is None
    assert card.preview is None

    # Prices
    assert card.prices.eur is None
    assert card.prices.eur_foil is None
    assert card.prices.tix is None
    assert card.prices.usd is None
    assert card.prices.usd_etched is None
    assert card.prices.usd_foil == 5.23

    assert card.printed_name is None
    assert card.printed_text is None
    assert card.printed_type_line is None
    assert card.prints_search_uri.startswith("https://api.scryfall.com/cards/search?")
    assert card.produced_mana is None
    assert card.promo == False
    assert card.promo_types is None

    # PurchaseUris
    assert card.purchase_uris["cardhoarder"].startswith("https://www.cardhoarder.com/")
    assert card.purchase_uris["cardmarket"].startswith("https://www.cardmarket.com/")
    assert card.purchase_uris["tcgplayer"].startswith("https://www.tcgplayer.com/")

    assert card.rarity == Rarity.RARE

    # RelatedUris
    assert card.related_uris["edhrec"].startswith("https://edhrec.com/")
    assert card.related_uris["tcgplayer_infinite_articles"].startswith("https://infinite.tcgplayer.com/")
    assert card.related_uris["tcgplayer_infinite_decks"].startswith("https://infinite.tcgplayer.com/")

    assert card.released_at == date(year=2022, month=4, day=22)
    assert card.reprint == True
    assert card.reserved == False
    assert card.rulings_uri.startswith("https://api.scryfall.com/cards/")
    assert card.scryfall_id == "d5dfd236-b1da-4552-b94f-ebf6bb9dafdf"
    assert card.scryfall_uri.startswith("https://scryfall.com/card/")
    assert card.security_stamp == SecurityStamp.OVAL
    assert card.set == "sld"
    assert card.set_id == "4d92a8a7-ccb0-437d-abdc-9d70fc5ed672"
    assert card.set_name == "Secret Lair Drop"
    assert card.set_search_uri.startswith("https://api.scryfall.com/cards/search?")
    assert card.set_type == SetType.BOX
    assert card.set_uri.startswith("https://api.scryfall.com/sets/")
    assert card.tcgplayer_etched_id is None
    assert card.tcgplayer_id == 259216
    assert card.textless == False
    assert card.toughness is None
    assert card.type_line is None
    assert card.uri.startswith("https://api.scryfall.com/cards/")
    assert card.variation == False
    assert card.variation_of is None
    assert card.watermark is None


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
    assert model.power == None
    assert model.toughness == None
    assert model.type_line == "Instant"


def test_cardmodel_from_json_creature(json_mystic_snake):
    model = CardModel.model_validate(json_mystic_snake)
    assert model.color_identity == {Color.BLUE, Color.GREEN}
    assert model.colors == {Color.BLUE, Color.GREEN}
    assert model.power == "2"
    assert model.toughness == "2"
    assert model.type_line == "Creature — Snake"


def test_cardmodel_from_json_token(json_snake_token, legalities_token):
    model = CardModel.model_validate(json_snake_token)
    assert model.cmc == 0.0
    assert model.color_identity == {Color.BLUE, Color.GREEN}
    assert model.colors == {Color.BLUE, Color.GREEN}
    assert model.legalities == legalities_token
    assert model.mana_cost == ""
    assert model.name == "Snake"
    assert model.power == "1"
    assert model.toughness == "1"
    assert model.type_line == "Token Creature — Snake"


# endregion

# region FullCardModel


def test_fullcardmodel_from_json_instant(json_ancestral_recall, legalities_ancestral_recall):
    model = FullCardModel.model_validate(json_ancestral_recall)
    assert model.all_parts is None
    assert model.arena_id is None
    assert model.artist == "Ryan Pancoast"
    assert model.artist_ids == ["89cc9475-dda2-4d13-bf88-54b92867a25c"]
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
    assert model.frame == Frame._2015
    assert model.frame_effects is None
    assert model.full_art == False
    assert model.games == {Game.MTGO}
    assert model.hand_modifier is None
    assert model.highres_image == True
    assert model.illustration_id == "95c5ab6f-fcce-4e21-9e02-cc1d922adfae"
    assert model.image_status == ImageStatus.HIGHRES_SCAN

    # ImageUris
    assert model.image_uris.art_crop.startswith("https://cards.scryfall.io/art_crop/")
    assert model.image_uris.border_crop.startswith("https://cards.scryfall.io/border_crop/")
    assert model.image_uris.large.startswith("https://cards.scryfall.io/large/")
    assert model.image_uris.normal.startswith("https://cards.scryfall.io/normal/")
    assert model.image_uris.png.startswith("https://cards.scryfall.io/png/")
    assert model.image_uris.small.startswith("https://cards.scryfall.io/small/")

    assert model.keywords == set()
    assert model.lang == Language.ENGLISH
    assert model.layout == Layout.NORMAL
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
    assert model.power == None
    assert model.preview is None

    # Prices
    assert model.prices.eur is None
    assert model.prices.eur_foil is None
    assert model.prices.tix == 1.9
    assert model.prices.usd is None
    assert model.prices.usd_etched is None
    assert model.prices.usd_foil is None

    assert model.printed_name is None
    assert model.printed_text is None
    assert model.printed_type_line is None
    assert model.prints_search_uri.startswith("https://api.scryfall.com/cards/")
    assert model.produced_mana is None
    assert model.promo == False
    assert model.promo_types is None

    # PurchaseUris
    assert model.purchase_uris["cardhoarder"].startswith("https://www.cardhoarder.com/")
    assert model.purchase_uris["cardmarket"].startswith("https://www.cardmarket.com/")
    assert model.purchase_uris["tcgplayer"].startswith("https://www.tcgplayer.com/")

    assert model.rarity == Rarity.BONUS

    # RelatedUris
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
    assert model.security_stamp == SecurityStamp.OVAL
    assert model.set == "vma"
    assert model.set_id == "a944551a-73fa-41cd-9159-e8d0e4674403"
    assert model.set_name == "Vintage Masters"
    assert model.set_search_uri.startswith("https://api.scryfall.com/cards/search?")
    assert model.set_type == SetType.MASTERS
    assert model.set_uri.startswith("https://api.scryfall.com/sets/")
    assert model.story_spotlight == False
    assert model.tcgplayer_etched_id is None
    assert model.tcgplayer_id is None
    assert model.textless == False
    assert model.toughness == None
    assert model.type_line == "Instant"
    assert model.uri.startswith("https://api.scryfall.com/cards/")
    assert model.variation == False
    assert model.variation_of is None
    assert model.watermark is None


def test_fullcardmodel_from_json_transform_planeswalker(
    json_arlinn_the_packs_hope, oracle_arlinn_the_packs_hope, oracle_arlinn_the_moons_fury
):
    model = FullCardModel.model_validate(json_arlinn_the_packs_hope)

    assert len(model.card_faces) == 2
    front, back = model.card_faces

    ## Front
    assert front.artist == "Anna Steinbauer"
    assert front.artist_id == "3516496c-c279-4b56-8239-720683d03ae0"
    assert front.cmc is None
    assert front.color_indicator is None
    assert front.colors == {Color.RED, Color.GREEN}
    assert front.flavor_text is None
    assert front.illustration_id == "810f9359-c82f-4962-9f42-0d0a79ee4cae"

    # Image Uris
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
    assert back.artist_id == "3516496c-c279-4b56-8239-720683d03ae0"
    assert back.cmc is None
    assert back.color_indicator == {Color.RED, Color.GREEN}
    assert back.colors == {Color.RED, Color.GREEN}
    assert back.flavor_text is None
    assert back.illustration_id == "9d3b73cb-6d91-48f1-ab96-89971207556d"

    # ImageUris
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


def test_fullcardmodel_from_json_reversible(
    json_zndrsplt_eye_of_wisdom, legalities_zndrsplt_eye_of_wisdom, oracle_zndrsplt_eye_of_wisdom
):
    model = FullCardModel.model_validate(json_zndrsplt_eye_of_wisdom)

    # all_parts (RelatedCards)
    assert len(model.all_parts) == 2
    r1, r2 = model.all_parts
    # RelatedCard 1
    assert r1.component == Component.COMBO_PIECE
    assert r1.name == "Zndrsplt, Eye of Wisdom // Zndrsplt, Eye of Wisdom"
    assert r1.scryfall_id == "e25ce640-baf5-442b-8b75-d05dd9fb20dd"
    assert r1.type_line == "Legendary Creature — Homunculus // Legendary Creature — Homunculus"
    assert r1.uri.startswith("https://api.scryfall.com/cards/")
    # RelatedCard 2
    assert r2.component == Component.COMBO_PIECE
    assert r2.name == "Okaun, Eye of Chaos // Okaun, Eye of Chaos"
    assert r2.scryfall_id == "8421ad46-dc7f-4b66-800b-e41c30835300"
    assert r2.type_line == "Legendary Creature — Cyclops Berserker // Legendary Creature — Cyclops Berserker"
    assert r2.uri.startswith("https://api.scryfall.com/cards/")

    assert model.arena_id is None
    assert model.artist == "Alexis Ziritt"
    assert model.artist_ids == ["add4cc84-9254-4c0b-8fcd-af4a238bdbd5"]
    assert model.attraction_lights is None
    assert model.booster == False
    assert model.border_color == BorderColor.BORDERLESS
    assert model.card_back_id == ""

    assert len(model.card_faces) == 2
    front, back = model.card_faces

    ## Front
    assert front.artist == "Alexis Ziritt"
    assert front.artist_id == "add4cc84-9254-4c0b-8fcd-af4a238bdbd5"
    assert front.cmc == 5.0
    assert front.color_indicator is None
    assert front.colors == {Color.BLUE}
    assert front.flavor_text is None
    assert front.illustration_id == "6d336a32-95a6-4a15-964c-358f11500f0a"

    # ImageUris
    assert front.image_uris.art_crop.startswith("https://cards.scryfall.io/art_crop/")
    assert front.image_uris.border_crop.startswith("https://cards.scryfall.io/border_crop/")
    assert front.image_uris.large.startswith("https://cards.scryfall.io/large/")
    assert front.image_uris.normal.startswith("https://cards.scryfall.io/normal/")
    assert front.image_uris.png.startswith("https://cards.scryfall.io/png/")
    assert front.image_uris.small.startswith("https://cards.scryfall.io/small/")

    assert front.layout == Layout.NORMAL
    assert front.loyalty is None
    assert front.mana_cost == "{4}{U}"
    assert front.name == "Zndrsplt, Eye of Wisdom"
    assert front.oracle_id == "502849a6-8e65-40f3-b348-a41c4f939768"
    assert front.oracle_text == oracle_zndrsplt_eye_of_wisdom
    assert front.power == "1"
    assert front.printed_name is None
    assert front.printed_text is None
    assert front.printed_type_line is None
    assert front.toughness == "4"
    assert front.type_line == "Legendary Creature — Homunculus"
    assert front.watermark is None

    ## Back
    assert back.artist == "Alexis Ziritt"
    assert back.artist_id == "add4cc84-9254-4c0b-8fcd-af4a238bdbd5"
    assert back.cmc == 5.0
    assert back.color_indicator is None
    assert back.colors == {Color.BLUE}
    assert back.flavor_text is None
    assert back.illustration_id == "c5e6cb8f-c7bd-4ba7-988f-1332bd6d595b"

    # ImageUris
    assert back.image_uris.art_crop.startswith("https://cards.scryfall.io/art_crop/")
    assert back.image_uris.border_crop.startswith("https://cards.scryfall.io/border_crop/")
    assert back.image_uris.large.startswith("https://cards.scryfall.io/large/")
    assert back.image_uris.normal.startswith("https://cards.scryfall.io/normal/")
    assert back.image_uris.png.startswith("https://cards.scryfall.io/png/")
    assert back.image_uris.small.startswith("https://cards.scryfall.io/small/")

    assert back.layout == Layout.NORMAL
    assert back.loyalty is None
    assert back.mana_cost == "{4}{U}"
    assert back.name == "Zndrsplt, Eye of Wisdom"
    assert back.oracle_id == "502849a6-8e65-40f3-b348-a41c4f939768"
    assert back.oracle_text == oracle_zndrsplt_eye_of_wisdom
    assert back.power == "1"
    assert back.printed_name is None
    assert back.printed_text is None
    assert back.printed_type_line is None
    assert back.toughness == "4"
    assert back.type_line == "Legendary Creature — Homunculus"
    assert back.watermark is None

    assert model.cardmarket_id is None
    assert model.cmc is None
    assert model.collector_number == "379"
    assert model.color_identity == {Color.BLUE}
    assert model.color_indicator is None
    assert model.colors is None
    assert model.content_warning == False
    assert model.digital == False
    assert model.edhrec_rank == 8719
    assert model.finishes == {Finish.FOIL}
    assert model.flavor_name is None
    assert model.flavor_text is None
    assert model.frame == Frame._2015
    assert model.frame_effects == {FrameEffect.INVERTED, FrameEffect.LEGENDARY}
    assert model.full_art == False
    assert model.games == {Game.PAPER}
    assert model.hand_modifier is None
    assert model.highres_image == True
    assert model.illustration_id is None
    assert model.image_status == ImageStatus.HIGHRES_SCAN
    assert model.image_uris is None
    assert model.keywords == {"Partner", "Partner with"}
    assert model.lang == Language.ENGLISH
    assert model.layout == Layout.REVERSIBLE_CARD
    assert model.legalities == legalities_zndrsplt_eye_of_wisdom
    assert model.life_modifier is None
    assert model.loyalty is None
    assert model.mana_cost == ""
    assert model.mtgo_foil_id is None
    assert model.mtgo_id is None
    assert model.multiverse_ids == []
    assert model.name == "Zndrsplt, Eye of Wisdom // Zndrsplt, Eye of Wisdom"
    assert model.oracle_id is None
    assert model.oracle_text is None
    assert model.oversized == False
    assert model.penny_rank is None
    assert model.power is None
    assert model.preview is None

    # Prices
    assert model.prices.eur is None
    assert model.prices.eur_foil is None
    assert model.prices.tix is None
    assert model.prices.usd is None
    assert model.prices.usd_etched is None
    assert model.prices.usd_foil == 5.23

    assert model.printed_name is None
    assert model.printed_text is None
    assert model.printed_type_line is None
    assert model.prints_search_uri.startswith("https://api.scryfall.com/cards/search?")
    assert model.produced_mana is None
    assert model.promo == False
    assert model.promo_types is None

    # PurchaseUris
    assert model.purchase_uris["cardhoarder"].startswith("https://www.cardhoarder.com/")
    assert model.purchase_uris["cardmarket"].startswith("https://www.cardmarket.com/")
    assert model.purchase_uris["tcgplayer"].startswith("https://www.tcgplayer.com/")

    assert model.rarity == Rarity.RARE

    # RelatedUris
    assert model.related_uris["edhrec"].startswith("https://edhrec.com/")
    assert model.related_uris["tcgplayer_infinite_articles"].startswith("https://infinite.tcgplayer.com/")
    assert model.related_uris["tcgplayer_infinite_decks"].startswith("https://infinite.tcgplayer.com/")

    assert model.released_at == date(year=2022, month=4, day=22)
    assert model.reprint == True
    assert model.reserved == False
    assert model.rulings_uri.startswith("https://api.scryfall.com/cards/")
    assert model.scryfall_id == "d5dfd236-b1da-4552-b94f-ebf6bb9dafdf"
    assert model.scryfall_uri.startswith("https://scryfall.com/card/")
    assert model.security_stamp == SecurityStamp.OVAL
    assert model.set == "sld"
    assert model.set_id == "4d92a8a7-ccb0-437d-abdc-9d70fc5ed672"
    assert model.set_name == "Secret Lair Drop"
    assert model.set_search_uri.startswith("https://api.scryfall.com/cards/search?")
    assert model.set_type == SetType.BOX
    assert model.set_uri.startswith("https://api.scryfall.com/sets/")
    assert model.tcgplayer_etched_id is None
    assert model.tcgplayer_id == 259216
    assert model.textless == False
    assert model.toughness is None
    assert model.type_line == ""
    assert model.uri.startswith("https://api.scryfall.com/cards/")
    assert model.variation == False
    assert model.variation_of is None
    assert model.watermark is None


# endregion

# endregion


# region CardModel -> Card Object

# region CardModel -> Card


def test_card_from_cardmodel_instant(json_ancestral_recall, legalities_ancestral_recall):
    model = CardModel.model_validate(json_ancestral_recall)
    card = Card.from_model(model)
    assert card.cmc == 1.0
    assert card.color_identity == {Color.BLUE}
    assert card.colors == {Color.BLUE}
    assert card.legalities == legalities_ancestral_recall
    assert card.mana_cost == "{U}"
    assert card.name == "Ancestral Recall"
    assert card.power is None
    assert card.toughness is None
    assert card.type_line == "Instant"


def test_card_from_cardmodel_creature(json_mystic_snake):
    model = CardModel.model_validate(json_mystic_snake)
    card = Card.from_model(model)
    assert card.color_identity == {Color.BLUE, Color.GREEN}
    assert card.colors == {Color.BLUE, Color.GREEN}
    assert card.power == "2"
    assert card.toughness == "2"
    assert card.type_line == "Creature — Snake"


# NOTE: just to see if going from FullCardModel -> Card works alright
def test_card_from_fullcardmodel_instant(json_ancestral_recall, legalities_ancestral_recall):
    model = FullCardModel.model_validate(json_ancestral_recall)
    card = Card.from_model(model)
    assert card.cmc == 1.0
    assert card.color_identity == {Color.BLUE}
    assert card.colors == {Color.BLUE}
    assert card.legalities == legalities_ancestral_recall
    assert card.mana_cost == "{U}"
    assert card.name == "Ancestral Recall"
    assert card.power is None
    assert card.toughness is None
    assert card.type_line == "Instant"


# endregion

# region FullCardModel -> OracleCard


def test_oraclecard_from_fullcardmodel_instant(json_ancestral_recall, legalities_ancestral_recall):
    model = FullCardModel.model_validate(json_ancestral_recall)
    card = OracleCard.from_model(model)
    assert card.card_faces is None
    assert card.cmc == 1.0
    assert card.color_identity == {Color.BLUE}
    assert card.color_indicator is None
    assert card.colors == {Color.BLUE}
    assert card.edhrec_rank is None
    assert card.hand_modifier is None
    assert card.keywords == set()
    assert card.legalities == legalities_ancestral_recall
    assert card.life_modifier is None
    assert card.loyalty is None
    assert card.mana_cost == "{U}"
    assert card.name == "Ancestral Recall"
    assert card.oracle_id == "550c74d4-1fcb-406a-b02a-639a760a4380"
    assert card.oracle_text == "Target player draws three cards."
    assert card.penny_rank is None
    assert card.power is None
    assert card.prints_search_uri.startswith("https://api.scryfall.com/cards/search?")
    assert card.produced_mana is None
    assert card.reserved == True
    assert card.rulings_uri.startswith("https://api.scryfall.com/cards/")
    assert card.toughness is None
    assert card.type_line == "Instant"


def test_oraclecard_from_fullcardmodel_transform_saga(json_tales_of_master_seshiro, oracle_tales_of_master_seshiro):
    model = FullCardModel.model_validate(json_tales_of_master_seshiro)
    card = OracleCard.from_model(model)
    assert len(card.card_faces) == 2
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


# endregion

# region FullCardModel -> FullCard


def test_fullcard_from_fullcardmodel_instant(json_ancestral_recall, legalities_ancestral_recall):
    model = FullCardModel.model_validate(json_ancestral_recall)
    card = FullCard.from_model(model)
    assert card.all_parts is None
    assert card.arena_id is None
    assert card.artist == "Ryan Pancoast"
    assert card.artist_ids == ["89cc9475-dda2-4d13-bf88-54b92867a25c"]
    assert card.attraction_lights is None
    assert card.booster == True
    assert card.border_color == BorderColor.BLACK
    assert card.card_back_id == "0aeebaf5-8c7d-4636-9e82-8c27447861f7"
    assert card.card_faces is None
    assert card.cardmarket_id is None
    assert card.cmc == 1.0
    assert card.collector_number == "1"
    assert card.color_identity == {Color.BLUE}
    assert card.color_indicator is None
    assert card.colors == {Color.BLUE}
    assert card.content_warning == False
    assert card.digital == True
    assert card.edhrec_rank is None
    assert card.finishes == {Finish.NONFOIL, Finish.FOIL}
    assert card.flavor_name is None
    assert card.flavor_text is None
    assert card.frame == Frame._2015
    assert card.frame_effects is None
    assert card.full_art == False
    assert card.games == {Game.MTGO}
    assert card.hand_modifier is None
    assert card.highres_image == True
    assert card.illustration_id == "95c5ab6f-fcce-4e21-9e02-cc1d922adfae"
    assert card.image_status == ImageStatus.HIGHRES_SCAN

    # ImageUris
    assert card.image_uris.art_crop.startswith("https://cards.scryfall.io/art_crop/")
    assert card.image_uris.border_crop.startswith("https://cards.scryfall.io/border_crop/")
    assert card.image_uris.large.startswith("https://cards.scryfall.io/large/")
    assert card.image_uris.normal.startswith("https://cards.scryfall.io/normal/")
    assert card.image_uris.png.startswith("https://cards.scryfall.io/png/")
    assert card.image_uris.small.startswith("https://cards.scryfall.io/small/")

    assert card.keywords == set()
    assert card.lang == Language.ENGLISH
    assert card.layout == Layout.NORMAL
    assert card.legalities == legalities_ancestral_recall
    assert card.life_modifier is None
    assert card.loyalty is None
    assert card.mana_cost == "{U}"
    assert card.mtgo_foil_id == 53178
    assert card.mtgo_id == 53177
    assert card.multiverse_ids == [382841]
    assert card.name == "Ancestral Recall"
    assert card.oracle_id == "550c74d4-1fcb-406a-b02a-639a760a4380"
    assert card.oracle_text == "Target player draws three cards."
    assert card.oversized == False
    assert card.penny_rank is None
    assert card.power is None
    assert card.preview is None

    # Prices
    assert card.prices.eur is None
    assert card.prices.eur_foil is None
    assert card.prices.tix == 1.9
    assert card.prices.usd is None
    assert card.prices.usd_etched is None
    assert card.prices.usd_foil is None

    assert card.printed_name is None
    assert card.printed_text is None
    assert card.printed_type_line is None
    assert card.prints_search_uri.startswith("https://api.scryfall.com/cards/search?")
    assert card.produced_mana is None
    assert card.promo == False
    assert card.promo_types is None

    # PurchaseUris
    assert card.purchase_uris["cardhoarder"].startswith("https://www.cardhoarder.com/")
    assert card.purchase_uris["cardmarket"].startswith("https://www.cardmarket.com/")
    assert card.purchase_uris["tcgplayer"].startswith("https://www.tcgplayer.com/")

    assert card.rarity == Rarity.BONUS

    # RelatedUris
    assert card.related_uris["edhrec"].startswith("https://edhrec.com/")
    assert card.related_uris["gatherer"].startswith("https://gatherer.wizards.com/")
    assert card.related_uris["tcgplayer_infinite_articles"].startswith("https://infinite.tcgplayer.com/")
    assert card.related_uris["tcgplayer_infinite_decks"].startswith("https://infinite.tcgplayer.com/")

    assert card.released_at == date(year=2014, month=6, day=16)
    assert card.reprint == True
    assert card.reserved == True
    assert card.rulings_uri.startswith("https://api.scryfall.com/cards/")
    assert card.scryfall_id == "2398892d-28e9-4009-81ec-0d544af79d2b"
    assert card.scryfall_set_uri.startswith("https://scryfall.com/sets/")
    assert card.scryfall_uri.startswith("https://scryfall.com/card/")
    assert card.security_stamp == SecurityStamp.OVAL
    assert card.set == "vma"
    assert card.set_id == "a944551a-73fa-41cd-9159-e8d0e4674403"
    assert card.set_name == "Vintage Masters"
    assert card.set_search_uri.startswith("https://api.scryfall.com/cards/search?")
    assert card.set_type == SetType.MASTERS
    assert card.set_uri.startswith("https://api.scryfall.com/sets/")
    assert card.story_spotlight == False
    assert card.tcgplayer_etched_id is None
    assert card.tcgplayer_id is None
    assert card.textless == False
    assert card.toughness is None
    assert card.type_line == "Instant"
    assert card.uri.startswith("https://api.scryfall.com/cards/")
    assert card.variation == False
    assert card.variation_of is None
    assert card.watermark is None


def test_fullcard_from_fullcardmodel_transform_planeswalker(
    json_arlinn_the_packs_hope, oracle_arlinn_the_packs_hope, oracle_arlinn_the_moons_fury
):
    model = FullCardModel.model_validate(json_arlinn_the_packs_hope)
    card = FullCard.from_model(model)
    assert len(card.card_faces) == 2
    front, back = card.card_faces

    ## Front
    assert front.artist == "Anna Steinbauer"
    assert front.artist_id == "3516496c-c279-4b56-8239-720683d03ae0"
    assert front.cmc is None
    assert front.color_indicator is None
    assert front.colors == {Color.RED, Color.GREEN}
    assert front.flavor_text is None
    assert front.illustration_id == "810f9359-c82f-4962-9f42-0d0a79ee4cae"

    # Image Uris
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
    assert back.artist_id == "3516496c-c279-4b56-8239-720683d03ae0"
    assert back.cmc is None
    assert back.color_indicator == {Color.RED, Color.GREEN}
    assert back.colors == {Color.RED, Color.GREEN}
    assert back.flavor_text is None
    assert back.illustration_id == "9d3b73cb-6d91-48f1-ab96-89971207556d"

    # ImageUris
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


def test_fullcard_from_fullcardmodel_reversible(
    json_zndrsplt_eye_of_wisdom, legalities_zndrsplt_eye_of_wisdom, oracle_zndrsplt_eye_of_wisdom
):
    model = FullCardModel.model_validate(json_zndrsplt_eye_of_wisdom)
    card = FullCard.from_model(model)

    # all_parts (RelatedCards)
    assert len(card.all_parts) == 2
    r1, r2 = card.all_parts
    # RelatedCard 1
    assert r1.component == Component.COMBO_PIECE
    assert r1.name == "Zndrsplt, Eye of Wisdom // Zndrsplt, Eye of Wisdom"
    assert r1.scryfall_id == "e25ce640-baf5-442b-8b75-d05dd9fb20dd"
    assert r1.type_line == "Legendary Creature — Homunculus // Legendary Creature — Homunculus"
    assert r1.uri.startswith("https://api.scryfall.com/cards/")
    # RelatedCard 2
    assert r2.component == Component.COMBO_PIECE
    assert r2.name == "Okaun, Eye of Chaos // Okaun, Eye of Chaos"
    assert r2.scryfall_id == "8421ad46-dc7f-4b66-800b-e41c30835300"
    assert r2.type_line == "Legendary Creature — Cyclops Berserker // Legendary Creature — Cyclops Berserker"
    assert r2.uri.startswith("https://api.scryfall.com/cards/")

    assert card.arena_id is None
    assert card.artist == "Alexis Ziritt"
    assert card.artist_ids == ["add4cc84-9254-4c0b-8fcd-af4a238bdbd5"]
    assert card.attraction_lights is None
    assert card.booster == False
    assert card.border_color == BorderColor.BORDERLESS
    assert card.card_back_id is ""

    assert len(card.card_faces) == 2
    front, back = card.card_faces

    ## Front
    assert front.artist == "Alexis Ziritt"
    assert front.artist_id == "add4cc84-9254-4c0b-8fcd-af4a238bdbd5"
    assert front.cmc == 5.0
    assert front.color_indicator is None
    assert front.colors == {Color.BLUE}
    assert front.flavor_text is None
    assert front.illustration_id == "6d336a32-95a6-4a15-964c-358f11500f0a"

    # ImageUris
    assert front.image_uris.art_crop.startswith("https://cards.scryfall.io/art_crop/")
    assert front.image_uris.border_crop.startswith("https://cards.scryfall.io/border_crop/")
    assert front.image_uris.large.startswith("https://cards.scryfall.io/large/")
    assert front.image_uris.normal.startswith("https://cards.scryfall.io/normal/")
    assert front.image_uris.png.startswith("https://cards.scryfall.io/png/")
    assert front.image_uris.small.startswith("https://cards.scryfall.io/small/")

    assert front.layout == Layout.NORMAL
    assert front.loyalty is None
    assert front.mana_cost == "{4}{U}"
    assert front.name == "Zndrsplt, Eye of Wisdom"
    assert front.oracle_id == "502849a6-8e65-40f3-b348-a41c4f939768"
    assert front.oracle_text == oracle_zndrsplt_eye_of_wisdom
    assert front.power == "1"
    assert front.printed_name is None
    assert front.printed_text is None
    assert front.printed_type_line is None
    assert front.toughness == "4"
    assert front.type_line == "Legendary Creature — Homunculus"
    assert front.watermark is None

    ## Back
    assert back.artist == "Alexis Ziritt"
    assert back.artist_id == "add4cc84-9254-4c0b-8fcd-af4a238bdbd5"
    assert back.cmc == 5.0
    assert back.color_indicator is None
    assert back.colors == {Color.BLUE}
    assert back.flavor_text is None
    assert back.illustration_id == "c5e6cb8f-c7bd-4ba7-988f-1332bd6d595b"

    # ImageUris
    assert back.image_uris.art_crop.startswith("https://cards.scryfall.io/art_crop/")
    assert back.image_uris.border_crop.startswith("https://cards.scryfall.io/border_crop/")
    assert back.image_uris.large.startswith("https://cards.scryfall.io/large/")
    assert back.image_uris.normal.startswith("https://cards.scryfall.io/normal/")
    assert back.image_uris.png.startswith("https://cards.scryfall.io/png/")
    assert back.image_uris.small.startswith("https://cards.scryfall.io/small/")

    assert back.layout == Layout.NORMAL
    assert back.loyalty is None
    assert back.mana_cost == "{4}{U}"
    assert back.name == "Zndrsplt, Eye of Wisdom"
    assert back.oracle_id == "502849a6-8e65-40f3-b348-a41c4f939768"
    assert back.oracle_text == oracle_zndrsplt_eye_of_wisdom
    assert back.power == "1"
    assert back.printed_name is None
    assert back.printed_text is None
    assert back.printed_type_line is None
    assert back.toughness == "4"
    assert back.type_line == "Legendary Creature — Homunculus"
    assert back.watermark is None

    assert card.cardmarket_id is None
    assert card.cmc is None
    assert card.collector_number == "379"
    assert card.color_identity == {Color.BLUE}
    assert card.color_indicator is None
    assert card.colors is None
    assert card.content_warning == False
    assert card.digital == False
    assert card.edhrec_rank == 8719
    assert card.finishes == {Finish.FOIL}
    assert card.flavor_name is None
    assert card.flavor_text is None
    assert card.frame == Frame._2015
    assert card.frame_effects == {FrameEffect.INVERTED, FrameEffect.LEGENDARY}
    assert card.full_art == False
    assert card.games == {Game.PAPER}
    assert card.hand_modifier is None
    assert card.highres_image == True
    assert card.illustration_id is None
    assert card.image_status == ImageStatus.HIGHRES_SCAN
    assert card.image_uris is None
    assert card.keywords == {"Partner", "Partner with"}
    assert card.lang == Language.ENGLISH
    assert card.layout == Layout.REVERSIBLE_CARD
    assert card.legalities == legalities_zndrsplt_eye_of_wisdom
    assert card.life_modifier is None
    assert card.loyalty is None
    assert card.mana_cost == ""
    assert card.mtgo_foil_id is None
    assert card.mtgo_id is None
    assert card.multiverse_ids == []
    assert card.name == "Zndrsplt, Eye of Wisdom // Zndrsplt, Eye of Wisdom"
    assert card.oracle_id is None
    assert card.oracle_text is None
    assert card.oversized == False
    assert card.penny_rank is None
    assert card.power is None
    assert card.preview is None

    # Prices
    assert card.prices.eur is None
    assert card.prices.eur_foil is None
    assert card.prices.tix is None
    assert card.prices.usd is None
    assert card.prices.usd_etched is None
    assert card.prices.usd_foil == 5.23

    assert card.printed_name is None
    assert card.printed_text is None
    assert card.printed_type_line is None
    assert card.prints_search_uri.startswith("https://api.scryfall.com/cards/search?")
    assert card.produced_mana is None
    assert card.promo == False
    assert card.promo_types is None

    # PurchaseUris
    assert card.purchase_uris["cardhoarder"].startswith("https://www.cardhoarder.com/")
    assert card.purchase_uris["cardmarket"].startswith("https://www.cardmarket.com/")
    assert card.purchase_uris["tcgplayer"].startswith("https://www.tcgplayer.com/")

    assert card.rarity == Rarity.RARE

    # RelatedUris
    assert card.related_uris["edhrec"].startswith("https://edhrec.com/")
    assert card.related_uris["tcgplayer_infinite_articles"].startswith("https://infinite.tcgplayer.com/")
    assert card.related_uris["tcgplayer_infinite_decks"].startswith("https://infinite.tcgplayer.com/")

    assert card.released_at == date(year=2022, month=4, day=22)
    assert card.reprint == True
    assert card.reserved == False
    assert card.rulings_uri.startswith("https://api.scryfall.com/cards/")
    assert card.scryfall_id == "d5dfd236-b1da-4552-b94f-ebf6bb9dafdf"
    assert card.scryfall_uri.startswith("https://scryfall.com/card/")
    assert card.security_stamp == SecurityStamp.OVAL
    assert card.set == "sld"
    assert card.set_id == "4d92a8a7-ccb0-437d-abdc-9d70fc5ed672"
    assert card.set_name == "Secret Lair Drop"
    assert card.set_search_uri.startswith("https://api.scryfall.com/cards/search?")
    assert card.set_type == SetType.BOX
    assert card.set_uri.startswith("https://api.scryfall.com/sets/")
    assert card.tcgplayer_etched_id is None
    assert card.tcgplayer_id == 259216
    assert card.textless == False
    assert card.toughness is None
    assert card.type_line == ""
    assert card.uri.startswith("https://api.scryfall.com/cards/")
    assert card.variation == False
    assert card.variation_of is None
    assert card.watermark is None


# endregion

# endregion
