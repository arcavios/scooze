A Scooze `CardModel` is a database representation of a Magic: the Gathering card closely following the
[Scryfall](https://scryfall.com/docs/api/cards) schema using [Pydantic](https://docs.pydantic.dev/latest/) models for
data validation.

::: scooze.models.card.CardModelData
    options:
        show_root_heading: true

::: scooze.models.card.CardModel
    options:
        show_root_heading: true

::: scooze.models.cardparts
    options:
        show_root_heading: true
        members:
            - ImageUrisModel
            - CardFaceModel
            - PricesModel
            - PreviewModel
            - PurchaseUrisModel
            - RelatedCardModel
            - RelatedUrisModel
