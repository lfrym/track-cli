from datetime import datetime
import json
import os

import pandas as pd
from prettytable import PrettyTable

def get_config():
    # Set the default path for the config file
    home_dir = os.path.expanduser("~")
    default_config_dir = os.path.join(home_dir, '.track-cli')
    default_config_path = os.path.join(default_config_dir, 'track-cli-config.json')

    # Create the .track-cli directory if it doesn't exist
    os.makedirs(default_config_dir, exist_ok=True)

    # Check if the config file exists, if not, create one with default settings
    if not os.path.isfile(default_config_path):
        default_config = {
            # default settings
            "track_cli_dir": default_config_dir
        }
        with open(default_config_path, 'w') as f:
            json.dump(default_config, f, indent=4)
    
    # Read and return the configuration
    with open(default_config_path, 'r') as f:
        config = json.load(f)
    
    return config



def check_first_time_setup():
    track_cli_dir = get_config()["track_cli_dir"]
    if not os.path.exists(track_cli_dir):
        os.makedirs(track_cli_dir)
        print(f"Initialized track-cli storage at {track_cli_dir}")


def handle_init(project: str, overwrite: bool = False):
    track_cli_dir = get_config()["track_cli_dir"]
    os.makedirs(f"{track_cli_dir}/{project}", exist_ok=True)

    # Create or update the config file to set the current project
    with open(f"{track_cli_dir}/config.json", "w") as file:
        json.dump({"current_project": project}, file, indent=4)
    
    # Initialize a tasks file
    # with open(f"{track_cli_dir}/{project}/tasks.json", "w") as file:
    #     # If file exists
    #     if not overwrite:
    #         if os.path.exists(f"{track_cli_dir}/{project}/tasks.json"):
    #             FileExistsError("Tasks file already exists. Use --overwrite to overwrite it.")
    #             return
    #     json.dump([], file, indent=4)
    

    print(f"Project '{project}' initialized.")


def handle_add(task_description: str, project: str, **kwargs):
    track_cli_dir = get_config()["track_cli_dir"]
    task_data = {"description": task_description, **kwargs}
    json_file_path = f"{track_cli_dir}/{project}/tasks.json"

    # Read existing data
    try:
        with open(json_file_path, "r") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        tasks = []
        next_id = 1
    else:
        next_id = max(task["task_id"] for task in tasks) + 1 if tasks else 1

    # Assign an ID to the new task
    task_data["task_id"] = next_id

    # Get a timestamp for the new task
    task_data["time_add"] = datetime.now().strftime("%Y-%m-%d--%H:%M")

    # Add new task
    tasks.append(task_data)

    # Write updated data
    with open(json_file_path, "w") as file:
        json.dump(tasks, file, indent=4)

    print(f"Task added to project '{project}': {task_data}")


def handle_eval(task_id: int, project: str, **kwargs):
    track_cli_dir = get_config()["track_cli_dir"]
    json_file_path = f"{track_cli_dir}/{project}/tasks.json"

    # Rename the keys in kwargs
    kwargs = {f"{key}_eval": value for key, value in kwargs.items()}

    try:
        with open(json_file_path, "r") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        print(f"No tasks found for project '{project}'.")
        return

    # Find the task with the given ID
    for task in tasks:
        if task["task_id"] == task_id:
            task.update(kwargs)
            break
    else:
        print(f"Task with ID {task_id} not found in project '{project}'.")
        return

    with open(json_file_path, "w") as file:
        json.dump(tasks, file, indent=4)

    print(f"Updated task in project '{project}': {task}")


def handle_list(project: str):
    track_cli_dir = get_config()["track_cli_dir"]
    json_file_path = f"{track_cli_dir}/{project}/tasks.json"

    try:
        with open(json_file_path, "r") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        print(f"No tasks found for project '{project}'.")
        return

    if not tasks:
        print(f"No tasks available in project '{project}'.")
        return

    table = PrettyTable()
    table.field_names = ["ID", "Resolved", "Description"]
    for task in tasks:
        resolved = "*" if any(key.endswith("_eval") and value for key, value in task.items()) else ""
        table.add_row([task["task_id"], resolved, task["description"]])
    
    print(table)


def handle_switch(project: str):
    track_cli_dir = get_config()["track_cli_dir"]
    config_file_path = f"{track_cli_dir}/config.json"
    config_data = {"current_project": project}

    with open(config_file_path, "w") as file:
        json.dump(config_data, file, indent=4)

    print(f"Switched to project '{project}'.")


def handle_export(project: str, file_format: str, file_name: str):
    track_cli_dir = get_config()["track_cli_dir"]
    json_file_path = f"{track_cli_dir}/{project}/tasks.json"

    try:
        with open(json_file_path, "r") as file:
            tasks = json.load(file)
    except FileNotFoundError:
        print(f"No tasks found for project '{project}'.")
        return

    df = pd.DataFrame(tasks)

    if file_format == "csv":
        df.to_csv(file_name, index=False)
        print(f"Data exported to {file_name}")

    elif file_format == "json":
        df.to_json(file_name, orient="records")
        print(f"Data exported to {file_name}")
    
    elif file_format == "feather":
        df.to_feather(file_name)
        print(f"Data exported to {file_name}")

    else:
        print(f"File format {file_format} not recognized.")