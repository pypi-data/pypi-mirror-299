# tests/test_task_manager.py
import unittest
from smart_task_manager import TaskManager

class TestTaskManager(unittest.TestCase):
    def setUp(self):
        self.manager = TaskManager()

    def test_add_task(self):
        self.manager.add_task("Task 1")
        self.assertIn("Task 1", self.manager.tasks)

    def test_remove_task(self):
        self.manager.add_task("Task 2")
        self.manager.remove_task("Task 2")
        self.assertNotIn("Task 2", self.manager.tasks)

    def test_list_tasks(self):
        self.manager.add_task("Task 3")
        self.assertEqual(self.manager.list_tasks(), ["Task 3"])

if __name__ == '__main__':
    unittest.main()
