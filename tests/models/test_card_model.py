from datetime import date

from httpx import AsyncClient
from scooze.card import FullCard
from scooze.catalogs import (
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
from scooze.enums import DbCollection
from scooze.models.card import CardModel, CardModelData

# region eq and ne


def test_cardmodel_eq():
    card = CardModel.model_construct(name="Test Card")
    card2 = CardModel.model_construct(name="Test Card")
    card3 = CardModel.model_construct(name="Another Card")
    assert card == card2
    assert not card == card3


def test_cardmodel_ne():
    card = CardModel.model_construct(name="Test Card")
    card2 = CardModel.model_construct(name="Test Card")
    card3 = CardModel.model_construct(name="Another Card")
    assert not card != card2
    assert card != card3


# endregion

# region CardModel


def test_cardmodel_beanie(api_client: AsyncClient):
    card = CardModel.model_construct(name="Test Card")
    assert card.get_motor_collection().name == DbCollection.CARDS


# endregion


# region CardModelData

# region from_json


def test_cardmodeldata_from_json_instant(json_ancestral_recall, legalities_ancestral_recall):
    model = CardModelData.model_validate(json_ancestral_recall)
    assert model.all_parts is None
    assert model.arena_id is None
    assert model.artist == "Ryan Pancoast"
    assert model.artist_ids == ["89cc9475-dda2-4d13-bf88-54b92867a25c"]
    assert model.attraction_lights is None
    assert model.booster is True
    assert model.border_color is BorderColor.BLACK
    assert model.card_back_id == "0aeebaf5-8c7d-4636-9e82-8c27447861f7"
    assert model.card_faces is None
    assert model.cardmarket_id is None
    assert model.cmc == 1.0
    assert model.collector_number == "1"
    assert model.color_identity == {Color.BLUE}
    assert model.color_indicator is None
    assert model.colors == {Color.BLUE}
    assert model.content_warning is False
    assert model.digital is True
    assert model.edhrec_rank is None
    assert model.finishes == {Finish.NONFOIL, Finish.FOIL}
    assert model.flavor_name is None
    assert model.flavor_text is None
    assert model.frame is Frame._2015
    assert model.frame_effects is None
    assert model.full_art is False
    assert model.games == {Game.MTGO}
    assert model.hand_modifier is None
    assert model.highres_image is True
    assert model.illustration_id == "95c5ab6f-fcce-4e21-9e02-cc1d922adfae"
    assert model.image_status is ImageStatus.HIGHRES_SCAN

    # ImageUris
    assert model.image_uris.art_crop.startswith("https://cards.scryfall.io/art_crop/")
    assert model.image_uris.border_crop.startswith("https://cards.scryfall.io/border_crop/")
    assert model.image_uris.large.startswith("https://cards.scryfall.io/large/")
    assert model.image_uris.normal.startswith("https://cards.scryfall.io/normal/")
    assert model.image_uris.png.startswith("https://cards.scryfall.io/png/")
    assert model.image_uris.small.startswith("https://cards.scryfall.io/small/")

    assert model.keywords == set()
    assert model.lang is Language.ENGLISH
    assert model.layout is Layout.NORMAL
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
    assert model.oversized is False
    assert model.penny_rank is None
    assert model.power is None
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
    assert model.promo is False
    assert model.promo_types is None

    # PurchaseUris
    assert model.purchase_uris.cardhoarder.startswith("https://www.cardhoarder.com/")
    assert model.purchase_uris.cardmarket.startswith("https://www.cardmarket.com/")
    assert model.purchase_uris.tcgplayer.startswith("https://www.tcgplayer.com/")

    assert model.rarity is Rarity.BONUS

    # RelatedUris
    assert model.related_uris.edhrec.startswith("https://edhrec.com/")
    assert model.related_uris.gatherer.startswith("https://gatherer.wizards.com/")
    assert model.related_uris.tcgplayer_infinite_articles.startswith("https://infinite.tcgplayer.com/")
    assert model.related_uris.tcgplayer_infinite_decks.startswith("https://infinite.tcgplayer.com/")

    assert model.released_at == date(year=2014, month=6, day=16)
    assert model.reprint is True
    assert model.reserved is True
    assert model.rulings_uri.startswith("https://api.scryfall.com/cards/")
    assert model.scryfall_id == "2398892d-28e9-4009-81ec-0d544af79d2b"
    assert model.scryfall_set_uri.startswith("https://scryfall.com/sets/")
    assert model.scryfall_uri.startswith("https://scryfall.com/card/")
    assert model.security_stamp is SecurityStamp.OVAL
    assert model.set_code == "vma"
    assert model.set_id == "a944551a-73fa-41cd-9159-e8d0e4674403"
    assert model.set_name == "Vintage Masters"
    assert model.set_search_uri.startswith("https://api.scryfall.com/cards/search?")
    assert model.set_type is SetType.MASTERS
    assert model.set_uri.startswith("https://api.scryfall.com/sets/")
    assert model.story_spotlight is False
    assert model.tcgplayer_etched_id is None
    assert model.tcgplayer_id is None
    assert model.textless is False
    assert model.toughness is None
    assert model.type_line == "Instant"
    assert model.uri.startswith("https://api.scryfall.com/cards/")
    assert model.variation is False
    assert model.variation_of is None
    assert model.watermark is None


def test_cardmodeldata_from_json_transform_planeswalker(
    json_arlinn_the_packs_hope, oracle_arlinn_daybound, oracle_arlinn_nightbound
):
    model = CardModelData.model_validate(json_arlinn_the_packs_hope)

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
    assert front.oracle_text == oracle_arlinn_daybound
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
    assert back.oracle_text == oracle_arlinn_nightbound
    assert back.power is None
    assert back.printed_name is None
    assert back.printed_text is None
    assert back.printed_type_line is None
    assert back.toughness is None
    assert back.type_line == "Legendary Planeswalker — Arlinn"
    assert back.watermark is None


def test_cardmodeldata_from_json_reversible(
    json_zndrsplt_eye_of_wisdom, legalities_zndrsplt_eye_of_wisdom, oracle_zndrsplt_eye_of_wisdom
):
    model = CardModelData.model_validate(json_zndrsplt_eye_of_wisdom)

    # all_parts (RelatedCards)
    assert len(model.all_parts) == 2
    r1, r2 = model.all_parts
    # RelatedCard 1
    assert r1.component is Component.COMBO_PIECE
    assert r1.name == "Zndrsplt, Eye of Wisdom // Zndrsplt, Eye of Wisdom"
    assert r1.scryfall_id == "e25ce640-baf5-442b-8b75-d05dd9fb20dd"
    assert r1.type_line == "Legendary Creature — Homunculus // Legendary Creature — Homunculus"
    assert r1.uri.startswith("https://api.scryfall.com/cards/")
    # RelatedCard 2
    assert r2.component is Component.COMBO_PIECE
    assert r2.name == "Okaun, Eye of Chaos // Okaun, Eye of Chaos"
    assert r2.scryfall_id == "8421ad46-dc7f-4b66-800b-e41c30835300"
    assert r2.type_line == "Legendary Creature — Cyclops Berserker // Legendary Creature — Cyclops Berserker"
    assert r2.uri.startswith("https://api.scryfall.com/cards/")

    assert model.arena_id is None
    assert model.artist == "Alexis Ziritt"
    assert model.artist_ids == ["add4cc84-9254-4c0b-8fcd-af4a238bdbd5"]
    assert model.attraction_lights is None
    assert model.booster is False
    assert model.border_color is BorderColor.BORDERLESS
    assert model.card_back_id is None

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

    assert front.layout is Layout.NORMAL
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

    assert back.layout is Layout.NORMAL
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
    assert model.content_warning is False
    assert model.digital is False
    assert model.edhrec_rank == 8719
    assert model.finishes == {Finish.FOIL}
    assert model.flavor_name is None
    assert model.flavor_text is None
    assert model.frame is Frame._2015
    assert model.frame_effects == {FrameEffect.INVERTED, FrameEffect.LEGENDARY}
    assert model.full_art is False
    assert model.games == {Game.PAPER}
    assert model.hand_modifier is None
    assert model.highres_image is True
    assert model.illustration_id is None
    assert model.image_status is ImageStatus.HIGHRES_SCAN
    assert model.image_uris is None
    assert model.keywords == {"Partner", "Partner with"}
    assert model.lang is Language.ENGLISH
    assert model.layout is Layout.REVERSIBLE_CARD
    assert model.legalities == legalities_zndrsplt_eye_of_wisdom
    assert model.life_modifier is None
    assert model.loyalty is None
    assert model.mana_cost is None
    assert model.mtgo_foil_id is None
    assert model.mtgo_id is None
    assert model.multiverse_ids == []
    assert model.name == "Zndrsplt, Eye of Wisdom // Zndrsplt, Eye of Wisdom"
    assert model.oracle_id is None
    assert model.oracle_text is None
    assert model.oversized is False
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
    assert model.promo is False
    assert model.promo_types is None

    # PurchaseUris
    assert model.purchase_uris.cardhoarder.startswith("https://www.cardhoarder.com/")
    assert model.purchase_uris.cardmarket.startswith("https://www.cardmarket.com/")
    assert model.purchase_uris.tcgplayer.startswith("https://www.tcgplayer.com/")

    assert model.rarity is Rarity.RARE

    # RelatedUris
    assert model.related_uris.edhrec.startswith("https://edhrec.com/")
    assert model.related_uris.tcgplayer_infinite_articles.startswith("https://infinite.tcgplayer.com/")
    assert model.related_uris.tcgplayer_infinite_decks.startswith("https://infinite.tcgplayer.com/")

    assert model.released_at == date(year=2022, month=4, day=22)
    assert model.reprint is True
    assert model.reserved is False
    assert model.rulings_uri.startswith("https://api.scryfall.com/cards/")
    assert model.scryfall_id == "d5dfd236-b1da-4552-b94f-ebf6bb9dafdf"
    assert model.scryfall_uri.startswith("https://scryfall.com/card/")
    assert model.security_stamp is SecurityStamp.OVAL
    assert model.set_code == "sld"
    assert model.set_id == "4d92a8a7-ccb0-437d-abdc-9d70fc5ed672"
    assert model.set_name == "Secret Lair Drop"
    assert model.set_search_uri.startswith("https://api.scryfall.com/cards/search?")
    assert model.set_type is SetType.BOX
    assert model.set_uri.startswith("https://api.scryfall.com/sets/")
    assert model.tcgplayer_etched_id is None
    assert model.tcgplayer_id == 259216
    assert model.textless is False
    assert model.toughness is None
    assert model.type_line is None
    assert model.uri.startswith("https://api.scryfall.com/cards/")
    assert model.variation is False
    assert model.variation_of is None
    assert model.watermark is None


def test_cardmodeldata_from_json_creature(json_mystic_snake):
    model = CardModelData.model_validate(json_mystic_snake)
    assert model.color_identity == {Color.BLUE, Color.GREEN}
    assert model.colors == {Color.BLUE, Color.GREEN}
    assert model.power == "2"
    assert model.toughness == "2"
    assert model.type_line == "Creature — Snake"


def test_cardmodeldata_from_json_token(json_snake_token, legalities_token):
    model = CardModelData.model_validate(json_snake_token)
    assert model.cmc == 0.0
    assert model.color_identity == {Color.BLUE, Color.GREEN}
    assert model.colors == {Color.BLUE, Color.GREEN}
    assert model.legalities == legalities_token
    assert model.mana_cost == ""
    assert model.name == "Snake"
    assert model.power == "1"
    assert model.toughness == "1"
    assert model.type_line == "Token Creature — Snake"


def test_cardmodeldata_from_json_watermark(json_anaconda_7ed_foil):
    model = CardModelData.model_validate(json_anaconda_7ed_foil)
    assert model.watermark == "wotc"


def test_cardmodeldata_from_json_non_english(json_python_spanish):
    model = CardModelData.model_validate(json_python_spanish)
    assert model.printed_name == "Pitón"


def test_cardmodeldata_from_json_flavor(json_elessar_the_elfstone):
    model = CardModelData.model_validate(json_elessar_the_elfstone)
    assert model.flavor_name == "Elessar, the Elfstone"
    assert (
        model.flavor_text == "Aragorn took the green stone and held it up, and there came a green fire from his hand."
    )
    assert model.name == "Cloudstone Curio"


def test_cardmodeldata_from_json_attraction(json_trash_bin):
    model = CardModelData.model_validate(json_trash_bin)
    assert model.attraction_lights == {2, 6}


def test_cardmodeldata_from_json_variation(json_anaconda_portal):
    model = CardModelData.model_validate(json_anaconda_portal)
    assert model.variation is True
    assert model.variation_of == "0a2012ad-6425-4935-83af-fc7309ec2ece"  # Anaconda


# endregion

# region from_card


def _test_from_card_helper(input_json):
    card = FullCard.from_json(input_json)
    model_from_card = CardModelData.model_validate(card.__dict__)
    model_from_json = CardModelData.model_validate(input_json)
    assert model_from_card == model_from_json


def test_cardmodeldata_from_card_instant(json_ancestral_recall):
    _test_from_card_helper(json_ancestral_recall)


def test_cardmodeldata_from_card_creature(json_omnath_locus_of_creation):
    _test_from_card_helper(json_omnath_locus_of_creation)


def test_cardmodeldata_from_card_token(json_snake_token):
    _test_from_card_helper(json_snake_token)


def test_cardmodeldata_from_card_transform_planeswalker(json_arlinn_the_packs_hope):
    _test_from_card_helper(json_arlinn_the_packs_hope)


def test_cardmodeldata_from_card_reversible(json_zndrsplt_eye_of_wisdom):
    card = FullCard.from_json(json_zndrsplt_eye_of_wisdom)
    model_from_card = CardModelData.model_validate(card.__dict__)
    model_from_json = CardModelData.model_validate(json_zndrsplt_eye_of_wisdom)

    # NOTE: CMC is not top-level for reversible cards in Scryfall so we add that here for ease of testing
    model_from_json.cmc = model_from_json.card_faces[0].cmc
    assert model_from_card == model_from_json


def test_cardmodeldata_from_card_watermark(json_anaconda_7ed_foil):
    _test_from_card_helper(json_anaconda_7ed_foil)


def test_cardmodeldata_from_card_non_english(json_python_spanish):
    _test_from_card_helper(json_python_spanish)


def test_cardmodeldata_from_card_flavor(json_elessar_the_elfstone):
    _test_from_card_helper(json_elessar_the_elfstone)


def test_cardmodeldata_from_card_attraction(json_trash_bin):
    _test_from_card_helper(json_trash_bin)


def test_cardmodeldata_from_card_variation(json_anaconda_portal):
    _test_from_card_helper(json_anaconda_portal)


# endregion

# endregion
