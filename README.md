# scooze

[![CI](https://img.shields.io/github/actions/workflow/status/arcavios/scooze/pytest.yml?branch=dev&logo=github&label=CI)](https://github.com/arcavios/scooze/actions?query=event%3Apush+branch%3Adev+workflow%3Apytest)
[![pypi](https://img.shields.io/pypi/v/scooze.svg)](https://pypi.python.org/pypi/scooze)
[![versions](https://img.shields.io/pypi/pyversions/scooze.svg)](https://github.com/arcavios/scooze)
[![license](https://img.shields.io/badge/license-MIT-green)](./LICENSE)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)

A flexible data layer for applications working with Magic: the Gathering cards, decks, and tournaments.

## Features

📊 Robust data models for representing Magic: the Gathering cards, decks, and tournaments

- Cards - follows the Scryfall standard
- Decks - main deck/sideboard/command zone, format legality, average words, and more
- Tournaments - coming soon!

🎛️ CLI to manage a local database of [Scryfall](https://scryfall.com/docs/api/bulk-data) data

🐍 Python and REST APIs for interacting with the scooze database

## Help

See our [documentation](https://scooze.readthedocs.io/en/latest) for more information.

## Installation

Install using `pip install scooze`. For more installation options, see the [Install](https://scooze.readthedocs.io/en/latest/installation) section in the documentation.

## A Simple Example

``` python
from scooze.card import Card
from scooze.deck import Deck, InThe
from scooze.catalogs import Format

deck = Deck()
card1 = Card("Python")
card2 = Card("Anaconda")
swamp = Card("Swamp")

deck.add_card(card1, 25)
deck.add_card(swamp, 15)
deck.add_card(card2, 100, in_the=InThe.SIDE)

legal_limited = deck.is_legal(Format.LIMITED)   # True
legal_pauper = deck.is_legal(Format.PAUPER)     # False

export = deck.export()
"""
Deck:
25 Python
15 Swamp

Sideboard:
100 Anaconda
"""
```

## Contributing

For guidance on setting up a development environment and how to make a contribution to Pydantic, see [Contributing to scooze](https://scooze.readthedocs.io/en/latest/contributing).

## Report a Bug

If you find a bug 🐛 please open a [bug report](https://github.com/arcavios/scooze/issues/new?assignees=&labels=bug&template=bug_report.md&title=). If you have an idea for an improvement or new feature 🚀 please open a [feature request](https://github.com/arcavios/scooze/issues/new?assignees=&labels=enhancement&template=feature_request.md&title=).

If you find a security vulnerability, please follow the instructions [here](https://github.com/arcavios/scooze/security/policy).

---

![Scavenging Ooze](https://cards.scryfall.io/large/front/4/8/487116ab-b885-406b-aa54-56cb67eb3ca5.jpg?1594737205)
