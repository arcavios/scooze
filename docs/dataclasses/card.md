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
        # Explicitly order classmethods first
        members:
            - oracle_text_without_reminder
            - is_double_sided
            - total_words

::: scooze.card.FullCard
    options:
        show_root_heading: true

## `cardparts`
### ::: scooze.cardparts.ImageUris
    options:
        show_root_heading: true

### ::: scooze.cardparts.CardFace
    options:
        show_root_heading: true

### ::: scooze.cardparts.FullCardFace
    options:
        show_root_heading: true

### ::: scooze.cardparts.Prices
    options:
        show_root_heading: true

### ::: scooze.cardparts.Preview
    options:
        show_root_heading: true

### ::: scooze.cardparts.PurchaseUris
    options:
        show_root_heading: true

### ::: scooze.cardparts.RelatedCard
    options:
        show_root_heading: true

### ::: scooze.cardparts.RelatedUris
    options:
        show_root_heading: true
