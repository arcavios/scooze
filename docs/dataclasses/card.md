A Scooze `Card` represents a Magic: the Gathering card closely following the
[Scryfall](https://scryfall.com/docs/api/cards) schema.

::: scooze.card.Card
    options:
        show_root_heading: true
        members:
            - from_json
            - from_model

::: scooze.card.OracleCard
    options:
        show_root_heading: true
        # explicit members list so we can set order and include `__init__` easily
        members:
            - oracle_text_without_reminder
            - is_double_sided
            - total_words

::: scooze.card.FullCard
    options:
        show_root_heading: true

::: scooze.cardparts
    options:
        show_root_heading: true
        members:
            - ImageUris
            - CardFace
            - FullCardFace
            - Prices
            - Preview
            - PurchaseUris
            - RelatedCard
            - RelatedUris
