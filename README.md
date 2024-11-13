# Practical job scheduling activity

This repository is intended for use by students to practice concepts related to batch scheduling algorithms.
It contains a simple simulation engine that replicates the behavior of jobs arriving at different times to run on a cluster or supercomputer.
A set of activities using this repository is presented in the [activities section](#activities) below.

## How To

- The code in this repository is written using Python3 and a few of its modules.
In order to check and install any missing modules, run `python3 setup.py`.

- The activities require the `ANL-Intrepid-2009-1.swf` file obtained from the [ANL Intrepid Log](https://www.cse.huji.ac.il/labs/parallel/workload/l_anl_int/). 
In order to download the log, run `./prepare_input.sh`.

- To run a simulation, try `python3 replay.py fcfs 20000 10000`. `replay.py` takes parameters from the command line and feeds them to the simulation engine.

- To learn more about the code in the simulator, try using the `help` function in your Python3 interpreter. Example:

```python
>>> import simulator.job
>>> help(simulator.job)
```

- To check if the code you downloaded or changed is still working properly, try the following commands:

```bash
$ cd unitary_tests
$ ./test_fcfs.py
```

## About the traces and simulation

The ANL Intrepid trace contains information about 68,936 jobs submitted to the Intrepid supercomputer (Argonne National Laboratory, USA) over 240 days of 2009. At the time, the machine of 40,960 quad-core nodes was among the world's 10 fastest supercomputers (https://www.top500.org/lists/2009/06/).
About each job, the dataset contains (among other things) its submission time (when an user has
asked the system to run it), number of requested nodes, amount of requested time, and its actual execution
time. 

The [simulation engine](simulator/engine.py) uses this information to simulate the job scheduler operation: jobs are added to a
queue when submitted, and a scheduling algorithm is used to decide when to remove jobs from the queue to
run them.

At the end of the simulation, several statistics are reported. They related to the execution time of the jobs, their wait times (time spent in the queue by the jobs while waiting to be scheduled) and on the usage of the machine.

To run the simulation, use the following command:

```bash
$ python3 replay.py [scheduling algorithm] [number of nodes] [number of jobs]

```

## Activities

**Basic steps**

0. Run `replay.py` with the FCFS simulator with a few variations on the number of nodes and see how the reported metrics behave. Read [the code of the FCFS scheduler](simulator/algorithms.py) and try to understand how to write your own algorithms.

1. Write the First Fit (*ff*) scheduling algorithm. Check if it passes the tests in [the unitary tests file](unitary_tests/test_ff.py). Present its code. Compare it to the FCFS scheduler for the different metrics and different numbers of nodes. Does this algorithm provide improvements over FCFS? Explain your reasoning.

2. Write the Shortest-Job First (*sjf*) scheduling algorithm. Check if it passes the tests in [the unitary tests file](unitary_tests/test_sjf.py). Present its code. Compare it to the FF scheduler for the different metrics and different numbers of nodes. Does this algorithm provide improvements over FCFS and FF? Explain your reasoning.


**Additional challenge**

3. Write the FCFS with EASY backfilling (*fcfs\_easy*). Check if it passes the tests in [the unitary tests file](unitary_tests/test_fcfs_easy.py). Present your code. Compare it to the previous schedulers for the different metrics and different numbers of nodes. Does this algorithm provide any improvements? Explain your reasoning.

4. Write your own batch scheduling algorithm and compare it to the aforementioned algorithms.
