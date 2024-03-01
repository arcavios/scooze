from collections import Counter
from sys import maxsize
from typing import Generic, Self

import scooze.utils as utils
from scooze.card import CardT
from scooze.catalogs import DecklistFormatter, Format, InThe, Legality
from scooze.deckpart import DeckDiff, DeckPart


class Deck(utils.ComparableObject, Generic[CardT]):
    """
    A class to represent a deck of Magic: the Gathering cards.

    Attributes:
        archetype: The archetype of this Deck.
        format: The format legality of the cards in this Deck.
        main: The main deck. Typically 60 cards minimum.
        side: The sideboard. Typically 15 cards maximum.
        cmdr: The command zone. Typically 1 or 2 cards in Commander formats.
        attractions: The attraction deck.
        stickers: The sticker deck.
    """

    def __init__(
        self,
        archetype: str | None = None,
        format: Format = Format.NONE,
        main: DeckPart[CardT] = None,
        side: DeckPart[CardT] = None,
        cmdr: DeckPart[CardT] = None,
        attractions: DeckPart[CardT] = None,
        stickers: DeckPart[CardT] = None,
        companion: CardT = None,
    ):
        self.archetype = archetype
        self.format = format

        self.main = main if main is not None else DeckPart()
        self.side = side if side is not None else DeckPart()
        self.cmdr = cmdr if cmdr is not None else DeckPart()
        self.attractions = attractions if attractions is not None else DeckPart()
        self.stickers = stickers if stickers is not None else DeckPart()

        self.companion = companion

    @property
    def cards(self) -> Counter[CardT]:
        return self.main.cards + self.side.cards + self.cmdr.cards + self.attractions.cards + self.stickers.cards

    def __str__(self):
        decklist = self.export()
        return f"""Archetype: {self.archetype}\n""" f"""Format: {self.format}\n""" f"""Decklist:\n{decklist}\n"""

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
            attractions=self.attractions.diff(other.attractions),
            stickers=self.stickers.diff(other.stickers),
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
        same_attractions = not bool(diff.attractions)
        same_stickers = not bool(diff.stickers)

        return same_main and same_side and same_cmdr and same_attractions and same_stickers

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
                cmdr_prefix = "Commander\n"
                companion_prefix = "Companion\n"
                main_prefix = "Deck\n"
                sb_prefix = "Sideboard\n"
                # TODO(#232): export specific versions to Arena <(SET) ###>
                # TODO(#50): filter out cards that are not on Arena. Log a WARNING with those cards.
            case DecklistFormatter.MTGO:
                decklist = f"{str(self.main)}"
                decklist += f"\n{str(self.side)}" if self.side else ""
                decklist += f"\n{str(self.cmdr)}" if self.cmdr else ""
                return decklist
                # TODO(#50): filter out cards that are not on MTGO. Log a WARNING with those cards.
            case _:
                cmdr_prefix = "Commander(s):\n"
                companion_prefix = "Companion:\n"
                main_prefix = "Deck:\n"
                sb_prefix = "Sideboard:\n"
                attraction_prefix = "Attractions:\n"
                sticker_prefix = "Stickers:\n"

        # ARENA and PLAINTEXT should be roughly the same.
        decklist = f"{cmdr_prefix}{str(self.cmdr)}\n" if self.cmdr else ""
        decklist += f"{companion_prefix}{self.companion.name}\n\n" if self.companion else ""
        decklist += f"{main_prefix}{str(self.main)}"
        decklist += f"\n{sb_prefix}{str(self.side)}" if self.side else ""

        # ARENA and MTGO not have attractions or stickers
        decklist += (
            f"\n{attraction_prefix}{str(self.attractions)}" if self.attractions and export_format is None else ""
        )
        decklist += f"\n{sticker_prefix}{str(self.stickers)}" if self.stickers and export_format is None else ""

        return decklist

    # TODO(#233): Add checks for commander formats to check cards for commanders' color identity
    # TODO(#234): Replace self.stickers.total() > 0 with a check to see if there are only stickers in the sticker deck
    # TODO(#236): Add `has_valid_companion()` and `has_valid_commanders(format)`. Call them in `is_legal(format)`
    def is_legal(self, format: Format = None) -> bool:
        """
        Determine if this Deck is legal in the given format.

        Default checks against `self.Format`. If `self.Format` is unset, checks
        against `Format.NONE`.

        - For cards with `Legality.RESTRICTED`, only 1 or fewer may be present
        throughout all deck parts.
        - For cards with `Legality.LEGAL`, only N or fewer may be present
        throughout all deck parts where N is determined by the max quantity of
        a single cards allowed by the given format.
        - For cards with `Legality.BANNED` or `Legality.NOT_LEGAL`, none may be
        present throughout all deck parts.

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

        # Only check attraction and sticker deck rules if there is at least 1 card in those parts.
        if self.attractions.total() > 0 and self.attractions.total() < utils.attractions_size(format)[0]:
            return False
        if self.stickers.total() > 0 and self.stickers.total() < utils.stickers_size(format)[0]:
            return False

        # Check deck is within maximum size requirements
        if self.main.total() > utils.main_size(format)[1]:
            return False
        if self.side.total() > utils.side_size(format)[1]:
            return False
        if self.cmdr.total() > utils.cmdr_size(format)[1]:
            return False

        # Only check attraction and sticker deck rules if there is at least 1 card in those parts.
        if self.attractions.total() > 0 and self.attractions.total() > utils.attractions_size(format)[1]:
            return False
        if self.stickers.total() > 0 and self.stickers.total() > utils.stickers_size(format)[1]:
            return False

        # Check card quantities do not exceed acceptable maximums per card
        for c, q in self.cards.items():
            c_legal = c.legalities[format] if format not in [Format.LIMITED, Format.NONE] else Legality.LEGAL

            if (c_legal is Legality.RESTRICTED and q > 1) or c_legal in [Legality.BANNED, Legality.NOT_LEGAL]:
                return False

            if q > utils.max_card_quantity(format) and q > utils.max_relentless_quantity(c.name):
                return False

        # Check attraction and sticker deck uniqueness rules
        if format not in [Format.LIMITED, Format.NONE]:
            if self.attractions.total() > len(self.attractions.cards):
                return False
            if self.stickers.total() > len(self.stickers.cards):
                return False

        return True

    def total_cards(self) -> int:
        """
        The number of cards in this Deck.
        """

        return (
            self.main.total() + self.side.total() + self.cmdr.total() + self.attractions.total() + self.stickers.total()
        )

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
            in_the: Where to add the card (main, side, etc.)
        """

        match in_the:
            case InThe.MAIN:
                self.main.add_card(card=card, quantity=quantity)
            case InThe.SIDE:
                self.side.add_card(card=card, quantity=quantity)
            case InThe.CMDR:
                self.cmdr.add_card(card=card, quantity=quantity)
            case InThe.ATTRACTIONS:
                self.attractions.add_card(card=card, quantity=quantity)
            case InThe.STICKERS:
                self.stickers.add_card(card=card, quantity=quantity)
            case _:
                pass  # TODO(#75): 'in' must be one of InThe.list()

    def add_cards(self, cards: Counter[CardT], in_the: InThe = InThe.MAIN) -> None:
        """
        Add the given cards to this Deck.

        Args:
            cards: The cards to add.
            in_the: Where to add the cards (main, side, etc.)
        """

        match in_the:
            case InThe.MAIN:
                self.main.add_cards(cards)
            case InThe.SIDE:
                self.side.add_cards(cards)
            case InThe.CMDR:
                self.cmdr.add_cards(cards)
            case InThe.ATTRACTIONS:
                self.attractions.add_cards(cards)
            case InThe.STICKERS:
                self.stickers.add_cards(cards)

    def remove_card(self, card: CardT, quantity: int = maxsize, in_the: InThe = InThe.MAIN) -> None:
        """
        Remove a given quantity of a given card from this Deck. If quantity is
        not provided, removes all copies.

        Args:
            card: The card to remove.
            quantity: The number of copies of the card to be removed.
            in_the: Where to remove the cards from (main, side, etc.)
        """

        # using counterA - counterB results in a new Counter with only positive results
        match in_the:
            case InThe.MAIN:
                self.main.remove_card(card=card, quantity=quantity)
            case InThe.SIDE:
                self.side.remove_card(card=card, quantity=quantity)
            case InThe.CMDR:
                self.cmdr.remove_card(card=card, quantity=quantity)
            case InThe.ATTRACTIONS:
                self.attractions.remove_card(card=card, quantity=quantity)
            case InThe.STICKERS:
                self.stickers.remove_card(card=card, quantity=quantity)
            case _:
                pass  # TODO(#75): failed to remove card

    def remove_cards(self, cards: Counter[CardT], in_the: InThe = InThe.MAIN) -> None:
        """
        Remove the given cards from this Deck.

        Args:
            cards: The cards to remove.
            in_the: Where to remove the cards from (main, side, etc.)
        """

        # using counterA - counterB results in a new Counter with only positive results
        match in_the:
            case InThe.MAIN:
                self.main.remove_cards(cards=cards)
            case InThe.SIDE:
                self.side.remove_cards(cards=cards)
            case InThe.CMDR:
                self.cmdr.remove_cards(cards=cards)
            case InThe.ATTRACTIONS:
                self.attractions.remove_cards(cards=cards)
            case InThe.STICKERS:
                self.stickers.remove_cards(cards=cards)
            case _:
                pass  # TODO(#75): failed to remove cards

    # endregion
