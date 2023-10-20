# Change Log

## [dev]

### Added

- Added scooze_id to CardModel and Card. Changed the MongoDB _id to scooze_id. ([#193](https://github.com/arcavios/scooze/pull/193))
- Added AsyncScoozeApi as a way to use API endpoints in an async context (fixes Jupyter compatibility) ([#199](https://github.com/arcavios/scooze/pull/199))
- Add Docker support for starting MongoDB via the CLI ([#200](https://github.com/arcavios/scooze/pull/200))
- CLI rework to be more robust ([#203](https://github.com/arcavios/scooze/pull/203))

### Changed

- Added `None` as valid return type in normalizers ([#190](https://github.com/arcavios/scooze/pull/190))

### Fixed

- Fixed the use of mutable default arguments ([#188](https://github.com/arcavios/scooze/pull/188))
- Fixed improper runner call in API init ([#190](https://github.com/arcavios/scooze/pull/190))
- Fixed missing `await` call ([#190](https://github.com/arcavios/scooze/pull/190))

### Docs

- More completely document possible exceptions ([#209])(https://github.com/arcavios/scooze/pull/209)


## [1.0.4] - 2023-10-02

### Added

- Add DB/API methods for retrieving all cards at once ([#172](https://github.com/arcavios/scooze/pull/172))

### Changed

- Rename `col_type` to `coll_type` ([#176](https://github.com/arcavios/scooze/pull/176))
- Update fastapi requirement to allow versions before 1.0.0 ([#179](https://github.com/arcavios/scooze/pull/179))

### Fixed

- Fix "Event Loop Closed" error on multiple API calls ([#169](https://github.com/arcavios/scooze/pull/169))

### Docs

- Add dev section to changelog ([#178](https://github.com/arcavios/scooze/pull/178))


## [1.0.3] - 2023-09-29

### Added

- Create a model for representing Magic: the Gathering decks ([#20](https://github.com/arcavios/scooze/pull/20), [#31](https://github.com/arcavios/scooze/pull/31))
- Add support for downloading bulk data files from Scryfall ([#44](https://github.com/arcavios/scooze/pull/44), [#73](https://github.com/arcavios/scooze/pull/73))
- Create helpers for converting between Cards and CardModels (from the database) ([#80](https://github.com/arcavios/scooze/pull/80))
- Create enums for miscellaneous card parts (e.g. Color, Frame, etc.) ([#87](https://github.com/arcavios/scooze/pull/87))
- Create a CRUD API for decks and ([#98](https://github.com/arcavios/scooze/pull/98), [#108](https://github.com/arcavios/scooze/pull/108))
- Create a CLI for users to manage their local database from the command line ([#104](https://github.com/arcavios/scooze/pull/104), [#143](https://github.com/arcavios/scooze/pull/143))

### Changed

- Update docstrings according to Google's style guide ([#89](https://github.com/arcavios/scooze/pull/89))
- Update Card Hashing ([#96](https://github.com/arcavios/scooze/pull/96))

### Fixed

- Fixes the README.md
- Rename `Cardartist_id` to `Card.artist_ids` to match Scryfall ([#85](https://github.com/arcavios/scooze/pull/85), [#86](https://github.com/arcavios/scooze/pull/86))

### Docs

- N/A


## [0.1.0] - 2023-07-31

### Added

- Create a setup.py for local DB use ([#8](https://github.com/arcavios/scooze/pull/8))
- Create a CRUD API for card and cards ([#8](https://github.com/arcavios/scooze/pull/8))

### Changed

- N/A

### Fixed

- N/A

### Docs

- N/A
