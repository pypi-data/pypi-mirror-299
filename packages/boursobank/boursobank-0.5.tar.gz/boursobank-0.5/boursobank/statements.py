"""Parses BoursoBank account statements."""

import datetime as dt
import logging
import re
from contextlib import suppress
from dataclasses import dataclass
from decimal import Decimal
from pathlib import Path
from typing import Any, Literal, Optional

from pypdf import PdfReader
from rich.console import Console
from rich.table import Table

__version__ = "0.5"

DATE_RE = r"([0-9]{1,2}/[0-9]{2}/[0-9]{2,4})"

HEADER_VALUE_PATTERN = rf"""\s*
        (?P<date>{DATE_RE})\s+
        (?P<RIB>[0-9]{{5}}\s+[0-9]{{5}}\s+[0-9]{{11}}\s+[0-9]{{2}})\s+
        (
            (?P<devise>[A-Z]{{3}})
            |
            (?P<card_number>[0-9]{{4}}\*{{8}}[0-9]{{4}})
        )\s+
        (?P<periode>(du)?\s+{DATE_RE}\s+(au\s+)?{DATE_RE})\s+
        """

RE_CARD_OWNER = [  # First pattern is tried first
    re.compile(r"Porteur\s+de\s+la\s+carte\s+:\s+(?P<porteur>.*)$", flags=re.M),
    re.compile(
        r"44\s+rue\s+Traversiere\s+CS\s+80134\s+92772\s+"
        r"Boulogne-Billancourt\s+Cedex\s+(?P<porteur>.*)$",
        flags=re.M,
    ),
]


logger = logging.getLogger(__name__)


def parse_decimal(amount: str) -> Decimal:
    """Parse a French amount like 1.234,56 to a Decimal instance."""
    return Decimal(amount.replace(".", "").replace(",", "."))


class Line:
    """Represents one line (debit or credit) in a bank statement."""

    PATTERN = re.compile(
        rf"\s+(?P<date>{DATE_RE})\s*(?P<label>.*)\s+"
        rf"(?P<valeur>{DATE_RE})\s+(?P<amount>[0-9.,]+)$"
    )

    def __init__(self, statement: "Statement", line: str):
        self.statement = statement
        self.line = line
        self.description = ""
        if (match := self.PATTERN.match(line)) is not None:
            self.match = match
        else:
            raise ValueError(f"{self.__class__.__name__} cannot parse line: {line!r}")

    @property
    def label(self) -> str:
        """Line short description."""
        return re.sub(r"\s+", " ", self.match["label"]).strip()

    def add_description(self, description_line: str) -> None:
        """Add a line to a long description."""
        description_line = re.sub(r"\s+", " ", description_line).strip()
        if not description_line:
            return
        if self.description:
            self.description += "\n"
        self.description += description_line

    @property
    def direction(self) -> Literal["-", "+"]:
        """returns '-' for outbound, and '+' for inbound.

        There's two columns in the PDF: Débit, Crédit.

        Sadly we don't really know where they are, and there's
        variations depending on the format, so we have to use an
        heuristic.
        """
        if self.statement.headers.date < dt.date(2021, 1, 1):
            column_at = 98
        else:
            column_at = 225

        column = self.match.start("amount")
        return "-" if column < column_at else "+"

    @property
    def abs_amount(self) -> Decimal:
        """Absolute value of the amount for this line."""
        return parse_decimal(self.match["amount"])

    @property
    def amount(self) -> Decimal:
        """Amount for this line. Positive for credits, negative for debits."""
        return self.abs_amount if self.direction == "+" else -self.abs_amount

    def __str__(self) -> str:
        return f"{self.label} {self.amount}"

    @classmethod
    def from_string(cls, statement: "Statement", line: str) -> Optional["Line"]:
        """Just an alternative constructor that can return None."""
        with suppress(ValueError):
            return cls(statement, line)
        return None


class AccountLine(Line):
    """Represents one line (debit or credit) in a bank statement."""

    PATTERN = re.compile(
        rf"\s+(?P<date>{DATE_RE})\s*(?P<label>.*)\s+"
        rf"(?P<valeur>{DATE_RE})\s+(?P<amount>[0-9.,]+)$"
    )


class BalanceBeforeLine(AccountLine):
    """Line, at the top of the statement, with the balance at the start of the month."""

    PATTERN = re.compile(rf"\s+SOLDE\s+AU\s+:\s+{DATE_RE}\s+(?P<amount>[0-9,.]+)$")


class BalanceAfterLine(AccountLine):
    """Line, at the bottom of the statement, with the balance at the end of the month."""

    PATTERN = re.compile(r"\s+Nouveau\s+solde\s+en\s+EUR\s+:\s+(?P<amount>[0-9,.]+)$")


