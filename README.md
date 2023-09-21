# scooze
A flexible data layer for applications working with Magic: the Gathering cards, decks, and tournaments.

## In this README 👇

- [Features](#features)
- [Usage](#usage)
  - [Initial setup](#initial-setup)
- [Contributing](#contributing)
  - [Developer setup](#developer-setup)

## Features

🎛️ CLI to manage a local database of Scryfall data

📊 Robust data models for representing Magic: the Gathering cards and decks
  - Cards - follows the Scryfall standard
  - Decks - main deck, sideboard, command zone. Format legality, average words, and more
  - Tournaments - coming soon!

🐍 Python and REST APIs for interacting with the scooze database
  - Note: v1 is local only

## Usage

### Initial setup

1. Download and install this package from [PyPi](https://pypi.org/project/scooze/).

    ```
    pip install scooze
    ```

2. Download and install [MongoDB](https://www.mongodb.com/docs/manual/installation/).

    Scooze depends on MongoDB to run your local database.

    *You can use scooze without MongoDB if you don't intend to use any of its database-related features.*

3. Run the MongoDB server.

    ```
    mongod --dbpath path/to/db/
    ```

    *Your local database can be stored wherever you want, but make sure you create the directory first. This is commonly stored at `/data/db`*

4. Run the scooze setup script to add some data to your local database.

    ```
    python -m scooze.cli --help
    python -m scooze.cli --include-cards oracle --include-decks pioneer
    ```

5. Use scooze in your application code!

    ```
    from scooze.api import scooze_api
    from scooze.catalogs import Format

    deck = scooze_api.get_deck() # gets a random deck from your local database
    print(deck.export())
    print(f"Legal in Explorer? {deck.is_legal(Format.EXPLORER)}")
    ```

## Contributing

If you find a bug 🐛, please open a [bug report](https://github.com/arcavios/scooze/issues/new?assignees=&labels=bug&template=bug_report.md&title=). If you have an idea for an improvement or new feature 🚀, please open a [feature request](https://github.com/arcavios/scooze/issues/new?assignees=&labels=enhancement&template=feature_request.md&title=). If it is a security vulnerability, **DO NOT** create an issue. Please reach out to one of the team members directly.

### Developer setup

1. Install Poetry
	- [Introduction to Poetry](https://python-poetry.org/docs/#installation)
	- Make sure it worked

        ```
        poetry --version
        ```

2. [Fork](https://github.com/arcavios/scooze/fork) and clone the scooze GitHub repo

    *Read more about forking [here](https://docs.github.com/en/get-started/quickstart/fork-a-repo).*

    ```
    git clone https://www.github.com/link/to/fork
    cd ./scooze
    poetry install
    ```

3. You're ready to develop!

4. When you have changes you'd like the team to review, please submit a pull request!

---

![Scavenging Ooze](https://cards.scryfall.io/large/front/4/8/487116ab-b885-406b-aa54-56cb67eb3ca5.jpg?1594737205)
