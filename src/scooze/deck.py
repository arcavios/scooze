import json
from collections import Counter
from datetime import date
from sys import maxsize
from typing import Generic, Iterable, Mapping, Self

import scooze.utils as utils
from bson import ObjectId
from scooze.api import ScoozeApi
from scooze.card import CardT, OracleCard
from scooze.catalogs import DecklistFormatter, Format, InThe, Legality
from scooze.deckpart import DeckDiff, DeckPart
from scooze.models.deck import DeckModel


class Deck(utils.ComparableObject, Generic[CardT]):
    """
    A class to represent a deck of Magic: the Gathering cards.

    Attributes:
        archetype: The archetype of this Deck.
        format: The format legality of the cards in this Deck.
        main: The main deck. Typically 60 cards minimum.
        side: The sideboard. Typically 15 cards maximum.
        cmdr: The command zone. Typically 1 or 2 cards in Commander formats.
    """

    def __init__(
        self,
        archetype: str | None = None,
        date_played: date | None = None,
        format: Format = Format.NONE,
        main: DeckPart[CardT] = DeckPart(),
        side: DeckPart[CardT] = DeckPart(),
        cmdr: DeckPart[CardT] = DeckPart(),
    ):
        self.archetype = archetype
        self.date_played = DeckNormalizer.to_date(date_played)
        self.format = format

        self.main = DeckNormalizer.to_deck_part(main)
        self.side = DeckNormalizer.to_deck_part(side)
        self.cmdr = DeckNormalizer.to_deck_part(cmdr)

    @property
    def cards(self) -> Counter[CardT]:
        return self.main.cards + self.side.cards + self.cmdr.cards

    def __str__(self):
        decklist = self.export()
        return f"""Archetype: {self.archetype}\n""" f"""Format: {self.format}\n""" f"""Decklist:\n{decklist}\n"""

    @classmethod
    def from_json(cls, data: dict | str) -> Self:
        if isinstance(data, dict):
            return cls(**data)
        elif isinstance(data, str):
            return cls(**json.loads(data))

    @classmethod
    def from_model(cls, model: DeckModel) -> Self:
        return cls(**model.model_dump())

    def average_cmc(self) -> float:
        """
        The average mana value of cards in this Deck.
        """

        # TODO(#112): Add type filters.
        # TODO(#113): Reversible cards do not have a top-level cmc. Assign one?

        total_cards = self.total_cards()

        if total_cards > 0:
            return self.total_cmc() / self.total_cards()
        return 0

    def average_words(self) -> float:
        """
        The average number of words across all oracle text on all cards in this
        Deck (excludes reminder text).
        """

        # TODO(#112): Add type filters.

        total_cards = self.total_cards()

        if total_cards > 0:
            return self.total_words() / self.total_cards()
        return 0

    def diff(self, other: Self) -> DeckDiff:
        """
        Generate a diff between this Deck and another.

        Args:
            other: The other Deck.

        Returns:
            A DeckDiff with keys for each deck part. Each contains a dict of
            each card in both decks and their counts.
        """

        return DeckDiff(
            main=self.main.diff(other.main),
            side=self.side.diff(other.side),
            cmdr=self.cmdr.diff(other.cmdr),
        )

    def decklist_equals(self, other: Self) -> bool:
        """
        Determine if this Deck contains exactly the same cards as another.

        Args:
            other: The other Deck.

        Returns:
            True if this Deck contains exactly the same cards as another, else
            False.
        """

        if self.total_cards() != other.total_cards():
            return False

        diff = self.diff(other)
        same_main = not bool(diff.main)
        same_side = not bool(diff.side)
        same_cmdr = not bool(diff.cmdr)

        return same_main and same_side and same_cmdr

    def export(self, export_format: DecklistFormatter = None) -> str:
        """
        Export this Deck as a string with the given DecklistFormatter.

        Args:
            export_format: The format of the exported Deck.

        Returns:
            A string containing the names and quantities of the cards in this
            Deck.
        """

        match export_format:
            case DecklistFormatter.ARENA:
                sb_prefix = "Sideboard\n"
                cmdr_prefix = "Commander\n"
                # TODO(#50): filter out cards that are not on Arena. Log a WARNING with those cards.
            case DecklistFormatter.MTGO:
                sb_prefix = "SIDEBOARD:\n"
                cmdr_prefix = ""
                # TODO(#50): filter out cards that are not on MTGO. Log a WARNING with those cards.
            case _:
                sb_prefix = "Sideboard\n"  # Default
                cmdr_prefix = "Commander\n"  # Default
        sb_prefix = "\n" + sb_prefix
        cmdr_suffix = "\n"

        # Build the decklist string
        main = str(self.main) if len(self.main) > 0 else ""
        side = (sb_prefix + str(self.side)) if len(self.side) > 0 else ""
        cmdr = (cmdr_prefix + str(self.cmdr) + cmdr_suffix) if len(self.cmdr) > 0 else ""
        decklist = f"{cmdr}{main}{side}"

        return decklist

    def is_legal(self, format: Format = None) -> bool:
        """
        Determine if this Deck is legal in the given format.

        Default checks against `self.Format`. If `self.Format` is unset, checks against `Format.NONE`.

        - For cards with `Legality.RESTRICTED`, only 1 or fewer may be present
        throughout all deck parts.
        - For cards with `Legality.LEGAL`, only N or fewer may be present
        throughout all deck parts where N is determined by the max quantity of
        a single cards allowed by the given format.
        - For cards with `Legality.BANNED` or `Legality.NOT_LEGAL`, none may be
        present throught all deck parts.

        Args:
            format: The format to check against.
        """

        # Default
        if format is None:
            format = self.format if self.format is not None else Format.NONE

        # Check deck meets minimum size requirements
        if self.main.total() < utils.main_size(format)[0]:
            return False
        if self.side.total() < utils.side_size(format)[0]:
            return False
        if self.cmdr.total() < utils.cmdr_size(format)[0]:
            return False

        # Check card quantities do not exceed acceptable maximums
        for c, q in self.cards.items():
            c_legal = c.legalities[format] if format not in [Format.LIMITED, Format.NONE] else Legality.LEGAL

            if (c_legal is Legality.RESTRICTED and q > 1) or c_legal in [Legality.BANNED, Legality.NOT_LEGAL]:
                return False

            if q > utils.max_card_quantity(format) and q > utils.max_relentless_quantity(c.name):
                return False

        return True

    def total_cards(self) -> int:
        """
        The number of cards in this Deck.
        """

        return self.main.total() + self.side.total() + self.cmdr.total()

    def total_cmc(self) -> float:
        """
        The total mana value of cards in this Deck.
        """

        # TODO(#113): Reversible cards do not have a top-level cmc. Assign one?

        return sum([c.cmc * q for c, q in self.cards.items()])

    def total_words(self) -> int:
        """
        The number of words across all oracle text on all cards in this Deck
        (excludes reminder text).
        """

        return sum([c.total_words() * q for c, q in self.cards.items()])

    # region Mutating Methods

    def add_card(self, card: CardT, quantity: int = 1, in_the: InThe = InThe.MAIN) -> None:
        """
        Add a given quantity of a given card to this Deck.

        Args:
            card: The card to add.
            quantity: The number of copies of the card to be added.
            in_the: Where to add the card (main, side, etc)
        """

        match in_the:
            case InThe.MAIN:
                self.main.add_card(card=card, quantity=quantity)
            case InThe.SIDE:
                self.side.add_card(card=card, quantity=quantity)
            case InThe.CMDR:
                self.cmdr.add_card(card=card, quantity=quantity)
            case _:
                pass  # TODO(#75): 'in' must be one of InThe.list()

    def add_cards(self, cards: Counter[CardT], in_the: InThe = InThe.MAIN) -> None:
        """
        Add the given cards to this Deck.

        Args:
            cards: The cards to add.
            in_the: Where to add the cards (main, side, etc)
        """

        match in_the:
            case InThe.MAIN:
                self.main.add_cards(cards)
            case InThe.SIDE:
                self.side.add_cards(cards)
            case InThe.CMDR:
                self.cmdr.add_cards(cards)

    def remove_card(self, card: CardT, quantity: int = maxsize, in_the: InThe = InThe.MAIN) -> None:
        """
        Remove a given quantity of a given card from this Deck. If quantity is
        not provided, removes all copies.

        Args:
            card: The card to remove.
            quantity: The number of copies of the card to be removed.
            in_the: Where to remove the cards from (main, side, etc)
        """

        # using counterA - counterB results in a new Counter with only positive results
        match in_the:
            case InThe.MAIN:
                self.main.remove_card(card=card, quantity=quantity)
            case InThe.SIDE:
                self.side.remove_card(card=card, quantity=quantity)
            case InThe.CMDR:
                self.cmdr.remove_card(card=card, quantity=quantity)
            case _:
                pass  # TODO(#75): failed to remove card

    def remove_cards(self, cards: Counter[CardT], in_the: InThe = InThe.MAIN) -> None:
        """
        Remove the given cards from this Deck.

        Args:
            cards: The cards to remove.
            in_the: Where to remove the cards from (main, side, etc)
        """

        # using counterA - counterB results in a new Counter with only positive results
        match in_the:
            case InThe.MAIN:
                self.main.remove_cards(cards=cards)
            case InThe.SIDE:
                self.side.remove_cards(cards=cards)
            case InThe.CMDR:
                self.cmdr.remove_cards(cards=cards)
            case _:
                pass  # TODO(#75): failed to remove cards

    # endregion


