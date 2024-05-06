# scooze

[![CI](https://img.shields.io/github/actions/workflow/status/arcavios/scooze/ci.yml?branch=dev&logo=github&label=CI)](https://github.com/arcavios/scooze/actions?query=event%3Apush+branch%3Adev+workflow%3A%22Continuous+Integration%22)
[![pypi](https://img.shields.io/pypi/v/scooze.svg)](https://pypi.python.org/pypi/scooze)
[![versions](https://img.shields.io/pypi/pyversions/scooze.svg)](https://github.com/arcavios/scooze)
[![license](https://img.shields.io/badge/license-MIT-green)](https://github.com/arcavios/scooze/blob/dev/LICENSE)
[![Pydantic v2](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/pydantic/pydantic/main/docs/badge/v2.json)](https://pydantic.dev)

A flexible data layer for applications working with Magic: the Gathering cards and decks.

## Features

📊 Robust data models for representing Magic: the Gathering cards and decks

- Cards - follows the Scryfall standard
- Decks - main deck/sideboard/command zone, format legality, average words, and more

🎛️ CLI to manage a local database of [Scryfall](https://scryfall.com/docs/api/bulk-data) data

🐍 Python and REST APIs for interacting with the scooze database

## Help

The source code can be found [here](https://github.com/arcavios/scooze).

See our [documentation](https://scooze.readthedocs.io/en/stable/) for more information.

## Installation

Install using `pip install scooze`. For more installation options, see the [Install](https://scooze.readthedocs.io/en/stable/installation) section in the documentation.

## A Simple Example

``` python
from scooze import Card, Deck, Format, InThe

deck = Deck()
card1 = Card("Python")
card2 = Card("Anaconda")
swamp = Card("Swamp")

deck.add_card(card1, 25)
deck.add_card(swamp, 15)
deck.add_card(card2, 100, InThe.SIDE)

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

See [Setup](https://scooze.readthedocs.io/en/stable/setup/) and our [API Documentation](https://scooze.readthedocs.io/en/stable/dataclasses/card/) for more details.

## Contributing

For guidance on setting up a development environment and how to make a contribution to scooze, see [Contributing to scooze](https://scooze.readthedocs.io/en/stable/contributing).

## Report a Bug

If you find a bug 🐛 please open a [bug report](https://github.com/arcavios/scooze/issues/new?assignees=&labels=bug&template=bug_report.md&title=). If you have an idea for an improvement or new feature 🚀 please open a [feature request](https://github.com/arcavios/scooze/issues/new?assignees=&labels=enhancement&template=feature_request.md&title=).

If you find a security vulnerability, please follow the instructions [here](https://github.com/arcavios/scooze/security/policy).

---

![Scavenging Ooze](https://cards.scryfall.io/large/front/4/8/487116ab-b885-406b-aa54-56cb67eb3ca5.jpg?1594737205)
