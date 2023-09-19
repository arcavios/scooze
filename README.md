# scooze
Tools for interacting with Magic: the Gathering tournaments, decklists, and cards.

## In this README 👇

- [Features](#features)
- [Usage](#usage)
  - [Initial setup](#initial-setup)
  - [Developer setup](#developer-setup)
- [Projects using this template](#projects-using-this-template)
- [FAQ](#faq)
- [Contributing](#contributing)

## Features
### TODO: write features list

This template repository comes with all of the boilerplate needed for:

⚙️ Robust (and free) CI with [GitHub Actions](https://github.com/features/actions):
  - Unit tests ran with [PyTest](https://docs.pytest.org) against multiple Python versions and operating systems.
  - Type checking with [mypy](https://github.com/python/mypy).
  - Linting with [ruff](https://astral.sh/ruff).
  - Formatting with [isort](https://pycqa.github.io/isort/) and [black](https://black.readthedocs.io/en/stable/).

🤖 [Dependabot](https://github.blog/2020-06-01-keep-all-your-packages-up-to-date-with-dependabot/) configuration to keep your dependencies up-to-date.

📄 Great looking API documentation built using [Sphinx](https://www.sphinx-doc.org/en/master/) (run `make docs` to preview).

🚀 Automatic GitHub and PyPI releases. Just follow the steps in [`RELEASE_PROCESS.md`](./RELEASE_PROCESS.md) to trigger a new release.

## Usage

### Initial setup

1. Download and install [Python 3.11](https://www.python.org/downloads/release/python-3115/) or newer.

2. Download and install this package from [PyPi](https://pypi.org/project/scooze/).

    ```
    pip install scooze
    ```

3. Download and install [MongoDB](https://www.mongodb.com/docs/manual/installation/).

    Scooze depends on MongoDB to run your local database.

    *You can use scooze without MongoDB if you don't intend to use any of its database-related features.*

4. Run the MongoDB server.

    ```
    mongod --dbpath path/to/db/
    ```

    *Your local database can be stored wherever you want, but make sure you create the directory first. This is commonly stored at `/data/db`*

5. Run the scooze setup script to add some data to your local database.

    ```
    python -m scooze.cli --help
    python -m scooze.cli --include-cards oracle --include-decks pioneer
    ```

6. Use scooze in your application code!

    ```
    from scooze.api import scooze_api
    from scooze.enums import Format # TODO: this reads poorly and I'd prefer scooze.catalogs or something

    deck = scooze_api.get_deck() # gets a random deck from your local database
    print(deck.export())
    print(f"Legal in Explorer? {deck.is_legal(Format.EXPLORER)}")
    ```

### Developer setup

1. TODO: put the stuff from our original setup.md file from junkwinder here.

2. Install poetry, then do

    ```
    git clone https://www.github.com/arcavios/scooze
    cd ./scooze
    poetry install
    ```

## Projects using this template

Here is an incomplete list of some projects that use scooze:

- [junkwinder](https://github.com/arcavios/junkwinder)
- [ophiomancer](https://github.com/arcavios/ophiomancer)
- [scraptrawler](https://github.com/arcavios/scraptrawler)

☝️ *Want your work featured here? Just open a pull request that adds the link.*

## FAQ

#### Do I need to have MongoDB to use scooze?

Nope! You can use most of scooze's functionality without using a database at all.

## Contributing

If you find a bug 🐛, please open a [bug report](https://github.com/allenai/python-package-template/issues/new?assignees=&labels=bug&template=bug_report.md&title=).
If you have an idea for an improvement or new feature 🚀, please open a [feature request](https://github.com/allenai/python-package-template/issues/new?assignees=&labels=Feature+request&template=feature_request.md&title=).

---

![Scavenging Ooze](https://cards.scryfall.io/large/front/4/8/487116ab-b885-406b-aa54-56cb67eb3ca5.jpg?1594737205)
