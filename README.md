# System Usage Python Script

This Python script is designed to monitor and report the CPU and memory usage of processes on a MacBook Pro within a specified time range. It utilizes the `psutil` library to gather process information and the `datetime` and `argparse` libraries for handling time and command-line arguments, respectively.

## Features

- **Process Monitoring:** Iterates through all processes running on the system to collect usage statistics.
- **Time Filtering:** Allows specifying a start and end time to filter processes that started within this time frame.
- **Usage Statistics:** Reports the CPU and memory usage percentages for filtered processes.

## Requirements

- Python 3.x
- `psutil` library

## Installation

1. Ensure Python 3.x is installed on your system.
2. Install the `psutil` library using pip:
