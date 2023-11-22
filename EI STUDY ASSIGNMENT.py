import datetime

class Task:
    def __init__(self, description, due_date=None):
        self.description = description
        self.due_date = due_date
        self.completed = False

    def mark_completed(self):
        self.completed = True

    def undo_completed(self):
        self.completed = False

    def __str__(self):
        status = "Completed" if self.completed else "Pending"
        due_date_str = f"(Due: {self.due_date.strftime('%Y-%m-%d')})" if self.due_date else ""
        return f"{self.description} - {status} {due_date_str}"

class TaskManager:
    def __init__(self):
        self.tasks = []
        self.undo_stack = []

    def add_task(self):
        description = input("Enter task description: ")
        due_date_str = input("Enter due date (optional, format YYYY-MM-DD): ")
        due_date = None if not due_date_str else datetime.datetime.strptime(due_date_str, "%Y-%m-%d")
        new_task = Task(description, due_date)
        self.tasks.append(new_task)
        self.save_state()

    def mark_completed(self):
        task_description = input("Enter task description to mark as completed: ")
        for task in self.tasks:
            if task.description == task_description:
                task.mark_completed()
                self.save_state()
                break

    def undo_mark_completed(self):
        task_description = input("Enter task description to undo completion: ")
        for task in self.tasks:
            if task.description == task_description:
                task.undo_completed()
                self.save_state()
                break

    def delete_task(self):
        task_description = input("Enter task description to delete: ")
        for task in self.tasks:
            if task.description == task_description:
                self.tasks.remove(task)
                self.save_state()
                break

    def view_tasks(self):
        filter_by = input("Filter tasks (all, completed, pending): ")
        filtered_tasks = self.tasks
        if filter_by == "completed":
            filtered_tasks = [task for task in self.tasks if task.completed]
        elif filter_by == "pending":
            filtered_tasks = [task for task in self.tasks if not task.completed]

        for task in filtered_tasks:
            print(task)

    def save_state(self):
        current_state = {"tasks": [task.__dict__ for task in self.tasks]}
        self.undo_stack.append(current_state)
        if len(self.undo_stack) > 10:
            self.undo_stack.pop(0)

    def undo(self):
        if len(self.undo_stack) > 0:
            previous_state = self.undo_stack.pop()
            self.tasks = [Task(**task_dict) for task_dict in previous_state["tasks"]]

# Example usage
if __name__ == "__main__":
    task_manager = TaskManager()

    while True:
        print("\nTask Manager Menu:")
        print("1. Add Task")
        print("2. Mark Task as Completed")
        print("3. Undo Completed Task")
        print("4. Delete Task")
        print("5. View Tasks")
        print("6. Undo Last Operation")
        print("0. Exit")

        choice = input("Enter your choice: ")

        if choice == "1":
            task_manager.add_task()
        elif choice == "2":
            task_manager.mark_completed()
        elif choice == "3":
            task_manager.undo_mark_completed()
        elif choice == "4":
            task_manager.delete_task()
        elif choice == "5":
            task_manager.view_tasks()
        elif choice == "6":
            task_manager.undo()
        elif choice == "0":
            break
        else:
            print("Invalid choice. Please enter a valid option.")