class CardLine(Line):
    """Represents one line (debit or credit) in a card statement."""

    PATTERN = re.compile(
        rf"\s*(?P<date>{DATE_RE})\s+CARTE\s+(?P<valeur>{DATE_RE})"
        rf"\s+(?P<label>.*)\s+(?P<amount>[0-9.,]+)$"
    )

    @property
    def direction(self) -> Literal["-"]:
        """returns '-' for outbound, and '+' for inbound.

        As it's a card, we have only one column: debits.
        """
        return "-"

    @classmethod
    def from_string(cls, statement: "Statement", line: str) -> Line | None:
        """For old statements, use a specific parser with Francs."""
        if statement.headers.date < dt.date(2020, 6, 1):
            with suppress(ValueError):
                return CardLineWithFrancs(statement, line)
        with suppress(ValueError):
            return cls(statement, line)
        return None


class CardLineWithFrancs(CardLine):
    """Represents one line (debit or credit) in a card statement."""

    PATTERN = re.compile(
        rf"\s*(?P<date>{DATE_RE})\s+CARTE\s+(?P<valeur>{DATE_RE}|[0-9]{{8}})"
        rf"\s+(?P<label>.*)\s+(?P<amount>[0-9.,]+)\s+(?P<amount_francs>[0-9.,]+)$"
    )


class CardLineDebit(CardLine):
    """Represents one debit line in a card statement."""

    PATTERN = re.compile(
        rf"\s+A\s+VOTRE\s+DEBIT\s+LE\s+{DATE_RE}\s+(?P<amount>[0-9.,]+)$"
    )

    @classmethod
    def from_string(cls, statement: "Statement", line: str) -> Line | None:
        """For old statements, use a specific parser with Francs."""
        if statement.headers.date < dt.date(2020, 6, 1):
            with suppress(ValueError):
                return CardLineDebitWithFrancs(statement, line)
        with suppress(ValueError):
            return cls(statement, line)
        return None


class CardLineDebitWithFrancs(CardLineDebit):
    """Around 2019-03-08 the date format changed from 08032019 to 08/03/19."""

    PATTERN = re.compile(
        rf"\s+A\s+VOTRE\s+DEBIT\s+LE\s+{DATE_RE}\s+"
        rf"(?P<amount>[0-9.,]+)\s+(?P<debit_francs>[0-9.,]+)$"
    )


@dataclass
class StatementHeaders:
    """Global informations about a statement.

    This is often represented as a small table on the top of the statement.
    """

    emit_date: dt.date
    date: dt.date
    RIB: str  # pylint: disable=invalid-name  # as it's an accronym
    devise: str
    card_number: str | None = None
    card_owner: str | None = None


class Statement:
    """Base class for either an account statement or a credit card statement.

    Statement class methods `from_pdf` and `from_string` can be used blindly:
    they return either an accountstatement or a CardStatement as
    needed.
    """

    _line_parser = Line

    def __init__(self, file: Path, text: str, headers: StatementHeaders, **kwargs: Any):
        self.file = file
        self.text = text
        self.headers = headers
        self.lines: list[Line] = []
        super().__init__(**kwargs)
        self.parse()

    def parse(self) -> None:
        """To be implemented in childs.

        See  parse() from or AccountStatement.
        """
        raise NotImplementedError()

    def validate(self) -> None:
        """To be implemented in childs.

        See validate() from or AccountStatement.
        """
        raise NotImplementedError()

    @classmethod
    def from_string(cls, string: str, file: Path | None = None) -> "Statement":
        """Builds a statement from a string, usefull for tests purposes."""
        headers = cls._parse_header(string, file)
        if headers.card_number:  # pylint: disable=no-else-return  # It prefer my way
            return CardStatement(file=file, text=string, headers=headers)
        else:
            return AccountStatement(file=file, text=string, headers=headers)

    @classmethod
    def from_pdf(cls, file: Path) -> "Statement":
        """Builds a statement from a PDF file."""
        buf = []
        for page in PdfReader(file).pages:
            try:
                buf.append(
                    page.extract_text(extraction_mode="layout", orientations=(0,))
                )
            except AttributeError:
                # Maybe just a blank page
                pass  # logger.exception("while parsing PDF %s", file)
        return cls.from_string("\n".join(buf), file)

    @staticmethod
    def _parse_header(text: str, file: Path | None) -> StatementHeaders:
        for text_line in text.splitlines():
            if values := re.match(HEADER_VALUE_PATTERN, text_line, re.VERBOSE):
                return StatementHeaders(
                    emit_date=dt.datetime.strptime(values["date"], "%d/%m/%Y").date(),
                    date=(
                        dt.datetime.strptime(values["periode"].split()[-1], "%d/%m/%Y")
                        .date()
                        .replace(day=1)
                    ),
                    RIB=re.sub(r"\s+", " ", values["RIB"]),
                    devise=values["devise"],
                    card_number=values["card_number"],
                )
        raise ValueError(f"Cannot parse headers in {file!r}")

    def _parse_lines(self, text: str) -> None:
        current_line = None
        for text_line in text.splitlines():
            if text_line.strip() == "":
                if current_line:
                    self.lines.append(current_line)
                current_line = None
            if line := self._line_parser.from_string(self, text_line):
                if current_line:
                    self.lines.append(current_line)
                current_line = line
            elif current_line:
                current_line.add_description(text_line)
        if current_line:
            self.lines.append(current_line)

    def __str__(self) -> str:
        buf = [f"Date: {self.headers.date}", f"RIB: {self.headers.RIB}"]
        for line in self.lines:
            buf.append(str(line))
        return "\n".join(buf)

    def pretty_print(self, show_descriptions: bool) -> None:
        """Display a colorfull ascii art table of this statement."""
        table = Table()
        table.add_column("Label", justify="right", style="cyan", no_wrap=True)
        table.add_column("Value", style="magenta")
        for line in self.lines:
            if line.description and show_descriptions:
                table.add_row(line.label + "\n" + line.description, str(line.amount))
            else:
                table.add_row(line.label, str(line.amount))

        Console().print(table)


