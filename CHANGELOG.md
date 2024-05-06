# Change Log

### [DEVELOPMENT] - UNRELEASED

#### Added

- Add count_pips for Deck and CardList ([#251](https://github.com/arcavios/scooze/pull/251))
- Logging for the scooze CLI ([#277](https://github.com/arcavios/scooze/pull/277))
- Regression tests for validating Scryfall bulkdata ([#278](https://github.com/arcavios/scooze/pull/278))
- Add `scooze save cards` to the scooze CLI ([#287](https://github.com/arcavios/scooze/pull/287))
- Add `spree` to supported `FrameEffect`s ([#293](https://github.com/arcavios/scooze/pull/293))

#### Changed

- Use `pathlib` for consistent cross-OS file paths ([#222](https://github.com/arcavios/scooze/pull/222))
- Using Beanie for decks ([#272](https://github.com/arcavios/scooze/pull/272))
- Refactored the bulkdata API endpoints ([#279](https://github.com/arcavios/scooze/pull/279))
- Renamed DeckPart to CardList ([#281](https://github.com/arcavios/scooze/pull/281))
- Default to home/scooze for storage of bulk data and logs ([#294](https://github.com/arcavios/scooze/pull/294))
- Refactored Card dataclasses so there is only one representation of a card ([#310](https://github.com/arcavios/scooze/pull/310))
- Developers can import modules directly from the package and sub-package levels ([#316](https://github.com/arcavios/scooze/pull/316))

#### Fixed

- Skip validation for Sole Performer ([#297](https://github.com/arcavios/scooze/pull/297))
- Rename `enum.py` to `enums.py` to avoid Python default package conflicts ([#308](https://github.com/arcavios/scooze/pull/308))


### [1.0.7] - 2024-03-02

[GitHub Release](https://github.com/arcavios/scooze/releases/tag/v1.0.7)

#### Added

- Start Docker container if exists, but not running ([#243](https://github.com/arcavios/scooze/pull/243))
- Add basic logging to some of our modules ([#249](https://github.com/arcavios/scooze/pull/249))

#### Changed

- Change logging behavior to be extensible by applications using scooze ([#248](https://github.com/arcavios/scooze/pull/248))

#### Fixed

- Upgrade dependencies ([#245](https://github.com/arcavios/scooze/pull/245))
- Support latest version of Pydantic ([#247](https://github.com/arcavios/scooze/pull/247))

#### Docs

- Introduce API documentation on Read the Docs via MkDocs and mkdocstring ([#252](https://github.com/arcavios/scooze/pull/252))


### [1.0.6] - 2024-03-02

[GitHub Release](https://github.com/arcavios/scooze/releases/tag/v1.0.6)

#### Added

- Add support for symbols on cards (mana, energy, tap/untap, etc.) ([#214](https://github.com/arcavios/scooze/pull/214))
- Add support for attraction and sticker decks ([#231](https://github.com/arcavios/scooze/pull/231))
- Add support for Timeless and Standard Brawl formats ([#235](https://github.com/arcavios/scooze/pull/235))

#### Changed

- Using Beanie ODM to handle Mongo IO ([#220](https://github.com/arcavios/scooze/pull/220))


### [1.0.5] - 2023-11-09

[GitHub Release](https://github.com/arcavios/scooze/releases/tag/v1.0.5)

#### Added

- Added scooze_id to CardModel and Card. Changed the MongoDB _id to scooze_id. ([#193](https://github.com/arcavios/scooze/pull/193))
- Added AsyncScoozeApi as a way to use API endpoints in an async context (fixes Jupyter compatibility) ([#199](https://github.com/arcavios/scooze/pull/199))
- Add Docker support for starting MongoDB via the CLI ([#200](https://github.com/arcavios/scooze/pull/200))
- CLI rework to be more robust ([#203](https://github.com/arcavios/scooze/pull/203))
- Github Actions to test on push and deploy on tag ([#211](https://github.com/arcavios/scooze/pull/211))
- Add `cmc` field to top level for reversible cards ([#212](https://github.com/arcavios/scooze/pull/212))

#### Changed

- Changed the database lookup behavior to treat _id and scooze_id as the same. Also support snake case and camel case for property names. ([#205](https://github.com/arcavios/scooze/pull/205))
- Added `None` as valid return type in normalizers ([#190](https://github.com/arcavios/scooze/pull/190))
- Use `super().__init__()` for Card subclasses ([#217](https://github.com/arcavios/scooze/pull/217))

#### Fixed

- Fixed the use of mutable default arguments ([#188](https://github.com/arcavios/scooze/pull/188))
- Fixed improper runner call in API init ([#190](https://github.com/arcavios/scooze/pull/190))
- Fixed missing `await` call ([#190](https://github.com/arcavios/scooze/pull/190))

#### Docs

- More completely document possible exceptions [#209](https://github.com/arcavios/scooze/pull/209)


### [1.0.4] - 2023-10-02

[GitHub Release](https://github.com/arcavios/scooze/releases/tag/v1.0.4)

#### Added

- Add DB/API methods for retrieving all cards at once ([#172](https://github.com/arcavios/scooze/pull/172))

#### Changed

- Rename `col_type` to `coll_type` ([#176](https://github.com/arcavios/scooze/pull/176))
- Update fastapi requirement to allow versions before 1.0.0 ([#179](https://github.com/arcavios/scooze/pull/179))

#### Fixed

- Fix "Event Loop Closed" error on multiple API calls ([#169](https://github.com/arcavios/scooze/pull/169))

#### Docs

- Add dev section to changelog ([#178](https://github.com/arcavios/scooze/pull/178))


### [1.0.3] - 2023-09-29

[GitHub Release](https://github.com/arcavios/scooze/releases/tag/v1.0.3)

#### Added

- Create a model for representing Magic: the Gathering decks ([#20](https://github.com/arcavios/scooze/pull/20), [#31](https://github.com/arcavios/scooze/pull/31))
- Add support for downloading bulk data files from Scryfall ([#44](https://github.com/arcavios/scooze/pull/44), [#73](https://github.com/arcavios/scooze/pull/73))
- Create helpers for converting between Cards and CardModels (from the database) ([#80](https://github.com/arcavios/scooze/pull/80))
- Create enums for miscellaneous card parts (e.g. Color, Frame, etc.) ([#87](https://github.com/arcavios/scooze/pull/87))
- Create a CRUD API for decks and ([#98](https://github.com/arcavios/scooze/pull/98), [#108](https://github.com/arcavios/scooze/pull/108))
- Create a CLI for users to manage their local database from the command line ([#104](https://github.com/arcavios/scooze/pull/104), [#143](https://github.com/arcavios/scooze/pull/143))

#### Changed

- Update docstrings according to Google's style guide ([#89](https://github.com/arcavios/scooze/pull/89))
- Update Card Hashing ([#96](https://github.com/arcavios/scooze/pull/96))

#### Fixed

- Fixes the README.md
- Rename `Cardartist_id` to `Card.artist_ids` to match Scryfall ([#85](https://github.com/arcavios/scooze/pull/85), [#86](https://github.com/arcavios/scooze/pull/86))


### [0.1.0] - 2023-07-31

[GitHub Release](https://github.com/arcavios/scooze/releases/tag/v0.1.0)

#### Added

- Create a setup.py for local DB use ([#8](https://github.com/arcavios/scooze/pull/8))
- Create a CRUD API for card and cards ([#8](https://github.com/arcavios/scooze/pull/8))
