A scooze `CardModel` is a database representation of a Magic: The Gathering card closely following the
[Scryfall](https://scryfall.com/docs/api/cards) schema using [Pydantic](https://docs.pydantic.dev/latest/) models for
data validation.

::: scooze.models.card
    options:
        members:
            - CardModelData
            - CardModel

::: scooze.models.cardparts
    options:
        members:
            - ImageUrisModel
            - CardFaceModel
            - PricesModel
            - PreviewModel
            - PurchaseUrisModel
            - RelatedCardModel
            - RelatedUrisModel
