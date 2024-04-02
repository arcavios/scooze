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

        ``` shell
        scooze setup docker
        ```

        * This will pull the latest MongoDB issued image for your machine's distribution, and spin up the container with port 27017 bound to the host's port 27017.
        * After this, you can continue to (3) below.

    - Running MongoDB locally:

        scooze depends on MongoDB to run your local database.
        Download and install [MongoDB](https://www.mongodb.com/docs/manual/installation/).

        *You can use scooze without MongoDB if you don't intend to use any of its database-related features.*

        *Your local database can be stored wherever you want, but make sure you create the directory first. This is commonly stored at `/data/db`*

        Run the MongoDB server with

        ``` shell
        mongod --dbpath path/to/db/
        ```

3. Run the scooze CLI tool (installed with pip install) to add some data to your local database.

  ``` shell
  scooze -h
  scooze load-cards oracle
  scooze run
  ```

4. Use scooze in your application code!

  ``` python
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
