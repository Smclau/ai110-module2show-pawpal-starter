from pawpal_systems import Owner, Pet, Task, Schedule, Priority
from datetime import date, time

jordan = Owner("Jordan", 8)
mochi = Pet("Mochi", "cat", 3)
luna = Pet("Luna", "dog", 2)
task1 = Task("Walk Mochi", 30, Priority.HIGH, date.today(), time(9, 0))
task2 = Task("Feed Mochi", 15, Priority.MEDIUM, date.today(), time(8, 0))
task3 = Task("Feed Luna", 15, Priority.HIGH, date.today(), time(8, 30))

mochi.add_task(task1)
mochi.add_task(task2)
luna.add_task(task3)

jordan.add_pet(mochi)
jordan.add_pet(luna)

minutes_remaining = jordan.available_hours * 60
for pet in jordan.pets:
    s = Schedule(jordan, pet)
    s.generate_schedule()
    print(s.show_schedule())
    if s.overflow_tasks:
        print(f"  [Overflow: {len(s.overflow_tasks)} task(s) didn't fit]")
        for t in s.overflow_tasks:
            print(f"    - {t.task_name} ({t.duration_minutes} min, {t.priority.name})")
    minutes_remaining -= sum(t.duration_minutes for t in s.scheduled_tasks)

print(f"\n{jordan.owner_name} has {minutes_remaining} minutes of available time left today.")
