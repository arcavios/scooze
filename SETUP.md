## Uvicorn

Run the server from `slurrk` root with:

```uvicorn src.slurrk.main:app --reload```

## Mongo

Setup these aliases for running MongoDB on Linux:

```
alias mongostart="sudo systemctl start mongod"
alias mongostop="sudo systemctl stop mongod"
alias mongostatus="sudo systemctl status mongod"
alias mongorestart="sudo systemctl restart mongod"
```

Run the Mongo shell:

`$ mongosh`