class AccountStatement(Statement):
    """Represents a statement for a bank account (not a credit card).

    Use the classmethods from Statement to get one.
    """

    _line_parser = AccountLine

    def __init__(self, **kwargs: Any):
        self.balance_before = Decimal(0)
        self.balance_after = Decimal(0)
        super().__init__(**kwargs)

    def validate(self) -> None:
        """Consistency check.

        It just verifies that all the lines sum to the right total.
        """
        computed = sum(line.amount for line in self.lines)
        if self.balance_before + computed != self.balance_after:
            raise ValueError(
                f"Inconsistent total, found: {self.balance_before + computed!r}, "
                f"expected: {self.balance_after!r} in {self.file}."
            )

    def parse(self) -> None:
        start, stop = self._parse_soldes()
        self._parse_lines("\n".join(self.text.splitlines()[start + 1 : stop]))

    def _parse_soldes(self) -> tuple[int, int]:
        start = stop = 0
        for lineno, text in enumerate(self.text.splitlines()):
            if before := BalanceBeforeLine.from_string(self, text):
                self.balance_before = before.amount
                start = lineno
            if after := BalanceAfterLine.from_string(self, text):
                self.balance_after = after.amount
                stop = lineno
        return start, stop

    def pretty_print(self, show_descriptions: bool) -> None:
        table = Table(title=str(self.file))
        table.add_column("Date")
        table.add_column("RIB")
        table.add_row(str(self.headers.date), self.headers.RIB)
        Console().print(table)
        super().pretty_print(show_descriptions)


class CardStatement(Statement):
    """Represents a statement for a credit card.

    Use the classmethods from Statement to get one.
    """

    _line_parser = CardLine

    def __init__(self, **kwargs: Any):
        self.card_debit = Decimal(0)
        super().__init__(**kwargs)

    def validate(self) -> None:
        """Consistency check.

        It just verifies that all the lines sum to the right total.
        """
        computed = sum(line.amount for line in self.lines)
        if computed != self.card_debit:
            raise ValueError(
                f"Inconsistent total, found: {computed!r}, "
                f"expected: {self.card_debit!r} in {self.file}."
            )

    def parse(self) -> None:
        self._parse_card_owner()
        self._parse_card_debit()
        self._parse_lines(self.text)

    def _parse_card_debit(self) -> None:
        for text in self.text.splitlines():
            if line := CardLineDebit.from_string(self, text):
                self.card_debit = line.amount
                return

    def _parse_card_owner(self) -> None:
        for pattern in RE_CARD_OWNER:
            if match := pattern.search(self.text):
                self.headers.card_owner = re.sub(r"\s+", " ", match["porteur"])
                break

    def pretty_print(self, show_descriptions: bool) -> None:
        table = Table(title=str(self.file))
        table.add_column("Date")
        table.add_column("RIB")
        table.add_column("Card number")
        table.add_column("Card debit")
        table.add_column("Card owner")
        table.add_row(
            str(self.headers.date),
            self.headers.RIB,
            self.headers.card_number,
            str(self.card_debit),
            self.headers.card_owner,
        )
        Console().print(table)
        super().pretty_print(show_descriptions)
