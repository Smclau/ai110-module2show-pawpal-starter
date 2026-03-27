from dataclasses import dataclass, field
from datetime import date, time, timedelta
from enum import Enum
from typing import Optional


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


class RecurFrequency(Enum):
    NONE = 0
    DAILY = 1
    WEEKLY = 7


@dataclass
class Task:
    task_name: str
    duration_minutes: int
    priority: Priority
    due: date
    time: Optional[time] = None
    complete: bool = False
    recur: RecurFrequency = RecurFrequency.NONE

    def __post_init__(self):
        """Validate that duration_minutes is at least 1."""
        if self.duration_minutes < 1:
            raise ValueError(f"duration_minutes must be at least 1, got {self.duration_minutes}")

    def is_overdue(self) -> bool:
        """Return True if the task is not complete and its due date has passed."""
        return not self.complete and self.due < date.today()

    def mark_complete(self):
        """Mark this task as complete."""
        self.complete = True

    def mark_incomplete(self):
        """Mark this task as incomplete."""
        self.complete = False

    def next_due(self) -> Optional[date]:
        """Return the next due date based on recurrence, or None if not recurring."""
        if self.recur == RecurFrequency.NONE:
            return None
        return self.due + timedelta(days=self.recur.value)

    def advance_if_recurring(self):
        """If complete and recurring, reset to the next due date and mark incomplete."""
        if self.complete and self.recur != RecurFrequency.NONE:
            self.due = self.next_due()
            self.complete = False

    def create_next_occurrence(self):
        """Return a new Task for the next occurrence of this recurring task, or None if not recurring."""
        if self.recur == RecurFrequency.NONE:
            return None
        return Task(
            task_name=self.task_name,
            duration_minutes=self.duration_minutes,
            priority=self.priority,
            due=self.next_due(),
            time=self.time,
            complete=False,
            recur=self.recur,
        )

    def edit_time(self, new_time: time):
        """Update the scheduled time for this task."""
        if not isinstance(new_time, time):
            raise ValueError(f"new_time must be a time object, got {type(new_time)}")
        self.time = new_time

    def edit_priority(self, new_priority: Priority):
        """Update the priority level of this task."""
        self.priority = new_priority

    def display_task(self):
        """Return a formatted string of all task details."""
        scheduled_time = self.time.strftime("%I:%M %p") if self.time else "Flexible"
        status = "Complete" if self.complete else "Pending"
        recur_label = f" ({self.recur.name.lower()})" if self.recur != RecurFrequency.NONE else ""
        return (
            f"Task: {self.task_name}{recur_label}\n"
            f"  Priority: {self.priority.name}\n"
            f"  Duration: {self.duration_minutes} mins\n"
            f"  Due: {self.due}\n"
            f"  Time: {scheduled_time}\n"
            f"  Status: {status}"
        )


@dataclass
class Pet:
    pet_name: str
    pet_type: str
    pet_age: float
    tasks: list = field(default_factory=list)

    def add_task(self, task: Task):
        """Add a task to this pet's task list."""
        self.tasks.append(task)

    def rmv_task(self, task_name: str):
        """Remove a task from this pet's task list by name."""
        self.tasks = [t for t in self.tasks if t.task_name != task_name]

    def get_tasks_by_status(self, status: str) -> list:
        """Return tasks filtered by 'pending', 'complete', or 'overdue'. Returns all if unrecognized."""
        if status == "complete":
            return [t for t in self.tasks if t.complete]
        elif status == "pending":
            return [t for t in self.tasks if not t.complete]
        elif status == "overdue":
            return [t for t in self.tasks if t.is_overdue()]
        return list(self.tasks)

    def get_pet_info(self):
        """Return a formatted string of this pet's basic information."""
        return f"{self.pet_name} is a {self.pet_type}."

    def show_tasks(self):
        """Return a formatted string of all tasks assigned to this pet."""
        return "\n\n".join(t.display_task() for t in self.tasks)


class Owner:
    def __init__(self, owner_name: str, available_hours: int):
        self.owner_name = owner_name
        self.available_hours = available_hours
        self.pets: list = []

    def add_pet(self, pet):
        """Add a pet to this owner's pet list."""
        self.pets.append(pet)

    def rmv_pet(self, pet_name: str):
        """Remove a pet from this owner's pet list by name."""
        self.pets = [p for p in self.pets if p.pet_name != pet_name]

    def get_pet(self, pet_name: str):
        """Return a pet by name, or None if not found."""
        for pet in self.pets:
            if pet.pet_name == pet_name:
                return pet
        return None

    def get_owner_info(self):
        """Return a formatted string of this owner's name, available hours, and pet count."""
        return f"{self.owner_name} has {self.available_hours} hours available per day to spend with their {len(self.pets)} pet(s)."


