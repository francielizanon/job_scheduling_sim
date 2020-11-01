"""
Script that replays the jobs from the ANL-Intrepid-2009-1.swf.gz dataset.

It uses a different scheduling algorithm and a simplified,
configurable-sized system.
"""

import sys
from simulator.engine import Engine


def usage_and_out(argv):
    """Writes a messages with the expected inputs."""
    print(f'Usage: python {argv[0]} scheduling_algorithm number_of_nodes' +
          ' number_of_jobs (optional)')
    exit()


# Debug flag: set to True if you want to see all messages during simulation
debug = False

# Gets the input parameters
if len(sys.argv) < 3:
    usage_and_out(sys.argv)
algorithm = sys.argv[1]
nodes_nb = int(sys.argv[2])
if debug:
    print(f'DEBUG: running the simulation using the {algorithm}' +
          f' scheduler for a machine of {nodes_nb} nodes.')

if len(sys.argv) == 4:
    task_limit = int(sys.argv[3])
    if debug:
        print(f'DEBUG: the simulation will only consider the' +
              f' first {task_limit} jobs in the input file.')
else:
    task_limit = -1

# Creates the simulation engine
simulator = Engine(algorithm, nodes_nb, task_limit, debug=debug)
# Starts the simulation
simulator.run()
