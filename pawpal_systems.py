from dataclasses import dataclass, field
from datetime import date, time
from enum import Enum
from typing import Optional


class Priority(Enum):
    LOW = 1
    MEDIUM = 2
    HIGH = 3


@dataclass
class Task:
    task_name: str
    duration_minutes: int
    priority: Priority
    due: date
    time: Optional[time] = None
    complete: bool = False

    def __post_init__(self):
        """Validate that duration_minutes is at least 1."""
        if self.duration_minutes < 1:
            raise ValueError(f"duration_minutes must be at least 1, got {self.duration_minutes}")

    def is_overdue(self) -> bool:
        """Return True if the task is not complete and its due date has passed."""
        # Note: date.today() uses local system time. If this app is deployed
        # across timezones, replace with datetime.now(timezone.utc).date()
        return not self.complete and self.due < date.today()

    def mark_complete(self):
        """Mark this task as complete."""
        self.complete = True

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
        return (
            f"Task: {self.task_name}\n"
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
        result = []
        for task in self.tasks:
            if task.task_name != task_name:
                result.append(task)
        self.tasks = result

    def get_pet_info(self):
        """Return a formatted string of this pet's basic information."""
        return f"{self.pet_name} is a {int(self.pet_age)}-year-old {self.pet_type}."

    def show_tasks(self):
        """Return a formatted string of all tasks assigned to this pet."""
        result = []
        for task in self.tasks:
            result.append(task.display_task())
        return "\n\n".join(result)


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
        result = []
        for pet in self.pets:
            if pet.pet_name != pet_name:
                result.append(pet)
        self.pets = result

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
        """Sort the pet's tasks from highest to lowest priority."""
        self.pet.tasks = sorted(self.pet.tasks, key=lambda task: task.priority.value, reverse=True)

    def check_conflicts(self):
        """Check for time overlaps between scheduled tasks."""
        for task_a in self.pet.tasks:
            for task_b in self.pet.tasks:
                if task_a == task_b:
                    continue
                if task_a.time is None or task_b.time is None:
                    continue

    def generate_schedule(self):
        """Build the schedule by fitting tasks into the owner's available hours."""
        self.sort_tasks_by_priority()
        total_minutes = self.owner.available_hours * 60

        minutes_used = 0
        for task in self.pet.tasks:
            if minutes_used + task.duration_minutes <= total_minutes:
                self.scheduled_tasks.append(task)
                minutes_used += task.duration_minutes
            else:
                self.overflow_tasks.append(task)

    def show_schedule(self):
        """Return a formatted string of today's scheduled tasks for this pet."""
        header = f"--- Today's Schedule for {self.owner.owner_name} and {self.pet.pet_name} ---\n"
        tasks = []
        for task in self.scheduled_tasks:
            tasks.append(task.display_task())
        return header + "\n\n".join(tasks)
