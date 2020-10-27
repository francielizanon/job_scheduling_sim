# job_scheduling_sim

This code was developed for educational purposes, it replays a trace from a supercomputer (containing information about job submissions) and allows for testing different scheduling algorithms. 

It requires the ANL-Intrepid-2009-1.swf file, obtained from the ANL Intrepid Log (https://www.cse.huji.ac.il/labs/parallel/workload/l_anl_int/). This trace contains information about 68,936 jobs
submitted to the Intrepid supercomputer (Argonne National Laboratory, USA) over 240 days of 2009. At the
2
time, the machine of 40,960 quad-core nodes was among the world's 10 fastest supercomputers
(https://www.top500.org/lists/2009/06/).

About each job, the dataset contains (among other things) its submission time (when an user has
asked the system to run it), number of requested nodes, amount of requested time, and its actual execution
time. The replay.py script uses this information to simulate the job scheduler operation: jobs are added to a
queue when submitted, and a scheduling algorithm is used to decide when to remove jobs from the queue to
run them.

At the end of the simulation, the makespan is reported, together with statistics on the wait times (time
spent in the queue by the jobs while waiting to be scheduled) and on the usage of the machine.

To run the simulation, use the following command:

python replay.py "scheduling algorithm" "number of nodes" "number of jobs"

The first argument is the scheduling algorithm being used, among the ones implemented in the
algorithms.py file. The simple
fifo (first-in, first-out) scheduler is provided with the simulator. The second argument allows for trying the
same dataset over a machine of different sizes.
A third optional argument allows for limiting the number of jobs taken from the input dataset and
simulated. It might be useful if your simulations are too long.
