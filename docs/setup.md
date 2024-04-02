scooze can be used without a database to gain access to robust data models for representing cards, decks, and tournaments.

!!! Example "Using scooze for its data models"

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

To take advantage of all the features scooze has to offer, you'll need to decide how you want to setup your database.

## Database Setup

### Using Docker

Make sure [Docker Desktop](https://www.docker.com/products/docker-desktop/) is running.

???+ Note

    This will pull the latest MongoDB issued image for your hardware, and spin up a container with port 27017 bound to the host's port 27017.

``` shell
scooze setup docker
```

After this, you can continue to ["Using The CLI"](#using-the-cli) below.

### Running Local MongoDB

scooze depends on MongoDB to run your local database.
Download and install [MongoDB](https://www.mongodb.com/docs/manual/installation/).

???+ note

    Your local database can be stored wherever you want, but make sure you create the directory first. This is commonly stored at `./data/db`

Run the MongoDB server like this:

``` shell
mongod --dbpath path/to/db/
```

## Using the CLI

Run the scooze command line interface tool to add some data to your local database.

!!! Example "Using the scooze CLI"

    ``` shell
    scooze -h
    scooze load-cards oracle
    scooze run
    ```

## Using scooze in Your Code

Now that you've got some cards in your database, you can use it in your own code!

!!! Example "Using scooze in your code"

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
