"""
Simple Task Manager (BEFORE refactor)

Run it:
    python task_manager.py

GOAL: 

- Split responsibilities into clean functions/modules
- Add type hints
- Replace the raw dicts with dataclasses
- Add proper, meaningful error handling
- Add linting/formatting (black, ruff/flake8)
- Add tests
- Organize it into a proper project structure (src/, tests/, etc.)

Modifying only how it's built, not what works for the user
"""

tasks = []


def add_task(title, priority, done=False):
    task = {}
    task["title"] = title
    task["priority"] = priority
    task["done"] = done
    tasks.append(task)
    print("added task:", title)


def remove_task(title):
    global tasks
    new_tasks = []
    found = False
    for t in tasks:
        if t["title"] == title:
            found = True
            continue
        new_tasks.append(t)
    tasks = new_tasks
    if not found:
        print("couldn't find that task")


def complete_task(title):
    for t in tasks:
        if t["title"] == title:
            t["done"] = True
            return
    print("no task with that name")


def show_tasks(filter_priority=None):
    for t in tasks:
        if filter_priority != None:
            if t["priority"] != filter_priority:
                continue
        status = "done" if t["done"] else "pending"
        print(t["title"], "-", t["priority"], "-", status)


def load_from_string(data):
    # data looks like: "title,priority,done;title2,priority2,done2"
    try:
        entries = data.split(";")
        for e in entries:
            parts = e.split(",")
            title = parts[0]
            priority = parts[1]
            done = True if parts[2] == "True" else False
            add_task(title, priority, done)
    except:
        print("something went wrong loading data")


def main():
    load_from_string("Write report,high,False;Email client,medium,True;Fix bug,high,False")
    add_task("Buy groceries", "low")
    complete_task("Buy groceries")
    remove_task("Email client")

    print("\nAll tasks:")
    show_tasks()

    print("\nHigh priority tasks:")
    show_tasks("high")


if __name__ == "__main__":
    main()