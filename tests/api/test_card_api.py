import asyncio

import pytest
import scooze.api.card as card_api
from scooze.card import Card, FullCard, OracleCard


# region Card fixtures
@pytest.fixture(scope="module")
def recall_base(json_ancestral_recall):
    return Card.from_json(json_ancestral_recall)


@pytest.fixture(scope="module")
def recall_oracle(json_ancestral_recall):
    return OracleCard.from_json(json_ancestral_recall)


@pytest.fixture(scope="module")
def recall_full(json_ancestral_recall):
    return FullCard.from_json(json_ancestral_recall)


@pytest.fixture(scope="module")
def cards_base(recall_base):
    return [recall_base, recall_base]


@pytest.fixture(scope="module")
def cards_oracle(recall_oracle):
    return [recall_oracle, recall_oracle]


@pytest.fixture(scope="module")
def cards_full(recall_full):
    return [recall_full, recall_full]


# @pytest.fixture(scope="module")
# def mystic_snake_base(json_mystic_snake):
#     return Card.from_json(json_mystic_snake)


# @pytest.fixture(scope="module")
# def mystic_snake_oracle(json_mystic_snake):
#     return OracleCard.from_json(json_mystic_snake)


# @pytest.fixture(scope="module")
# def mystic_snake_full(json_mystic_snake):
#     return FullCard.from_json(json_mystic_snake)


# endregion

# TODO: clean these up with mocks
# run tests with pytest -s to see the print statements
# NOTE: these tests will actually add cards to your local database (it has to be running for these to pass)
# you can see them with
# use scooze
# db.cards.find()
# db.cards.deleteMany({})


def test_add_base_card(recall_base):
    from scooze.database.mongo import mongo_close, mongo_connect

    asyncio.run(mongo_connect())
    result = card_api.add_card_to_db(recall_base)
    from pprint import pprint

    pprint(result)
    assert result
    asyncio.run(mongo_close())


def test_add_oracle_card(recall_oracle):
    from scooze.database.mongo import mongo_close, mongo_connect

    asyncio.run(mongo_connect())
    result = card_api.add_card_to_db(recall_oracle)
    from pprint import pprint

    pprint(result)
    assert result
    asyncio.run(mongo_close())


def test_add_full_card(recall_full):
    from scooze.database.mongo import mongo_close, mongo_connect

    asyncio.run(mongo_connect())
    result = card_api.add_card_to_db(recall_full)
    from pprint import pprint

    pprint(result)
    assert result
    asyncio.run(mongo_close())


def test_add_base_cards(cards_base):
    from scooze.database.mongo import mongo_close, mongo_connect

    asyncio.run(mongo_connect())
    result = card_api.add_cards_to_db(cards_base)
    from pprint import pprint

    pprint(result)
    assert result
    asyncio.run(mongo_close())


def test_add_oracle_cards(cards_oracle):
    from scooze.database.mongo import mongo_close, mongo_connect

    asyncio.run(mongo_connect())
    result = card_api.add_cards_to_db(cards_oracle)
    from pprint import pprint

    pprint(result)
    assert result
    asyncio.run(mongo_close())


def test_add_full_cards(cards_full):
    from scooze.database.mongo import mongo_close, mongo_connect

    asyncio.run(mongo_connect())
    result = card_api.add_cards_to_db(cards_full)
    from pprint import pprint

    pprint(result)
    assert result
    asyncio.run(mongo_close())


def test_add_mixed_cards(cards_base, cards_oracle, cards_full):
    cards_base.extend(cards_oracle + cards_full)
    from scooze.database.mongo import mongo_close, mongo_connect

    asyncio.run(mongo_connect())
    result = card_api.add_cards_to_db(cards_base)
    from pprint import pprint

    pprint(result)
    assert result
    asyncio.run(mongo_close())
