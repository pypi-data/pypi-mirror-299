# smart_task_manager/__init__.py
from .task_manager import TaskManager
from .scheduler import Scheduler
from .analytics import Analytics

__all__ = ['TaskManager', 'Scheduler', 'Analytics']
