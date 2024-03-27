import psutil
import datetime
import argparse

def get_usage_stats(start_time, end_time):
    processes = psutil.process_iter()
    
    # Initialize dictionaries to store usage statistics
    cpu_usage = {}
    mem_usage = {}

    # Iterate through each process
    for proc in processes:
        try:
            # Get process information
            proc_info = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_percent'])
            
            # Check if the process started between the specified time range
            proc_start_time = datetime.datetime.fromtimestamp(proc.create_time())
            if start_time <= proc_start_time <= end_time:
                # Store CPU and memory usage statistics for the process
                cpu_usage[proc_info['name']] = proc_info['cpu_percent']
                mem_usage[proc_info['name']] = proc_info['memory_percent']
        except psutil.NoSuchProcess:
            # Process might have terminated between the iteration, ignore
            pass

    return cpu_usage, mem_usage

if __name__ == "__main__":
    processes = psutil.process_iter()
    for proc in processes:
        try:
            proc_info = proc.as_dict(attrs=['pid', 'name', 'cpu_percent', 'memory_percent'])
            print(proc_info)
        except psutil.NoSuchProcess:
            pass
    exit()
    parser = argparse.ArgumentParser(description="Get MacBook Pro usage statistics for a specified time.")
    parser.add_argument("--start", help="Start time in 'YYYY-MM-DD HH:MM:SS' format", required=True)
    parser.add_argument("--end", help="End time in 'YYYY-MM-DD HH:MM:SS' format", required=True)
    args = parser.parse_args()

    try:
        # Parse start and end time arguments
        start_time = datetime.datetime.strptime(args.start, "%Y-%m-%d %H:%M:%S")
        end_time = datetime.datetime.strptime(args.end, "%Y-%m-%d %H:%M:%S")

        # Get usage statistics
        cpu_usage, mem_usage = get_usage_stats(start_time, end_time)

        # Print the results
        print("CPU Usage:")
        for process, usage in cpu_usage.items():
            print(f"{process}: {usage}%")

        print("\nMemory Usage:")
        for process, usage in mem_usage.items():
            print(f"{process}: {usage}%")
    except ValueError:
        print("Invalid datetime format. Please use 'YYYY-MM-DD HH:MM:SS'.")

