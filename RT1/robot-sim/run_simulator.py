import yaml
import threading
import argparse
import sys
import time
import signal
import os

sys.path.append("sr/robot")
sys.path.append("sr/robot/arenas")

from sr.robot import *

# Global variable to hold the simulator instance
sim = None
threads = []

def shutdown_simulator(signal_received=None, frame=None):
    """Shutdown the simulator and join all threads."""
    global sim, threads
    print("Shutting down the simulator...")
    if sim:
        sim.running = False  # Assuming setting running to False will stop the simulator
    for thread in threads:
        thread.join()
    sys.exit(0)

def main():
    global sim, threads

    parser = argparse.ArgumentParser()
    parser.add_argument('-c', '--config',
                        type=argparse.FileType('r'),
                        default='games/two_colours_assignment.yaml')
    parser.add_argument('robot_scripts',
                        type=argparse.FileType('r'),
                        nargs='*')
    args = parser.parse_args()

    def read_file(fn):
        with open(fn, 'r') as f:
            return f.read()

    robot_scripts = args.robot_scripts
    prompt = "Enter the names of the Python files to run, separated by commas: "
    while not robot_scripts:
        robot_script_names = input(prompt).split(',')
        if robot_script_names == ['']: continue
        robot_scripts = [read_file(s.strip()) for s in robot_script_names]

    with args.config as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    sim = Simulator(config, background=False)

    class RobotThread(threading.Thread):
        def __init__(self, zone, script_content, *args, **kwargs):
            super(RobotThread, self).__init__(*args, **kwargs)
            self.zone = zone
            self.script_content = script_content
            self.daemon = True

        def run(self):
            def robot():
                with sim.arena.physics_lock:
                    robot_object = SimRobot(sim)
                    robot_object.zone = self.zone
                    robot_object.location = sim.arena.start_locations[self.zone]
                    robot_object.heading = sim.arena.start_headings[self.zone]
                    return robot_object
            try:
                exec(self.script_content, {'Robot': robot})
            except Exception as e:
                print(f"Exception in RobotThread (zone {self.zone}): {e}")

    threads = []
    for zone, robot_script in enumerate(robot_scripts):
        thread = RobotThread(zone, robot_script.read())
        thread.start()
        threads.append(thread)

    # Register signal handlers for termination
    signal.signal(signal.SIGINT, shutdown_simulator)
    signal.signal(signal.SIGTERM, shutdown_simulator)

    # Create PID file early in the script
    with open('run_pid.txt', 'w') as f:
        f.write(str(os.getpid()))

    try:
        sim.run()  # Main simulator run loop
    except KeyboardInterrupt:
        print("Received KeyboardInterrupt, shutting down.")
    except Exception as e:
        print(f"Received termination signal or unexpected exception: {e}")
    finally:
        shutdown_simulator()

if __name__ == "__main__":
    main()
