from scooze.card import Card, OracleCard, FullCard
import scooze.api.card as card_api
import pytest


@pytest.fixture(scope="session")
def recall_base(json_ancestral_recall):
    return Card.from_json(json_ancestral_recall)


@pytest.fixture(scope="session")
def recall_oracle(json_ancestral_recall):
    return OracleCard.from_json(json_ancestral_recall)


@pytest.fixture(scope="session")
def recall_full(json_ancestral_recall):
    return FullCard.from_json(json_ancestral_recall)


@pytest.fixture(scope="session")
def mystic_snake_base(json_mystic_snake):
    return Card.from_json(json_mystic_snake)


@pytest.fixture(scope="session")
def mystic_snake_oracle(json_mystic_snake):
    return OracleCard.from_json(json_mystic_snake)


@pytest.fixture(scope="session")
def mystic_snake_full(json_mystic_snake):
    return FullCard.from_json(json_mystic_snake)


def test_add_base_card(recall_base):
    assert card_api.add_card_to_db(recall_base)


def test_add_oracle_card(recall_oracle):
    assert card_api.add_card_to_db(recall_oracle)


def test_add_full_card(recall_full):
    assert card_api.add_card_to_db(recall_full)


def test_add_base_cards(recall_base, mystic_snake_base):
    pass


def test_add_oracle_cards(recall_oracle, mystic_snake_oracle):
    pass


def test_add_full_cards(recall_full, mystic_snake_full):
    pass


def test_add_mixed_cards(recall_oracle, mystic_snake_full):
    pass
