import pytest
from datetime import date, time
from pawpal_systems import Owner, Pet, Task, Schedule, Priority, RecurFrequency

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


def test_invalid_duration_raises():
    with pytest.raises(ValueError):
        Task("Bad task", 0, Priority.HIGH, date(2026, 3, 27))


def test_schedule_overflow():
    owner = Owner("Jordan", 1)  # 60 minutes available
    pet = Pet("Mochi", "cat", 3)
    pet.add_task(Task("Walk", 45, Priority.HIGH,   date(2026, 3, 27), time(9, 0)))
    pet.add_task(Task("Bath", 30, Priority.MEDIUM, date(2026, 3, 27), time(10, 0)))
    schedule = Schedule(owner, pet)
    schedule.generate_schedule()
    assert len(schedule.scheduled_tasks) == 1
    assert len(schedule.overflow_tasks) == 1


def test_schedule_no_tasks():
    owner = Owner("Jordan", 8)
    pet = Pet("Ghost", "cat", 1)
    schedule = Schedule(owner, pet)
    schedule.generate_schedule()
    assert schedule.scheduled_tasks == []
    assert schedule.overflow_tasks == []


def test_priority_sort_order():
    owner = Owner("Jordan", 8)
    pet = Pet("Mochi", "cat", 3)
    pet.add_task(Task("Low task",  10, Priority.LOW,    date(2026, 3, 27)))
    pet.add_task(Task("High task", 20, Priority.HIGH,   date(2026, 3, 27)))
    pet.add_task(Task("Med task",  15, Priority.MEDIUM, date(2026, 3, 27)))
    schedule = Schedule(owner, pet)
    schedule.sort_tasks_by_priority()
    priorities = [t.priority for t in pet.tasks]
    assert priorities == [Priority.HIGH, Priority.MEDIUM, Priority.LOW]


def test_conflict_detection():
    owner = Owner("Jordan", 8)
    pet = Pet("Mochi", "cat", 3)
    t1 = Task("Walk", 30, Priority.HIGH,   date(2026, 3, 27), time(9, 0))
    t2 = Task("Feed", 20, Priority.MEDIUM, date(2026, 3, 27), time(9, 15))  # overlaps Walk
    pet.add_task(t1)
    pet.add_task(t2)
    schedule = Schedule(owner, pet)
    schedule.generate_schedule()
    assert len(schedule.check_conflicts()) == 1


def test_no_conflict_non_overlapping():
    owner = Owner("Jordan", 8)
    pet = Pet("Mochi", "cat", 3)
    t1 = Task("Walk", 30, Priority.HIGH,   date(2026, 3, 27), time(9, 0))
    t2 = Task("Feed", 20, Priority.MEDIUM, date(2026, 3, 27), time(10, 0))  # starts after Walk ends
    pet.add_task(t1)
    pet.add_task(t2)
    schedule = Schedule(owner, pet)
    schedule.generate_schedule()
    assert schedule.check_conflicts() == []


def test_recurring_next_occurrence():
    task = Task("Feed", 15, Priority.HIGH, date(2026, 3, 27), recur=RecurFrequency.DAILY)
    next_task = task.create_next_occurrence()
    assert next_task is not None
    assert next_task.due == date(2026, 3, 28)


def test_non_recurring_no_next():
    task = Task("Bath", 20, Priority.LOW, date(2026, 3, 27), recur=RecurFrequency.NONE)
    assert task.create_next_occurrence() is None


# --- Required: Sorting Correctness ---
def test_sort_scheduled_by_time():
    """Tasks added out of order should appear in chronological order after sorting."""
    owner = Owner("Jordan", 8)
    pet = Pet("Mochi", "cat", 3)
    pet.add_task(Task("Evening walk", 20, Priority.LOW,    date(2026, 3, 27), time(18, 0)))
    pet.add_task(Task("Morning feed", 15, Priority.HIGH,   date(2026, 3, 27), time(8, 0)))
    pet.add_task(Task("Afternoon nap", 30, Priority.MEDIUM, date(2026, 3, 27), time(13, 0)))
    schedule = Schedule(owner, pet)
    schedule.generate_schedule()
    schedule.sort_scheduled_by_time()
    times = [t.time for t in schedule.scheduled_tasks]
    assert times == sorted(times)


# --- Required: Recurrence Logic ---
def test_mark_complete_daily_creates_next_task():
    """Marking a daily task complete and calling create_next_occurrence produces a new task due the next day."""
    pet = Pet("Mochi", "cat", 3)
    task = Task("Feed Mochi", 15, Priority.HIGH, date(2026, 3, 27), time(8, 0), recur=RecurFrequency.DAILY)
    pet.add_task(task)

    task.mark_complete()
    next_task = task.create_next_occurrence()

    assert task.complete == True
    assert next_task is not None
    assert next_task.due == date(2026, 3, 28)   # one day later
    assert next_task.complete == False            # starts fresh


# --- Required: Conflict Detection (exact same time) ---
def test_conflict_same_start_time():
    """Two tasks starting at the exact same time should be flagged as a conflict."""
    owner = Owner("Jordan", 8)
    pet = Pet("Mochi", "cat", 3)
    t1 = Task("Walk",  30, Priority.HIGH,   date(2026, 3, 27), time(9, 0))
    t2 = Task("Feed",  15, Priority.MEDIUM, date(2026, 3, 27), time(9, 0))  # identical start
    pet.add_task(t1)
    pet.add_task(t2)
    schedule = Schedule(owner, pet)
    schedule.generate_schedule()
    conflicts = schedule.check_conflicts()
    assert len(conflicts) == 1
    conflict_names = {conflicts[0][0].task_name, conflicts[0][1].task_name}
    assert conflict_names == {"Walk", "Feed"}
