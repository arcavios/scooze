import asyncio

import pytest
from bson import ObjectId
from scooze.card import Card, FullCard, OracleCard


@pytest.fixture(scope="session")
def asyncio_runner():
    with asyncio.Runner() as runner:
        yield runner


# region Card fixtures


@pytest.fixture(scope="module")
def recall_base(json_ancestral_recall) -> Card:
    card = Card.from_json(json_ancestral_recall)
    card.scooze_id = ObjectId()
    return card


@pytest.fixture(scope="module")
def recall_oracle(json_ancestral_recall) -> OracleCard:
    card = OracleCard.from_json(json_ancestral_recall)
    card.scooze_id = ObjectId()
    return card


@pytest.fixture(scope="module")
def recall_full(json_ancestral_recall) -> FullCard:
    card = FullCard.from_json(json_ancestral_recall)
    card.scooze_id = ObjectId()
    return card


@pytest.fixture(scope="module")
def mystic_snake_base(json_mystic_snake) -> Card:
    card = Card.from_json(json_mystic_snake)
    card.scooze_id = ObjectId()
    return card


@pytest.fixture(scope="module")
def mystic_snake_oracle(json_mystic_snake) -> OracleCard:
    card = OracleCard.from_json(json_mystic_snake)
    card.scooze_id = ObjectId()
    return card


@pytest.fixture(scope="module")
def mystic_snake_full(json_mystic_snake) -> FullCard:
    card = FullCard.from_json(json_mystic_snake)
    card.scooze_id = ObjectId()
    return card


@pytest.fixture(scope="module")
def cards_base(recall_base, mystic_snake_base) -> list[Card]:
    return [recall_base, mystic_snake_base]


@pytest.fixture(scope="module")
def cards_oracle(recall_oracle, mystic_snake_oracle) -> list[OracleCard]:
    return [recall_oracle, mystic_snake_oracle]


@pytest.fixture(scope="module")
def cards_full(recall_full, mystic_snake_full) -> list[FullCard]:
    return [recall_full, mystic_snake_full]


# endregion
