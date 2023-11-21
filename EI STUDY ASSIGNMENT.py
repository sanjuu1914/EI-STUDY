#!/usr/bin/env python
# coding: utf-8

# In[8]:


from abc import ABC, abstractmethod

# Observer Pattern
class Observer(ABC):
    @abstractmethod
    def update(self):
        pass

class Observable(ABC):
    def __init__(self):
        self.observers = []

    def add_observer(self, observer):
        self.observers.append(observer)

    def remove_observer(self, observer):
        self.observers.remove(observer)

    def notify_observers(self):
        for observer in self.observers:
            observer.update()

# Factory Method Pattern
class DeviceFactory(ABC):
    @abstractmethod
    def create_device(self, device_info):
        pass

class LightFactory(DeviceFactory):
    def create_device(self, device_info):
        light = Light(device_info['id'], device_info['status'])
        light.add_observer(light)  # Each device observes itself
        return light

class ThermostatFactory(DeviceFactory):
    def create_device(self, device_info):
        thermostat = Thermostat(device_info['id'], device_info['temperature'])
        thermostat.add_observer(thermostat)  # Each device observes itself
        return thermostat

class DoorLockFactory(DeviceFactory):
    def create_device(self, device_info):
        door_lock = DoorLock(device_info['id'], device_info['status'])
        door_lock.add_observer(door_lock)  # Each device observes itself
        return door_lock

# Proxy Pattern
class DeviceProxy:
    def __init__(self, device):
        self.device = device

    def __getattr__(self, name):
        if name == 'status':
            if hasattr(self.device, 'is_on'):
                return "On" if self.device.is_on() else "Off"
            else:
                return "Status not available"
        return getattr(self.device, name)

    def turn_on(self):
        print(f"Turning on {self.device.get_type()} {self.device.get_id()}")
        self.device.turn_on()

    def turn_off(self):
        print(f"Turning off {self.device.get_type()} {self.device.get_id()}")
        self.device.turn_off()

# Concrete Devices
class Light(Observer, Observable):
    def __init__(self, device_id, status):
        super().__init__()  # Ensure Observable is properly initialized
        self.device_id = device_id
        self._status = status

    def turn_on(self):
        self._status = "On"
        self.notify_observers()

    def turn_off(self):
        self._status = "Off"
        self.notify_observers()

    def is_on(self):
        return self._status == "On"

    def get_id(self):
        return self.device_id

    def get_type(self):
        return "Light"

    def update(self):
        print(f"Light {self.device_id} is {self._status}.")

class Thermostat(Observer, Observable):
    def __init__(self, device_id, temperature):
        super().__init__()  # Ensure Observable is properly initialized
        self.device_id = device_id
        self.temperature = temperature

    def set_temperature(self, temperature):
        self.temperature = temperature
        self.notify_observers()

    def get_id(self):
        return self.device_id

    def get_type(self):
        return "Thermostat"

    def update(self):
        print(f"{self.get_type()} is set to {self.temperature} degrees.")

class DoorLock(Observer, Observable):
    def __init__(self, device_id, status):
        super().__init__()  # Ensure Observable is properly initialized
        self.device_id = device_id
        self._status = status

    def lock(self):
        self._status = "Locked"
        self.notify_observers()

    def unlock(self):
        self._status = "Unlocked"
        self.notify_observers()

    def is_locked(self):
        return self._status == "Locked"

    def get_id(self):
        return self.device_id

    def get_type(self):
        return "Door Lock"

    def update(self):
        print(f"{self.get_type()} is {self._status}.")

# Smart Home System Hub
class SmartHomeSystem:
    def __init__(self):
        self.devices = []
        self.scheduled_tasks = []
        self.automated_triggers = []

    def add_device(self, device):
        self.devices.append(device)

    def remove_device(self, device):
        self.devices.remove(device)

    def get_status_report(self):
        status_report = []
        for device in self.devices:
            status_report.append(f"{device.get_type()} {device.get_id()} is {DeviceProxy(device).status}.")
        return " ".join(status_report)

    def get_scheduled_tasks(self):
        return self.scheduled_tasks

    def get_automated_triggers(self):
        return self.automated_triggers

    def add_scheduled_task(self, device_id, time, command):
        self.scheduled_tasks.append({"device": device_id, "time": time, "command": command})

    def add_automated_trigger(self, condition, action):
        self.automated_triggers.append({"condition": condition, "action": action})

    def execute_command(self, command):
        parts = command.split('(')
        device_id = int(parts[1].split(')')[0])
        method_name = parts[0]
        device = self.get_device_by_id(device_id)

        if device:
            if hasattr(device, method_name):
                method = getattr(device, method_name)
                method()
            else:
                print(f"Error: Device {device_id} does not have method {method_name}.")
        else:
            print(f"Error: Device {device_id} not found.")

    def get_device_by_id(self, device_id):
        for device in self.devices:
            if device.get_id() == device_id:
                return device
        return None

