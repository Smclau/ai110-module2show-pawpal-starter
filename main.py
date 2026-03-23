from pawpal_systems import Owner, Pet, Task, Schedule, Priority
from datetime import date, time

jordan = Owner("Jordan", 8)
mochi = Pet("Mochi", "cat", 3)
luna = Pet("Luna", "dog", 2)
task1 = Task("Walk Mochi", 30, Priority.HIGH, date(2026, 3, 25), time(9, 0))
task2 = Task("Feed Mochi", 15, Priority.MEDIUM, date(2026, 3, 25), time(8, 0))
task3 = Task("Feed Luna", 15, Priority.HIGH, date(2026, 3, 25), time(8, 30))

mochi.add_task(task1)
mochi.add_task(task2)
luna.add_task(task3)

jordan.add_pet(mochi)
jordan.add_pet(luna)

mochi_schedule = Schedule(jordan, mochi)
mochi_schedule.generate_schedule()
print(mochi_schedule.show_schedule())

luna_schedule = Schedule(jordan, luna)
luna_schedule.generate_schedule()
print(luna_schedule.show_schedule())
