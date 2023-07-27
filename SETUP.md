## Uvicorn

Run the server from `slurrk` root with:

```uvicorn src.slurrk.main:app --reload```

## Mongo

1. Installing Mongo (Ubuntu 22.04):
```
wget -qO - https://www.mongodb.org/static/pgp/server-6.0.asc | sudo apt-key add -
echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse" | sudo tee /etc/apt/sources.list.d/mongodb-org-6.0.list
deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu jammy/mongodb-org/6.0 multiverse
sudo apt-get install mongodb-org
```
Run `$ mongod` to run mongo database

Optional steps: 

Setup these aliases for running MongoDB on Linux:

```
alias mongostart="sudo systemctl start mongod"
alias mongostop="sudo systemctl stop mongod"
alias mongostatus="sudo systemctl status mongod"
alias mongorestart="sudo systemctl restart mongod"
```

2. Run the Mongo shell:

Run `$ mongosh` to open mongodb shell
Test database by creating a new collection and adding a new card:
```
db.createCollection("cards")
db.cards.insert({name: "Birds of Paradise", mv: "1"})
db.cards.find()
```

