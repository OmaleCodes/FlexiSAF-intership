"""The record model and the allowed values."""

from dataclasses import dataclass

# A set is used because "is this rating allowed?" is answered instantly.
VALID_RATINGS = {
    "TV-MA", "TV-14", "TV-PG", "R", "PG-13", "TV-Y7", "TV-Y",
    "PG", "TV-G", "NR", "G", "TV-Y7-FV", "NC-17", "UR",
}  # fmt: skip

VALID_TYPES = ("Movie", "TV Show")


class InvalidRecordError(Exception):
    """Raised when a row breaks a rule. The message says which rule."""


@dataclass
class Record:
    """One clean row from the dataset."""

    show_id: str
    content_type: str
    title: str
    release_year: int
    rating: str
    duration: str
    director: str | None = None
    country: str | None = None
    date_added: str | None = None