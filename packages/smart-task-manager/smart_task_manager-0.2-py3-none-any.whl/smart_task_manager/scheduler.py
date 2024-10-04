# smart_task_manager/scheduler.py
from datetime import datetime, timedelta

class Scheduler:
    def __init__(self):
        self.schedule = {}

    def add_to_schedule(self, task, deadline):
        self.schedule[task] = deadline
        print(f"Scheduled '{task}' for {deadline}.")

    def get_schedule(self):
        return self.schedule
