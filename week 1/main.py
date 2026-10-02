"""Entry point: runs the same scenario as the original script, refactored."""

from src.manager import TaskManager, TaskNotFoundError
from src.models import Priority


def _print_tasks(manager: TaskManager, priority: Priority | None = None) -> None:
    for task in manager.list_tasks(priority=priority):
        status = "done" if task.done else "pending"
        print(f"{task.title} - {task.priority.value} - {status}")


def main() -> None:
    manager = TaskManager()
    manager.load_from_string(
        "Write report,high,False;Email client,medium,True;Fix bug,high,False"
    )
    manager.add_task("Buy groceries", Priority.LOW)
    manager.complete_task("Buy groceries")

    try:
        manager.remove_task("Email client")
    except TaskNotFoundError as exc:
        print(f"Could not remove task: {exc}")

    print("\nAll tasks:")
    _print_tasks(manager)

    print("\nHigh priority tasks:")
    _print_tasks(manager, priority=Priority.HIGH)


if __name__ == "__main__":
    main()