class Schedule:
    def __init__(self, owner: Owner, pet: Pet):
        self.owner = owner
        self.pet = pet
        self.scheduled_tasks: list = []
        self.overflow_tasks: list = []

    def sort_tasks_by_priority(self):
        """Sort tasks highest to lowest priority; break ties by shortest duration first."""
        self.pet.tasks = sorted(
            self.pet.tasks,
            key=lambda task: (task.priority.value, -task.duration_minutes),
            reverse=True
        )

    def sort_scheduled_by_time(self):
        """Sort scheduled tasks by time; flexible (no time) tasks go last."""
        self.scheduled_tasks.sort(
            key=lambda t: (t.time is None, t.time if t.time is not None else time.min)
        )

    def check_conflicts(self):
        """Return pairs of scheduled tasks whose time windows overlap (same pet)."""
        conflicts = []
        tasks_with_time = [t for t in self.scheduled_tasks if t.time is not None and not t.complete]
        for i, task_a in enumerate(tasks_with_time):
            for task_b in tasks_with_time[i + 1:]:
                a_start = task_a.time.hour * 60 + task_a.time.minute
                a_end = a_start + task_a.duration_minutes
                b_start = task_b.time.hour * 60 + task_b.time.minute
                b_end = b_start + task_b.duration_minutes
                if a_start < b_end and b_start < a_end:
                    conflicts.append((task_a, task_b))
        return conflicts

    def conflict_warnings(self) -> list[str]:
        """Return a list of human-readable warning strings for any time conflicts."""
        warnings = []
        for task_a, task_b in self.check_conflicts():
            warnings.append(
                f"Warning: '{task_a.task_name}' ({task_a.time.strftime('%I:%M %p')}) "
                f"and '{task_b.task_name}' ({task_b.time.strftime('%I:%M %p')}) overlap."
            )
        return warnings

    @staticmethod
    def check_cross_pet_conflicts(schedules: list):
        """Return conflicts between tasks from different pets that overlap in time."""
        conflicts = []
        all_tasks = []
        for s in schedules:
            for task in s.scheduled_tasks:
                if task.time is not None and not task.complete:
                    all_tasks.append((task, s.pet.pet_name))

        for i, (task_a, pet_a) in enumerate(all_tasks):
            for (task_b, pet_b) in all_tasks[i + 1:]:
                if pet_a == pet_b:
                    continue
                a_start = task_a.time.hour * 60 + task_a.time.minute
                a_end = a_start + task_a.duration_minutes
                b_start = task_b.time.hour * 60 + task_b.time.minute
                b_end = b_start + task_b.duration_minutes
                if a_start < b_end and b_start < a_end:
                    conflicts.append((task_a, pet_a, task_b, pet_b))
        return conflicts

    def generate_schedule(self):
        """Build the schedule by fitting tasks into the owner's available hours."""
        self.sort_tasks_by_priority()
        total_minutes = self.owner.available_hours * 60

        minutes_used = 0
        for task in self.pet.tasks:
            if task.complete:
                continue
            elif minutes_used + task.duration_minutes <= total_minutes:
                self.scheduled_tasks.append(task)
                minutes_used += task.duration_minutes
            else:
                self.overflow_tasks.append(task)

    def show_schedule(self):
        """Return a formatted string of today's scheduled tasks sorted by time, with overflow and conflicts."""
        self.sort_scheduled_by_time()
        header = f"--- Today's Schedule for {self.owner.owner_name} and {self.pet.pet_name} ---\n"
        tasks = [task.display_task() for task in self.scheduled_tasks]
        result = header + "\n\n".join(tasks)

        if self.overflow_tasks:
            result += "\n\n--- Could Not Fit (Overflow) ---\n"
            result += "\n".join(
                f"  - {t.task_name} ({t.duration_minutes} min, {t.priority.name})"
                for t in self.overflow_tasks
            )

        conflicts = self.check_conflicts()
        if conflicts:
            result += "\n\n--- Time Conflicts Detected ---\n"
            for task_a, task_b in conflicts:
                result += f"  - '{task_a.task_name}' and '{task_b.task_name}' overlap\n"

        return result
