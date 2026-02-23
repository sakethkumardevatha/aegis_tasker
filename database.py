import json
import os

DB_FILE = "roadmap.json"

def load_data():
    if not os.path.exists(DB_FILE):
        return {}
    try:
        with open(DB_FILE, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return {}

def save_data(data):
    with open(DB_FILE, "w") as f:
        json.dump(data, f, indent=4)

def update_task_status(day_id, task_index, new_status):
    data = load_data()
    if day_id in data:
        tasks = data[day_id].get("tasks", [])
        if 0 <= task_index < len(tasks):
            tasks[task_index]["status"] = new_status
            save_data(data)
            return True
    return False

# --- This is the function the error is looking for ---
def delete_task(day_id, task_index):
    """Removes a task from the list and persists the change to JSON."""
    data = load_data()
    if day_id in data:
        tasks = data[day_id].get("tasks", [])
        if 0 <= task_index < len(tasks):
            # pop() removes the item at the specific index
            tasks.pop(task_index)
            save_data(data)
            return True
    return False
def update_task_details(day_id, task_index, new_topic, new_action):
    """Modifies the description and action of an existing task."""
    data = load_data()
    if day_id in data:
        tasks = data[day_id].get("tasks", [])
        if 0 <= task_index < len(tasks):
            tasks[task_index]["topic"] = new_topic
            tasks[task_index]["action"] = new_action
            save_data(data)
            return True
    return False