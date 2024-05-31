import subprocess
import time
import sys
import os
import uuid

script_to_run = "run_simulator.py"
assignment_script = "assignment.py"
config_file = "games/two_colours_assignment.yaml"

# Check if the number of tests is provided as a command-line argument
if len(sys.argv) != 2:
    print("Usage: python3 run_tests.py <number_of_tests>")
    sys.exit(1)

try:
    num_tests = int(sys.argv[1])
except ValueError:
    print("Number of tests must be an integer.")
    sys.exit(1)

# Create a directory named "logs" if it doesn't exist
log_directory = "logs"
if not os.path.exists(log_directory):
    os.makedirs(log_directory)
filename = os.path.join(log_directory, f"execution_log_{uuid.uuid4()}.txt")

# Open a file for logging
for i in range(num_tests):
    start_time = time.time()
    execution_times = []

    try:
        # Run the simulator script using subprocess with a timeout
        result = subprocess.run(
            ["python3", script_to_run, "-c", config_file, assignment_script],
            capture_output=True,
            text=True,
            timeout= 240 # Set a timeout of 240 seconds (4 mins) or adjust as needed
        )
        end_time = time.time()
        execution_time = end_time - start_time
        execution_times.append(execution_time)
    except subprocess.TimeoutExpired:
        end_time = time.time()
        execution_time = end_time - start_time
        execution_times.append(f"Timeout after {execution_time:.2f} seconds")
    except Exception as e:
        end_time = time.time()
        execution_time = end_time - start_time
        execution_times.append(f"Exception after {execution_time:.2f} seconds: {str(e)}")

    # Generate a unique filename using UUID
    with open(filename, "a") as log_file:
        # After the loop is finished, log all execution times
        for time_info in execution_times:
            log_file.write(f"{time_info}\n")

print(f"Execution times have been logged to '{filename}'.")
