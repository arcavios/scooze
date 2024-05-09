A scooze `Card` represents a Magic: The Gathering card closely following the
[Scryfall](https://scryfall.com/docs/api/cards) schema.

::: scooze.card
    options:
        inherited_members: false
        filters:
            - "!CardNormalizer"

::: scooze.cardparts
    options:
        filters:
            - "!CardPartsNormalizer"
