from pawpal_systems import Owner, Pet, Task, Schedule, Priority, RecurFrequency
from datetime import date, time

jordan = Owner("Jordan", 8)
mochi = Pet("Mochi", "cat", 3)
luna = Pet("Luna", "dog", 2)

# Tasks added out of order intentionally — sort_scheduled_by_time should fix the display
task1 = Task("Walk Mochi",    30, Priority.HIGH,   date.today(), time(9, 0))
task2 = Task("Feed Mochi",    15, Priority.MEDIUM, date.today(), time(8, 0))
task3 = Task("Brush Mochi",   10, Priority.LOW,    date.today(), time(14, 0))
task4 = Task("Evening play",  20, Priority.MEDIUM, date.today(), time(18, 0))
task5 = Task("Feed Luna",     15, Priority.HIGH,   date.today(), time(8, 0))   # same time as Feed Mochi — intentional cross-pet conflict
task6 = Task("Walk Luna",     45, Priority.HIGH,   date.today(), time(7, 0))

mochi.add_task(task1)  # 9:00am
mochi.add_task(task3)  # 2:00pm  (out of order)
mochi.add_task(task4)  # 6:00pm  (out of order)
mochi.add_task(task2)  # 8:00am  (out of order — earliest, added last)

luna.add_task(task5)   # 8:30am
luna.add_task(task6)   # 7:00am  (out of order — earlier, added last)

jordan.add_pet(mochi)
jordan.add_pet(luna)

# --- Mark some tasks complete to test filtering ---
task2.mark_complete()   # Feed Mochi — complete
task6.mark_complete()   # Walk Luna  — complete

# --- Schedule and print sorted output ---
print("=" * 50)
print("FULL SCHEDULES (sorted by time)")
print("=" * 50)
minutes_remaining = jordan.available_hours * 60
schedules = []
for pet in jordan.pets:
    s = Schedule(jordan, pet)
    s.generate_schedule()
    schedules.append(s)
    print(s.show_schedule())
    if s.overflow_tasks:
        print(f"  [Overflow: {len(s.overflow_tasks)} task(s) didn't fit]")
        for t in s.overflow_tasks:
            print(f"    - {t.task_name} ({t.duration_minutes} min, {t.priority.name})")
    minutes_remaining -= sum(t.duration_minutes for t in s.scheduled_tasks)

print(f"\n{jordan.owner_name} has {minutes_remaining} minutes of available time left today.")

# --- Cross-pet conflict detection ---
print("\n" + "=" * 50)
print("CROSS-PET CONFLICT CHECK")
print("=" * 50)
cross_conflicts = Schedule.check_cross_pet_conflicts(schedules)
if cross_conflicts:
    for task_a, pet_a, task_b, pet_b in cross_conflicts:
        print(f"  CONFLICT: '{task_a.task_name}' ({pet_a}) overlaps '{task_b.task_name}' ({pet_b})")
else:
    print("  No cross-pet conflicts.")

# --- Filter by status ---
print("\n" + "=" * 50)
print("FILTER: pending tasks for Mochi")
print("=" * 50)
for task in mochi.get_tasks_by_status("pending"):
    print(f"  - {task.task_name} @ {task.time.strftime('%I:%M %p') if task.time else 'Flexible'}")

print("\n" + "=" * 50)
print("FILTER: complete tasks for Luna")
print("=" * 50)
for task in luna.get_tasks_by_status("complete"):
    print(f"  - {task.task_name} (done)")

# --- Filter by pet name ---
print("\n" + "=" * 50)
print("FILTER: look up pet by name 'Luna'")
print("=" * 50)
found = jordan.get_pet("Luna")
if found:
    print(f"  Found: {found.get_pet_info()}")
    print(f"  Tasks: {[t.task_name for t in found.tasks]}")
