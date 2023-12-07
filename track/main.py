import argparse
import json

from .commands import get_config, check_first_time_setup, handle_init, handle_add, handle_eval, handle_list, handle_switch, handle_export

def main():
    check_first_time_setup()

    parser = argparse.ArgumentParser(prog="track", description="Track and calibrate your productivity.")
    subparsers = parser.add_subparsers(dest="command")

    # Initialize a new project
    parser_init = subparsers.add_parser("init", help="Initialize a new project.")
    parser_init.add_argument("project", type=str, help="Name of the project to initialize.")

    # Add a new task
    parser_add = subparsers.add_parser("add", help="Add a new task.")
    parser_add.add_argument("task_description", type=str, help="Description of the task.")
    # Add more arguments for time, difficulty, etc.

    # Update a task with results
    parser_eval = subparsers.add_parser("eval", help="Evaluate and update a task.")
    parser_eval.add_argument("--task_id", type=int, help="ID of the task to update.")
    parser_eval.add_argument("--project", help="Name of the project to update the task in.")

    # Switch between projects
    parser_switch = subparsers.add_parser("switch", help="Switch between projects.")
    parser_switch.add_argument("project", type=str, help="Name of the project to switch to.")

    # List IDs of tasks in a project
    parser_list = subparsers.add_parser("list", help="List tasks in a project.")
    parser_list.add_argument("--project", help="Name of the project to list tasks from.")

    # Switch to a new project
    parser_switch = subparsers.add_parser("switch", help="Switch between projects.")
    parser_switch.add_argument("project", type=str, help="Name of the project to switch to.")

    # Visualize data
    parser_plot = subparsers.add_parser("plot", help="Visualize data.")
    # Add arguments for types of plots

    # Export data
    parser_export = subparsers.add_parser("export", help="Export data from a project.")
    parser_export.add_argument("file", help="Name of the file to export data to.")
    parser_export.add_argument("--project", help="Name of the project to export data from.")
    parser_export.add_argument("--format", choices=["csv", "json", "feather"], default="csv", help="Format to export data in.")
    

    args, unknown_args = parser.parse_known_args()
    config = get_config()
    track_cli_dir = config["track_cli_dir"]

    # If project is not specified, use the current project
    if not hasattr(args, "project") or hasattr(args, "project") and args.project is None:
        with open(f"{track_cli_dir}/config.json", "r") as file:
            args.project = json.load(file)["current_project"]

    # Mapping commands to their respective functions
    if args.command == "init":
        handle_init(args.project)

    elif args.command == "add":
        kwargs = {unknown_args[i].lstrip('--'): unknown_args[i + 1] for i in range(0, len(unknown_args), 2)}
        handle_add(args.task_description, args.project, **kwargs)

    elif args.command == "eval":
        kwargs = {unknown_args[i].lstrip('--'): unknown_args[i + 1] for i in range(0, len(unknown_args), 2)}

        # If task_id is not specified, use the last task
        if not hasattr(args, "task_id") or hasattr(args, "task_id") and args.task_id is None:
            task_dir = f"{track_cli_dir}/{args.project}"
            with open(f"{task_dir}/tasks.json", "r") as file:
                tasks = json.load(file)
                if len(tasks) == 0:
                    print(f"No tasks found for project '{args.project}'.")
                    return
                args.task_id = tasks[-1]["task_id"]

        handle_eval(args.task_id, args.project, **kwargs)

    elif args.command == "list":
        handle_list(args.project)

    elif args.command == "switch":
        handle_switch(args.project)

    elif args.command == "plot":
        print("Not yet implemented :(")

    elif args.command == "export":
        handle_export(args.project, args.format, args.file)


if __name__ == "__main__":
    main()
