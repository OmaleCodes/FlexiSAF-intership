import pytest

from src.manager import TaskManager, TaskNotFoundError
from src.models import Priority


def test_add_task():
    manager = TaskManager()
    task = manager.add_task("Test", Priority.LOW)
    assert task.title == "Test"
    assert task.done is False


def test_add_task_with_empty_title_raises():
    manager = TaskManager()
    with pytest.raises(ValueError):
        manager.add_task("   ", Priority.LOW)


def test_remove_task():
    manager = TaskManager()
    manager.add_task("Test", Priority.LOW)
    manager.remove_task("Test")
    assert manager.list_tasks() == []


def test_remove_missing_task_raises():
    manager = TaskManager()
    with pytest.raises(TaskNotFoundError):
        manager.remove_task("Nope")


def test_complete_task():
    manager = TaskManager()
    manager.add_task("Test", Priority.LOW)
    manager.complete_task("Test")
    assert manager.list_tasks()[0].done is True


def test_list_tasks_filtered_by_priority():
    manager = TaskManager()
    manager.add_task("A", Priority.HIGH)
    manager.add_task("B", Priority.LOW)
    high_priority = manager.list_tasks(priority=Priority.HIGH)
    assert len(high_priority) == 1
    assert high_priority[0].title == "A"


def test_load_from_string():
    manager = TaskManager()
    manager.load_from_string("A,high,False;B,low,True")
    tasks = manager.list_tasks()
    assert len(tasks) == 2
    assert tasks[1].done is True


def test_load_from_string_bad_priority_raises():
    manager = TaskManager()
    with pytest.raises(ValueError):
        manager.load_from_string("A,urgent,False")