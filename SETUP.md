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
        - `test` - A set of cards that includes the Power 9 for testing purposes. (default)
        - `oracle` - A set of cards that includes one version of each card ever printed.
        - `scryfall` - A set of cards that includes every version of each card ever printed. (in English where available)
        - `all` - A set of every version of all cards and game objects in all available languages.
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
