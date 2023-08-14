from collections import Counter
from sys import maxsize

import scooze.utils as utils
from scooze.data.card import DecklistCard
from scooze.enums import DecklistFormatter, Format, InThe


class DeckPart:
    """
    A class to represent a part of a deck.

    Attributes
    ----------
        cards (Counter[DecklistCard]): The cards in this DeckPart.

    Methods
    -------
    total():
        The number of cards in this Deck.
    diff(other: DeckPart):
        Generates a diff between this DeckPart and another.
    add_card(card: DecklistCard, quantity: int):
        Adds a given quantity of a given card to this DeckPart.
    add_cards(cards: Counter[DecklistCard]):
        Adds the given cards to this DeckPart.
    remove_card(card: DecklistCard, quantity: int):
        Removes a given quantity of a given card from this DeckPart.
    remove_cards(cards: Counter[DecklistCard]):
        Removes the given cards from this DeckPart.
    """

    def __init__(self, cards: Counter[DecklistCard] = Counter()):
        # Deep copy of
        # TODO(#66): Add __copy__ and __deepcopy__ to Deck and DeckPart
        self.cards = Counter()
        self.cards.update(cards)

    def __eq__(self, other):
        return self.cards == other.cards

    def __ne__(self, other):
        return not self.__eq__(other)

    def __len__(self):
        return len(self.cards)

    def __str__(self):
        if len(self.cards) > 0:
            return "\n".join([f"{quantity} {card.name}" for card, quantity in self.cards.items()]) + "\n"
        else:
            return ""

    def total(self):
        """
        The number of cards in this DeckPart.
        """

        return self.cards.total()

    def diff(self, other):
        """
        Generates a diff between this DeckPart and another.

        Parameters:
            other (DeckPart): The other DeckPart.

        Returns:
            diff (dict[DecklistCard, tuple(int, int)]): Returns a dict with every card in both DeckParts and their counts.
        """

        return utils.dict_diff(self.cards, other.cards, NO_KEY=0)

    def add_card(self, card: DecklistCard, quantity: int = 1) -> None:
        """
        Adds a given quantity of a given card to this DeckPart.

        Parameters:
            card (DecklistCard): The card to add.
            quantity (int): The number of copies of the card to be added.
        """

        self.cards.update({card: quantity})

    def add_cards(self, cards: Counter[DecklistCard]) -> None:
        """
        Adds the given cards to this DeckPart.

        Parameters:
            cards (Counter[DecklistCard]): The cards to add.
        """

        self.cards.update(cards)

    def remove_card(self, card: DecklistCard, quantity: int = maxsize) -> None:
        """
        Removes a given quantity of a given card from this Deck. If quantity is not provided, removes all copies.

        Parameters:
            card (DecklistCard): The card to remove.
            quantity (int): The number of copies of the card to be removed.
        """

        # using counterA - counterB results in a new Counter with only positive results
        self.cards = self.cards - Counter({card: quantity})

    def remove_cards(self, cards: Counter[DecklistCard]) -> None:
        """
        Removes the given cards from this DeckPart.

        Parameters:
            cards (Counter[DecklistCard]): The cards to remove.
        """

        # using counterA - counterB results in a new Counter with only positive results
        self.cards = self.cards - cards


