"""Data models for the task manager."""

from dataclasses import dataclass
from enum import Enum


class Priority(str, Enum):
    """Allowed priority levels for a task."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


@dataclass
class Task:
    """A single to-do item."""

    title: str
    priority: Priority
    done: bool = False