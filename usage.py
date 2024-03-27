import psutil  # Importing psutil for accessing system details and process information
import datetime  # Importing datetime for handling time-related operations
import argparse  # Importing argparse for parsing command-line arguments

def get_usage_stats(start_time, end_time):
    """
    Gathers CPU and memory usage statistics for processes that started within a specified time range.

    Parameters:
    - start_time (datetime): The start of the time range.
    - end_time (datetime): The end of the time range.

    Returns:
    - Tuple[Dict, Dict]: Two dictionaries containing CPU and memory usage percentages keyed by process name.
    """
    processes = psutil.process_iter()  # Getting an iterator for all current processes
    
    # Initialize dictionaries to store usage statistics
    cpu_usage = {}
    mem_usage = {}

    # Iterate through each process to gather necessary information
    for proc in processes:
        try:
            # Fetching process details as a dictionary
            proc_info = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_percent'])
            
            # Convert process start time to datetime object for comparison
            proc_start_time = datetime.datetime.fromtimestamp(proc.create_time())
            # Check if the process started within the specified time range
            if start_time <= proc_start_time <= end_time:
                # If so, store the CPU and memory usage statistics keyed by process name
                # Ensure unique entries by appending process ID to process name
                unique_proc_name = f"{proc_info['name']}_{proc_info['pid']}"
                cpu_usage[unique_proc_name] = proc_info['cpu_percent']
                mem_usage[unique_proc_name] = proc_info['memory_percent']
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            # If the process has terminated or cannot be accessed before its information could be accessed, ignore it
            pass

    return cpu_usage, mem_usage  # Return the gathered statistics

if __name__ == "__main__":
    # Setting up command-line argument parsing
    parser = argparse.ArgumentParser(description="Get MacBook Pro usage statistics for a specified time.")
    parser.add_argument("--start", help="Start time in 'YYYY-MM-DD HH:MM:SS' format", required=True)
    parser.add_argument("--end", help="End time in 'YYYY-MM-DD HH:MM:SS' format", required=True)
    args = parser.parse_args()

    try:
        # Parse the start and end time from the provided arguments
        start_time = datetime.datetime.strptime(args.start, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(args.end, "%Y-%m-%d %H:%M:%S")

        # Retrieve usage statistics for the specified time range
        cpu_usage, mem_usage = get_usage_stats(start_time, end_time)
        print("CPU Usage:", cpu_usage)
        print("Memory Usage:", mem_usage)

        # Check if the dictionaries are not empty before displaying the results
        if cpu_usage and mem_usage:
            print("CPU Usage:")
            for process, usage in cpu_usage.items():
                print(f"{process}: {usage}%")

            print("\nMemory Usage:")
            for process, usage in mem_usage.items():
                print(f"{process}: {usage}%")
        else:
            print("No processes found within the specified time range.")
    except ValueError:
        # Handle incorrect datetime format provided by the user
        print("Invalid datetime format. Please use 'YYYY-MM-DD HH:MM:SS'.")

