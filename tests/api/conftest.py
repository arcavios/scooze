import pytest
from scooze.card import Card

# region Card fixtures


@pytest.fixture(scope="module")
def recall_base(json_ancestral_recall) -> Card:
    card = Card.from_json(json_ancestral_recall)
    return card


@pytest.fixture(scope="module")
def recall_oracle(json_ancestral_recall) -> Card:
    card = Card.from_json(json_ancestral_recall)
    return card


@pytest.fixture(scope="module")
def recall_full(json_ancestral_recall) -> Card:
    card = Card.from_json(json_ancestral_recall)
    return card


@pytest.fixture(scope="module")
def mystic_snake_base(json_mystic_snake) -> Card:
    card = Card.from_json(json_mystic_snake)
    return card


@pytest.fixture(scope="module")
def mystic_snake_oracle(json_mystic_snake) -> Card:
    card = Card.from_json(json_mystic_snake)
    return card


@pytest.fixture(scope="module")
def mystic_snake_full(json_mystic_snake) -> Card:
    card = Card.from_json(json_mystic_snake)
    return card


@pytest.fixture(scope="module")
def cards_base(recall_base, mystic_snake_base) -> list[Card]:
    return [recall_base, mystic_snake_base]


@pytest.fixture(scope="module")
def cards_oracle(recall_oracle, mystic_snake_oracle) -> list[Card]:
    return [recall_oracle, mystic_snake_oracle]


@pytest.fixture(scope="module")
def cards_full(recall_full, mystic_snake_full) -> list[Card]:
    return [recall_full, mystic_snake_full]


# endregion
