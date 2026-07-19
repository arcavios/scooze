from datetime import date
import pytest
from scooze.catalogs import BorderColor, Color, Finish, Frame, Game, ImageStatus, Language, Layout, Rarity, SecurityStamp, SetType
from scooze.models import CardModel

# region Card fixtures


@pytest.fixture()
def model_ancestral_recall(json_ancestral_recall, legalities_ancestral_recall) -> CardModel:
    model = CardModel()

    model.all_parts = None
    model.arena_id = None
    model.artist = "Ryan Pancoast"
    model.artist_ids = ["89cc9475-dda2-4d13-bf88-54b92867a25c"]
    model.attraction_lights = None
    model.booster = True
    model.border_color = BorderColor.BLACK
    model.card_back_id = "0aeebaf5-8c7d-4636-9e82-8c27447861f7"
    model.card_faces = None
    model.cardmarket_id = None
    model.cmc = 1.0
    model.collector_number = "1"
    model.color_identity = {Color.BLUE}
    model.color_indicator = None
    model.colors = {Color.BLUE}
    model.content_warning = False
    model.digital = True
    model.edhrec_rank = None
    model.finishes = {Finish.NONFOIL, Finish.FOIL}
    model.flavor_name = None
    model.flavor_text = None
    model.frame = Frame._2015
    model.frame_effects = None
    model.full_art = False
    model.games = {Game.MTGO}
    model.hand_modifier = None
    model.highres_image = True
    model.illustration_id = "95c5ab6f-fcce-4e21-9e02-cc1d922adfae"
    model.image_status = ImageStatus.HIGHRES_SCAN

    # ImageUris
    # TODO: create nested models
    model.image_uris.art_crop = "https://cards.scryfall.io/art_crop/front/2/3/2398892d-28e9-4009-81ec-0d544af79d2b.jpg?1614638829"
    model.image_uris.border_crop = "https://cards.scryfall.io/border_crop/front/2/3/2398892d-28e9-4009-81ec-0d544af79d2b.jpg?1614638829"
    model.image_uris.large = "https://cards.scryfall.io/large/front/2/3/2398892d-28e9-4009-81ec-0d544af79d2b.jpg?1614638829"
    model.image_uris.normal = "https://cards.scryfall.io/normal/front/2/3/2398892d-28e9-4009-81ec-0d544af79d2b.jpg?1614638829"
    model.image_uris.png = "https://cards.scryfall.io/png/front/2/3/2398892d-28e9-4009-81ec-0d544af79d2b.png?1614638829"
    model.image_uris.small = "https://cards.scryfall.io/small/front/2/3/2398892d-28e9-4009-81ec-0d544af79d2b.jpg?1614638829"

    model.keywords = set()
    model.lang = Language.ENGLISH
    model.layout = Layout.NORMAL
    model.legalities = legalities_ancestral_recall
    model.life_modifier = None
    model.loyalty = None
    model.mana_cost = "{U}"
    model.mtgo_foil_id = 53178
    model.mtgo_id = 53177
    model.multiverse_ids = [382841]
    model.name = "Ancestral Recall"
    model.oracle_id = "550c74d4-1fcb-406a-b02a-639a760a4380"
    model.oracle_text = "Target player draws three cards."
    model.oversized = False
    model.penny_rank = None
    model.power = None
    model.preview = None

    # Prices
    model.prices.eur = None
    model.prices.eur_foil = None
    model.prices.tix = 1.9
    model.prices.usd = None
    model.prices.usd_etched = None
    model.prices.usd_foil = None

    model.printed_name = None
    model.printed_text = None
    model.printed_type_line = None
    model.prints_search_uri = "https://api.scryfall.com/cards/search?order=released&q=oracleid%3A550c74d4-1fcb-406a-b02a-639a760a4380&unique=prints"
    model.produced_mana = None
    model.promo = False
    model.promo_types = None

    # PurchaseUris
    model.purchase_uris.cardhoarder = "https://www.cardhoarder.com/cards/53177?affiliate_id=scryfall&ref=card-profile&utm_campaign=affiliate&utm_medium=card&utm_source=scryfall"
    model.purchase_uris.cardmarket = "https://www.cardmarket.com/en/Magic/Products/Search?referrer=scryfall&searchString=Ancestral+Recall&utm_campaign=card_prices&utm_medium=text&utm_source=scryfall"
    model.purchase_uris.tcgplayer = "https://www.tcgplayer.com/search/magic/product?productLineName=magic&q=Ancestral+Recall&utm_campaign=affiliate&utm_medium=api&utm_source=scryfall&view=grid"

    model.rarity = Rarity.BONUS

    # RelatedUris
    model.related_uris.edhrec = "https://edhrec.com/route/?cc=Ancestral+Recall"
    model.related_uris.gatherer = "https://gatherer.wizards.com/Pages/Card/Details.aspx?multiverseid=382841"
    model.related_uris.tcgplayer_infinite_articles = "https://infinite.tcgplayer.com/search?contentMode=article&game=magic&partner=scryfall&q=Ancestral+Recall&utm_campaign=affiliate&utm_medium=api&utm_source=scryfall"
    model.related_uris.tcgplayer_infinite_decks = "https://infinite.tcgplayer.com/search?contentMode=deck&game=magic&partner=scryfall&q=Ancestral+Recall&utm_campaign=affiliate&utm_medium=api&utm_source=scryfall"

    model.released_at = date(year=2014, month=6, day=16)
    model.reprint = True
    model.reserved = True
    model.rulings_uri = "https://api.scryfall.com/cards/2398892d-28e9-4009-81ec-0d544af79d2b/rulings"
    model.scryfall_id = "2398892d-28e9-4009-81ec-0d544af79d2b"
    model.scryfall_set_uri = "https://scryfall.com/sets/vma?utm_source=api"
    model.scryfall_uri = "https://scryfall.com/card/vma/1/ancestral-recall?utm_source=api"
    model.security_stamp = SecurityStamp.OVAL
    model.set_code = "vma"
    model.set_id = "a944551a-73fa-41cd-9159-e8d0e4674403"
    model.set_name = "Vintage Masters"
    model.set_search_uri = "https://api.scryfall.com/cards/search?order=set&q=e%3Avma&unique=prints"
    model.set_type = SetType.MASTERS
    model.set_uri = "https://api.scryfall.com/sets/a944551a-73fa-41cd-9159-e8d0e4674403"
    model.story_spotlight = False
    model.tcgplayer_etched_id = None
    model.tcgplayer_id = None
    model.textless = False
    model.toughness = None
    model.type_line = "Instant"
    model.uri = "https://api.scryfall.com/cards/2398892d-28e9-4009-81ec-0d544af79d2b"
    model.variation = False
    model.variation_of = None
    model.watermark = None

    return CardModel(model)


# endregion
