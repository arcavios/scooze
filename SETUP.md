## MongoDB

1. Installing Mongo (Ubuntu 22.04):
```
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse
sudo apt-get install mongodb-org
```
Run `$ mongod` to run mongo database

Optional steps:

2. Run the local database setup script:

- Creates a local database containing the Power 9 cards.
- Flags
    - `--include-cards` - Which cards do you want to insert into your local database?
        - `test` - The same as running without any flag. Include _only_ the Power 9 cards.
        - `oracle` - Include all OracleCards from [Ophidian's](https://github.com/arcavios/ophidian) `oracle_cards.json` bulk file.
        - `scryfall` - Include all default Cards from [Ophidian's](https://github.com/arcavios/ophidian) `default_cards.json` bulk file.
        - `all` - Include all.
    - `--include-decks`
        - `test` - Include some test Deck data.

3. Run the Mongo shell to manually interact with the database:

Run `$ mongosh` to open mongodb shell
Test database by creating a new collection and adding a new card:
```
db.createCollection("cards")
db.cards.insert({name: "Birds of Paradise", mv: "1"})
db.cards.find()
```

## Uvicorn

Run the FastAPI server from `slurrk` root with:

```uvicorn src.slurrk.main:app --reload```