class Deck:
    """
    A class to represent a deck of Magic: the Gathering cards.

    Attributes
    ----------
    archetype : str
        The archetype of this Deck.
    format : Format
        The format legality of the cards in this Deck.
    main : DeckPart
        The main deck. Typically 60 cards minimum.
    side : DeckPart
        The sideboard. Typically 15 cards maximum.
    cmdr : DeckPart
        The command zone. Typically 1 card in Commander formats.

    Methods
    -------
    total():
        The number of cards in this Deck.
    diff(other: Deck):
        Generates a diff between this Deck and another.
    add_card(card: DecklistCard, quantity: int, in_the: InThe):
        Adds a given quantity of a given card to this Deck.
    add_cards(cards: Counter[DecklistCard], in_the: InThe):
        Adds the given cards to this Deck.
    remove_card(card: DecklistCard, quantity: int, in_the: InThe):
        Removes a given quantity of a given card from this Deck.
    remove_cards(cards: Counter[DecklistCard], in_the: InThe):
        Removes the given cards from this Deck.
    to_decklist(DecklistFormat):
        Exports the Deck as a str with the given DecklistFormat.
    """

    def __init__(
        self,
        archetype: str | None = None,
        format: Format = Format.NONE,
        main: DeckPart = DeckPart(),
        side: DeckPart = DeckPart(),
        cmdr: DeckPart = DeckPart(),
    ):
        self.archetype = archetype
        self.format = format

        # Deep copy of DeckPart
        # TODO(#66): Add __copy__ and __deepcopy__ to Deck and DeckPart
        self.main = DeckPart(cards=main.cards)
        self.side = DeckPart(cards=side.cards)
        self.cmdr = DeckPart(cards=cmdr.cards)

    def __eq__(self, other):
        return (
            self.archetype == other.archetype
            and self.format == other.format
            and self.main == other.main
            and self.side == other.side
            and self.cmdr == other.cmdr
        )

    def __ne__(self, other):
        return not self.__eq__(other)

    def __str__(self):
        decklist = self.to_decklist()
        return f"""Archetype: {self.archetype}\n""" f"""Format: {self.format}\n""" f"""Decklist:\n{decklist}\n"""

    def total(self) -> int:
        """
        The number of cards in this Deck.
        """

        return self.main.total() + self.side.total() + self.cmdr.total()

    def diff(self, other):
        """
        Generates a diff between this Deck and another.

        Parameters:
            other (Deck): The other Deck.

        Returns:
            diff (dict[str, dict[DecklistCard, tuple(int, int)]]): Returns a dict with keys for each deck part.
                Each contains a dict of every card in both decks and their counts.
        """

        # TODO: should this be a NamedTuple or something?
        return {
            "main_diff": self.main.diff(other.main),
            "side_diff": self.side.diff(other.side),
            "cmdr_diff": self.cmdr.diff(other.cmdr),
        }

    def same_list(self, other):
        # TODO: needs a new name
        """
        Determines if this Deck contains exactly the same cards as another.

        Parameters:
            other (Deck): The other Deck.

        Returns:
            same (bool): True if this Deck contains exactly the same cards as another, else False.
        """

        diff = self.diff(other)
        same_main = bool(diff["main_diff"])
        same_side = bool(diff["side_diff"])
        same_cmdr = bool(diff["cmdr_diff"])
        return same_main and same_side and same_cmdr

    def add_card(self, card: DecklistCard, quantity: int = 1, in_the: InThe = InThe.MAIN) -> None:
        """
        Adds a given quantity of a given card to this Deck.

        Parameters:
            card (DecklistCard): The card to add.
            quantity (int): The number of copies of the card to be added.
            in_the (InThe): Where to add the card (main, side, etc)
        """

        match in_the:
            case InThe.MAIN:
                self.main.add_card(card=card, quantity=quantity)
            case InThe.SIDE:
                self.side.add_card(card=card, quantity=quantity)
            case InThe.CMDR:
                self.cmdr.add_card(card=card, quantity=quantity)
            case _:
                pass  # 'in' must be one of InThe.list()

    def add_cards(self, cards: Counter[DecklistCard], in_the: InThe = InThe.MAIN) -> None:
        """
        Adds the given cards to this Deck.

        Parameters:
            cards (Counter[DecklistCard]): The cards to add.
            in_the (InThe): Where to add the cards (main, side, etc)
        """

        match in_the:
            case InThe.MAIN:
                self.main.add_cards(cards)
            case InThe.SIDE:
                self.side.add_cards(cards)
            case InThe.CMDR:
                self.cmdr.add_cards(cards)

    def remove_card(self, card: DecklistCard, quantity: int = maxsize, in_the: InThe = InThe.MAIN) -> None:
        """
        Removes a given quantity of a given card from this Deck. If quantity is not provided, removes all copies.

        Parameters:
            card (DecklistCard): The card to remove.
            quantity (int): The number of copies of the card to be removed.
            in_the (InThe): Where to remove the cards from (main, side, etc)
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
                pass  # failed to remove card

    def remove_cards(self, cards: Counter[DecklistCard], in_the: InThe = InThe.MAIN) -> None:
        """
        Removes the given cards from this Deck.

        Parameters:
            cards (Counter[DecklistCard]): The cards to remove.
            in_the (InThe): Where to remove the cards from (main, side, etc)
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
                pass  # failed to remove cards

    def to_decklist(self, decklist_formatter: DecklistFormatter = None) -> str:
        """
        Exports this Deck as a str with the given DecklistFormatter.

        Parameters:
            export_format (DecklistFormatter): The format of the exported Deck.

        Returns:
            decklist (str): A string containing the names and quantities of the cards in this Deck.
        """

        match decklist_formatter:
            case DecklistFormatter.ARENA:
                sb_prefix = "Sideboard\n"
                # TODO(#50): filter out cards that are not on Arena. Log a WARNING with those cards.
            case DecklistFormatter.MTGO:
                sb_prefix = "SIDEBOARD:\n"
                # TODO(#50): filter out cards that are not on MTGO. Log a WARNING with those cards.
            case _:
                sb_prefix = ""  # Default
        sb_prefix = "\n" + sb_prefix

        # TODO(#64): may differ between MTGO, Arena, plain text
        cmdr_prefix = "Commander\n"
        cmdr_suffix = "\n"

        # Build the decklist string
        main = str(self.main) if len(self.main) > 0 else ""
        side = (sb_prefix + str(self.side)) if len(self.side) > 0 else ""
        cmdr = (cmdr_prefix + str(self.cmdr) + cmdr_suffix) if len(self.cmdr) > 0 else ""
        decklist = f"{cmdr}{main}{side}"
        return decklist
