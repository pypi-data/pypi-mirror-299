from smart_task_manager.analytics import Analytics

# Create an instance of the Analytics class
analytics_instance = Analytics()

# Create a sample task
sample_task = analytics_instance.create_task("Sample Task", "This is a sample task description.")

# Print the created task
print("Created Task:", sample_task)

# Retrieve and print all tasks
all_tasks = analytics_instance.get_tasks()
print("All Tasks:", all_tasks)