class DeckNormalizer(utils.JsonNormalizer):
    """
    A simple class to use when normalizing non-serializable data from JSON.

    Usage:
        >>> deck.main = DeckNormalizer.deckpart(main_card_ids_json)
    """

    @classmethod
    def to_deck_part(
        cls,
        deck_part: DeckPart[CardT] | Mapping[CardT | ObjectId | str, int] | None,
        card_class: type[CardT] = OracleCard,
    ) -> DeckPart[CardT]:
        """
        Normalize DeckPart from JSON.

        Args:
            cards: A list of cards or scooze IDs of cards to normalize.

        Returns:
            An instance of DeckPart containing the given cards.
        """

        # TODO: write objectid code such that it works correctly and types are inherited correctly

        if deck_part is None or isinstance(deck_part, DeckPart):
            return deck_part
        elif all(isinstance(card, card_class) for card in deck_part.keys()):
            return DeckPart[CardT](cards=deck_part)
        elif all(isinstance(card, str) for card in deck_part.keys()):
            return DeckPart[CardT](cards={ObjectId(card_id): q for card_id, q in deck_part.items()})
        elif all(isinstance(card, ObjectId) for card in deck_part.keys()):
            with ScoozeApi() as api:
                return DeckPart[CardT](
                    cards={api.get_card_by(property_name="_id", value=card_id): q for card_id, q in deck_part.items()}
                )