# Example Usage
if __name__ == "__main__":
    # Initialize Smart Home System
    smart_home = SmartHomeSystem()

    # Create Devices using Factory Method
    light_factory = LightFactory()
    thermostat_factory = ThermostatFactory()
    door_lock_factory = DoorLockFactory()

    light = light_factory.create_device({'id': 1, 'status': 'off'})
    thermostat = thermostat_factory.create_device({'id': 2, 'temperature': 70})
    door_lock = door_lock_factory.create_device({'id': 3, 'status': 'locked'})

    # Add Devices to Smart Home System
    smart_home.add_device(light)
    smart_home.add_device(thermostat)
    smart_home.add_device(door_lock)

    # Proxy Pattern
    light_proxy = DeviceProxy(light)
    thermostat_proxy = DeviceProxy(thermostat)
    door_lock_proxy = DeviceProxy(door_lock)

    # Demonstrate Proxy Pattern
    print(light_proxy.status)  # Outputs "Off"
    light_proxy.turn_on()      # Outputs "Turning on Light 1"
    print(light_proxy.status)  # Outputs "On"

    # Demonstrate Observer Pattern
    thermostat.set_temperature(75)
    door_lock.unlock()

    # Demonstrate Smart Home System
    smart_home.execute_command('turnOn(1)')
    smart_home.add_scheduled_task(2, "06:00", "turnOn")
    smart_home.add_automated_trigger("temperature > 75", "turnOff(1)")

    print("Status Report:", smart_home.get_status_report())
    print("Scheduled Tasks:", smart_home.get_scheduled_tasks())
    print("Automated Triggers:", smart_home.get_automated_triggers())


# In[10]:


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
        due_date_str = f" Due: {self.due_date.strftime('%Y-%m-%d')} " if self.due_date else ""
        return f"{self.description} - {status} {due_date_str}"


class TaskManager:
    def __init__(self):
        self.tasks = []
        self.undo_stack = []

    def add_task(self, description, due_date=None):
        new_task = Task(description, due_date)
        self.tasks.append(new_task)
        self.save_state()

    def mark_completed(self, task_description):
        for task in self.tasks:
            if task.description == task_description:
                task.mark_completed()
                self.save_state()
                break

    def undo_mark_completed(self, task_description):
        for task in self.tasks:
            if task.description == task_description:
                task.undo_completed()
                self.save_state()
                break

    def delete_task(self, task_description):
        for task in self.tasks:
            if task.description == task_description:
                self.tasks.remove(task)
                self.save_state()
                break

    def view_tasks(self, filter_by=None):
        filtered_tasks = self.tasks
        if filter_by == "completed":
            filtered_tasks = [task for task in self.tasks if task.completed]
        elif filter_by == "pending":
            filtered_tasks = [task for task in self.tasks if not task.completed]

        for task in filtered_tasks:
            print(task)

    def save_state(self):
        current_state = {"tasks": self.tasks.copy()}
        self.undo_stack.append(current_state)
        if len(self.undo_stack) > 10:
            self.undo_stack.pop(0)

    def undo(self):
        if len(self.undo_stack) > 0:
            previous_state = self.undo_stack.pop()
            self.tasks = previous_state["tasks"]

task_manager = TaskManager()

task_manager.add_task("Buy groceries", datetime.date(2023, 9, 20))
task_manager.add_task("Finish project report")
task_manager.mark_completed("Buy groceries")
task_manager.view_tasks("all")
task_manager.undo_mark_completed("Buy groceries")
task_manager.view_tasks("all")
task_manager.delete_task("Finish project report")
task_manager.view_tasks("pending")


# In[13]:


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


# In[ ]:





# In[ ]:




