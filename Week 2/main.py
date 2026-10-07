
"""Entry point demonstrating the decorator, generator processor, and context manager
working together.
"""
 
from collections.abc import Callable
 
from src.decorators import retry, timed
from src.processor import process_readings, running_average
from src.resource_manager import managed_resource
 
SAMPLE_DATA = [
    "08:00,21.5",
    "08:01,22.0",
    "08:02,bad-value",
    "08:03,21.8",
    ",23.0",
    "08:05,22.4",
]
 
 
@timed
def summarize(lines: list[str]) -> list[float]:
    readings = process_readings(lines)
    return list(running_average(readings))
