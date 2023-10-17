from unittest.mock import MagicMock, patch

import scooze.api.card as card_api
from scooze.api import ScoozeApi
from scooze.card import Card
from scooze.catalogs import Color
from scooze.models.card import CardModelOut


@patch("scooze.database.card.get_card_by_property")
def test_get_card_by(mock_get: MagicMock, recall_base):
    model = CardModelOut.model_validate(recall_base.__dict__)
    mock_get.return_value: CardModelOut = model

    with ScoozeApi(card_class=Card) as s:
        card = s.get_card_by(property_name="colors", value=[Color.BLUE])
        assert card == recall_base
        card = s.get_card_by(property_name="produced_mana", value=[])
        assert card == recall_base
        card = s.get_card_by(property_name="producedMana", value=[])
        assert card == recall_base
