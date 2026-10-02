
from src.models import Priority, Task


class TaskNotFoundError(Exception):
    """Raised when a task with the given title does not exist."""


class TaskManager:
    """Keeps track of a list of tasks and the operations on them."""

    def __init__(self) -> None:
        self._tasks: list[Task] = []

    def add_task(self, title: str, priority: Priority, done: bool = False) -> Task:
        if not title.strip():
            raise ValueError("Task title cannot be empty.")
        task = Task(title=title, priority=priority, done=done)
        self._tasks.append(task)
        return task

    def remove_task(self, title: str) -> None:
        for index, task in enumerate(self._tasks):
            if task.title == title:
                del self._tasks[index]
                return
        raise TaskNotFoundError(f"No task named {title!r} found.")

    def complete_task(self, title: str) -> Task:
        for task in self._tasks:
            if task.title == title:
                task.done = True
                return task
        raise TaskNotFoundError(f"No task named {title!r} found.")

    def list_tasks(self, priority: Priority | None = None) -> list[Task]:
        if priority is None:
            return list(self._tasks)
        return [task for task in self._tasks if task.priority == priority]

    def load_from_string(self, data: str) -> None:
        """Bulk-load tasks from a string like 'title,priority,done;title2,...'."""
        if not data.strip():
            return
        for entry in data.split(";"):
            parts = entry.split(",")
            if len(parts) != 3:
                raise ValueError(f"Malformed task entry: {entry!r}")
            title, priority_str, done_str = parts
            try:
                priority = Priority(priority_str.strip().lower())
            except ValueError as exc:
                raise ValueError(
                    f"Unknown priority {priority_str!r} in entry {entry!r}"
                ) from exc
            done = done_str.strip().lower() == "true"
            self.add_task(title.strip(), priority, done)