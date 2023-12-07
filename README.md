# Track-CLI
Track-CLI is a command-line interface (CLI) tool designed to help professionals track and calibrate their productivity. Inspired by Git's command-line syntax, Track-CLI offers an intuitive way to log tasks, evaluate performance, and visualize productivity trends over time.

## Features
- Task Logging: Easily log tasks with predicted completion times and other custom metrics.
- Evaluation: Update tasks upon completion with actual outcomes, allowing for performance assessment and calibration.
- Project Flexibility: Separate tracking for different projects like work, personal tasks, etc.
- Data Visualization: Built-in methods for generating calibration plots and time series analyses.
- Data Export: Export task data in various formats (CSV, JSON, etc.) for further analysis.

## Installation
To install Track-CLI, clone this repository and run the following command in the root directory:

```bash
pip install .
```
This will install track-cli and its dependencies on your system.

## Usage
Here are some common commands used in Track-CLI:

Initialize a Project:
```bash
track init [project-name]
```

Add a Task:
```bash
track add "Task Description" --project [project-name] --time [time-estimate] --[other-parameters]
```

Tracked metrics are highly flexible; you can work with whatever fields you'd like by simply specifying named arguments, allowing for different use cases: 
```bash
track add "Emily will win survivor" --project [project-name] --probability 0.35
```

Evaluate a Task:
```bash
track eval [task-id] --project [project-name] --time [actual-time] --[other-updates]
```
Note that task-id will default to the most recent task if not specified.

List Tasks:
```bash
track list --project [project-name]
```

Switch Project:
```bash
track switch [project-name]
```
Visualize Data:
```bash
track plot --project [project-name] --type [plot-type]
```

Export Data:
```bash
track export --project [project-name] --format [format] --file [filename]
```

Replace `[project-name]`, `[task-id]`, `[time-estimate]`, `[actual-time]`, `[other-parameters]`, `[other-updates]`, `[plot-type]`, `[format]`, and `[filename]` with your actual project names, task IDs, time estimates, etc.

## Contributing
Contributions to Track-CLI are welcome! Please refer to the contribution guidelines for more information.

## License
This project is licensed under the MIT License.