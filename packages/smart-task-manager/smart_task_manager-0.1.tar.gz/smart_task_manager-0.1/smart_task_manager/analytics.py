# smart_task_manager/analytics.py
class Analytics:
    def __init__(self):
        self.completed_tasks = 0
        self.total_tasks = 0

    def add_completed_task(self):
        self.completed_tasks += 1
        self.total_tasks += 1

    def add_task(self):
        self.total_tasks += 1

    def productivity_ratio(self):
        if self.total_tasks == 0:
            return 0
        return self.completed_tasks / self.total_tasks
