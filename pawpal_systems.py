from dataclasses import dataclass, field


@dataclass
class Task:
    task_name: str
    duration: int
    priority: str
    time: str
    due: str
    complete: bool = False

    def mark_complete(self):
        pass

    def edit_time(self, new_time):
        pass

    def edit_priority(self, new_priority):
        pass

    def display_task(self):
        pass


@dataclass
class Pet:
    pet_name: str
    pet_type: str
    pet_age: int
    tasks: list = field(default_factory=list)

    def add_task(self, task):
        pass

    def rmv_task(self, task_name):
        pass

    def get_pet_info(self):
        pass

    def show_tasks(self):
        pass


class Owner:
    def __init__(self, owner_name, available_hours):
        self.owner_name = owner_name
        self.available_hours = available_hours

    def get_owner_info(self):
        pass


class Schedule:
    def __init__(self, owner, pet):
        self.owner = owner
        self.pet = pet
        self.scheduled_tasks = []

    def sort_tasks_by_priority(self, tasks):
        pass

    def check_conflicts(self, tasks):
        pass

    def generate_schedule(self):
        pass

    def show_schedule(self):
        pass
