A Scooze `Card` represents a Magic: the Gathering card closely following the
[Scryfall](https://scryfall.com/docs/api/cards) schema.

::: scooze.card
    options:
        members:
            - Card
            - OracleCard
            - FullCard

::: scooze.cardparts
    options:
        members:
            - ImageUris
            - CardFace
            - FullCardFace
            - Prices
            - Preview
            - PurchaseUris
            - RelatedCard
            - RelatedUris
