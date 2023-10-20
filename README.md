# scooze
A flexible data layer for applications working with Magic: the Gathering cards, decks, and tournaments.

## In this README 👇

- [Features](#features)
- [Usage](#usage)
  - [Initial setup](#initial-setup)
- [Contributing](#contributing)
  - [Developer setup](#developer-setup)

## Features

🎛️ CLI to manage a local database of [Scryfall](https://scryfall.com/docs/api/bulk-data) data

📊 Robust data models for representing Magic: the Gathering cards, decks, and tournaments
  - Cards - follows the Scryfall standard
  - Decks - main deck/sideboard/command zone, format legality, average words, and more
  - Tournaments - coming soon!

🐍 Python and REST APIs for interacting with the scooze database
  - Note: v1 is local only

## Usage

### Initial setup

1. Download and install this package from [PyPi](https://pypi.org/project/scooze/).

    ```
    pip install scooze
    ```

2. Set up the database
    - Using Docker:

        *Make sure [Docker Desktop](https://www.docker.com/products/docker-desktop/) is running.*

         ```
         scooze setup docker
         ```
         * This will pull the latest MongoDB issued image for your machine's distribution, and spin up the container with port 27017 bound to the host's port 27017.
         * After this, you can continue to (3) below.

    - Running MongoDB locally:

         Scooze depends on MongoDB to run your local database.
         Download and install [MongoDB](https://www.mongodb.com/docs/manual/installation/).

         *You can use scooze without MongoDB if you don't intend to use any of its database-related features.*

         *Your local database can be stored wherever you want, but make sure you create the directory first. This is commonly stored at `/data/db`*

         Run the MongoDB server with

         ```
         mongod --dbpath path/to/db/
         ```

3. Run the scooze CLI tool (installed with pip install) to add some data to your local database.

    ```
    scooze -h
    scooze load-cards oracle
    scooze run
    ```

4. Use scooze in your application code!

    ```
    from scooze.api import ScoozeApi
    from scooze.catalogs import Color

    with ScoozeApi() as s:
      # get 10 arbitrary green cards
      green_cards = s.get_cards_by("colors", [Color.GREEN], paginated=True, page_size=10)
      # get _all_ green cards
      green_cards = s.get_cards_by("colors", [Color.GREEN])

      # get all cards from a particular set
      woe_cards = s.get_cards_by_set("woe")

      # get a specific card
      black_lotus = s.get_card_by_name("Black Lotus")
      print(black_lotus.total_words())

      # and more!
    ```

## Contributing

If you find a bug 🐛, please open a [bug report](https://github.com/arcavios/scooze/issues/new?assignees=&labels=bug&template=bug_report.md&title=). If you have an idea for an improvement or new feature 🚀, please open a [feature request](https://github.com/arcavios/scooze/issues/new?assignees=&labels=enhancement&template=feature_request.md&title=).

If you find a security vulnerability, please follow the instructions [here](./SECURITY.md).

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
