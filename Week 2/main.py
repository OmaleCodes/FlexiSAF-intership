
"""Entry point demonstrating the decorator, generator processor, and context manager
working together.
"""
 
from collections.abc import Callable
 
from decorators import retry, timed
from processor import process_readings, running_average
from resource_manager import managed_resource
 
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

 
def make_flaky_task() -> Callable[[], str]:
    """Returns a function that fails twice before succeeding, to demonstrate retry."""
    state = {"attempts": 0}
 
    @retry(times=3, delay=0.05)
    def flaky_task() -> str:
        state["attempts"] += 1
        if state["attempts"] < 3:
            raise ValueError("Simulated transient failure")
        return "succeeded"
 
    return flaky_task
 
def main() -> None:
    print("Running averages:", summarize(SAMPLE_DATA))
 
    flaky_task = make_flaky_task()
    print("Flaky task result:", flaky_task())
 
    with managed_resource("demo-file") as resource:
        print(resource.use())
 
 
if __name__ == "__main__":
    main()