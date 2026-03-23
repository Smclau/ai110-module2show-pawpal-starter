import pytest
from datetime import date, time
from pawpal_systems import Owner, Pet, Task, Schedule, Priority

def test_mark_complete():
    task = Task("Walk Mochi", 30, Priority.HIGH, date(2026, 3, 25), time(9, 0))
    assert task.complete == False
    task.mark_complete()
    assert task.complete == True

def test_add_task():
    mochi = Pet("Mochi", "cat", 3)
    task = Task("Feed Mochi", 30, Priority.HIGH, date(2026, 3, 25), time(10, 0))
    assert len(mochi.tasks) == 0
    mochi.add_task(task)
    assert len(mochi.tasks) == 1


