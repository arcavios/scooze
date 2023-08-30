from datetime import date

from scooze.card import Card, FullCard, OracleCard
from scooze.enums import (
    BorderColor,
    Color,
    Component,
    Finish,
    Frame,
    FrameEffect,
    Game,
    ImageStatus,
    Language,
    Layout,
    Rarity,
    SecurityStamp,
    SetType,
)
from scooze.models.card import CardModel, FullCardModel

# region eq and ne


def test_card_eq():
    card = Card(name="Test Card")
    card2 = Card(name="Test Card")
    card3 = Card(name="Another Card")
    assert card == card2
    assert not card == card3


def test_card_ne():
    card = Card(name="Test Card")
    card2 = Card(name="Test Card")
    card3 = Card(name="Another Card")
    assert not card != card2
    assert card != card3


def test_oraclecard_eq():
    card = OracleCard(name="Test Card")
    card2 = OracleCard(name="Test Card")
    card3 = OracleCard(name="Another Card")
    assert card == card2
    assert not card == card3


def test_oraclecard_ne():
    card = OracleCard(name="Test Card")
    card2 = OracleCard(name="Test Card")
    card3 = OracleCard(name="Another Card")
    assert not card != card2
    assert card != card3


def test_fullcard_eq():
    card = FullCard(name="Test Card")
    card2 = FullCard(name="Test Card")
    card3 = FullCard(name="Another Card")
    assert card == card2
    assert not card == card3


def test_fullcard_ne():
    card = FullCard(name="Test Card")
    card2 = FullCard(name="Test Card")
    card3 = FullCard(name="Another Card")
    assert not card != card2
    assert card != card3


# endregion


# region Hash


def test_card_hash(json_anaconda_7ed_foil, json_anaconda_portal):
    a7 = Card.from_json(json_anaconda_7ed_foil)
    assert {a7: "value"}[a7] == "value"
    ap = Card.from_json(json_anaconda_portal)
    assert hash(a7) == hash(ap)  # all Card-level fields are the same
    a7_clone = Card.from_json(json_anaconda_7ed_foil)
    assert hash(a7) == hash(a7_clone)


def test_oraclecard_hash(json_anaconda_7ed_foil, json_anaconda_portal):
    a7 = OracleCard.from_json(json_anaconda_7ed_foil)
    assert {a7: "value"}[a7] == "value"
    ap = OracleCard.from_json(json_anaconda_portal)
    assert hash(a7) != hash(ap)
    a7_clone = OracleCard.from_json(json_anaconda_7ed_foil)
    assert hash(a7) == hash(a7_clone)


def test_fullcard_hash(json_anaconda_7ed_foil, json_anaconda_portal):
    a7 = FullCard.from_json(json_anaconda_7ed_foil)
    assert {a7: "value"}[a7] == "value"
    ap = FullCard.from_json(json_anaconda_portal)
    assert hash(a7) != hash(ap)
    a7_clone = FullCard.from_json(json_anaconda_7ed_foil)
    assert hash(a7) == hash(a7_clone)


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
    assert card.keywords == frozenset()
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
    assert card.artist_ids == tuple(["89cc9475-dda2-4d13-bf88-54b92867a25c"])
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

    assert card.keywords == frozenset()
    assert card.lang == Language.ENGLISH
    assert card.layout == Layout.NORMAL
    assert card.legalities == legalities_ancestral_recall
    assert card.life_modifier is None
    assert card.loyalty is None
    assert card.mana_cost == "{U}"
    assert card.mtgo_foil_id == 53178
    assert card.mtgo_id == 53177
    assert card.multiverse_ids == tuple([382841])
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
    assert card.artist_ids == tuple(["add4cc84-9254-4c0b-8fcd-af4a238bdbd5"])
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
    assert card.multiverse_ids == tuple([])
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


def test_fullcard_from_json_watermark(json_anaconda_7ed_foil):
    card = FullCard.from_json(json_anaconda_7ed_foil)
    assert card.watermark == "wotc"


def test_fullcard_from_json_non_english(json_python_spanish):
    card = FullCard.from_json(json_python_spanish)
    assert card.printed_name == "Pitón"


def test_fullcard_from_json_flavor(json_elessar_the_elfstone):
    card = FullCard.from_json(json_elessar_the_elfstone)
    assert card.flavor_name == "Elessar, the Elfstone"
    assert card.flavor_text == "Aragorn took the green stone and held it up, and there came a green fire from his hand."
    assert card.name == "Cloudstone Curio"


def test_fullcard_from_json_attraction(json_trash_bin):
    card = FullCard.from_json(json_trash_bin)
    assert card.attraction_lights == {2, 6}


def test_fullcard_from_json_variation(json_anaconda_portal):
    card = FullCard.from_json(json_anaconda_portal)
    assert card.variation == True
    assert card.variation_of == "0a2012ad-6425-4935-83af-fc7309ec2ece"  # Anaconda


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
    assert card.keywords == frozenset()
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
    assert card.artist_ids == tuple(["89cc9475-dda2-4d13-bf88-54b92867a25c"])
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

    assert card.keywords == frozenset()
    assert card.lang == Language.ENGLISH
    assert card.layout == Layout.NORMAL
    assert card.legalities == legalities_ancestral_recall
    assert card.life_modifier is None
    assert card.loyalty is None
    assert card.mana_cost == "{U}"
    assert card.mtgo_foil_id == 53178
    assert card.mtgo_id == 53177
    assert card.multiverse_ids == tuple([382841])
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
    assert card.artist_ids == tuple(["add4cc84-9254-4c0b-8fcd-af4a238bdbd5"])
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
    assert card.multiverse_ids == tuple([])
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


def test_fullcard_from_fullcardmodel_watermark(json_anaconda_7ed_foil):
    card = FullCardModel.model_validate(json_anaconda_7ed_foil)
    assert card.watermark == "wotc"


def test_fullcardmodel_from_fullcardmodel_non_english(json_python_spanish):
    card = FullCardModel.model_validate(json_python_spanish)
    assert card.printed_name == "Pitón"


def test_fullcardmodel_from_fullcardmodel_flavor(json_elessar_the_elfstone):
    card = FullCardModel.model_validate(json_elessar_the_elfstone)
    assert card.flavor_name == "Elessar, the Elfstone"
    assert card.flavor_text == "Aragorn took the green stone and held it up, and there came a green fire from his hand."
    assert card.name == "Cloudstone Curio"


def test_fullcardmodel_from_fullcardmodel_attraction(json_trash_bin):
    card = FullCardModel.model_validate(json_trash_bin)
    assert card.attraction_lights == {2, 6}


def test_fullcardmodel_from_fullcardmodel_variation(json_anaconda_portal):
    card = FullCardModel.model_validate(json_anaconda_portal)
    assert card.variation == True
    assert card.variation_of == "0a2012ad-6425-4935-83af-fc7309ec2ece"  # Anaconda


# endregion

# endregion
