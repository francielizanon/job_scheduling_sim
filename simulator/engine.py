"""Simulation engine module.

Replays the jobs from the ANL-Intrepid-2009-1.swf.gz dataset.

It uses a different scheduling algorithm and a simplified,
configurable-sized system.
"""

import heapq
import math
from numpy import min, max, mean, median, sum
from simulator.job import Job
from simulator.node import Cluster
from simulator.event import Event
from simulator.utils import printable
import simulator.algorithms as algorithms


class Engine:
    """Simulation engine.

    Attributes
    ----------
    debug : bool
        True if debug messages should be printed
    scheduler : function from algorithms
        Scheduler to be used during simulation
    cluster : Cluster object
        Cluster with a given number of nodes
    events : heap of events
        Structure organizing events in the simulation
        (start of jobs, end of jobs)
    clock : int
        Time in the simulation

    """
    def __init__(self,
                 algorithm_name,
                 nodes,
                 task_limit,
                 input_file='ANL-Intrepid-2009-1.swf',
                 debug=False):
        """Creates the simulation engine.

        Parameters
        ----------
        algorithm_name : string
            Name of the scheduling algorithm to use
        nodes : int
            Number of nodes in the cluster
        task_limit : int
            Number of tasks to read from the input file
        input_file : string [default=ANL-Intrepid-2009-1.swf]
            Name of the file containing the cluster's log
        debug : bool [default=False]
            True if debug messages should be printed
        """
        self.debug = debug

        try:  # gets the scheduling function identified by its name
            self.scheduler = getattr(algorithms, algorithm_name)
            if self.debug:
                print(f'DEBUG: Set {algorithm_name} as the scheduler.')
        except AttributeError:
            print('PANIC! Could not find scheduling algorithm' +
                  f' {algorithm_name}. Stopping execution.')
            exit()

        self.cluster = Cluster(nodes)
        if self.debug:
            print(f'DEBUG: Created the cluster with {nodes} nodes.')

        self.events = []
        self.clock = 0
        num_jobs = 0

        # Reads the input file to populate 'events' and ''jobs'
        print(f'Reading file {input_file} to populate the simulation')
        infile = open(input_file, 'r')

        for line in infile:
            if line[0] == ";":  # skips comments
                continue
            parsed = line.split()
            assert (len(parsed) == 18)
            # adds an event for this job's submission time
            submission = int(parsed[1])
            jobid = int(parsed[0])
            run = int(parsed[3])
            required_run = int(parsed[8])

            nproc = int(parsed[7])
            nodes = math.ceil(float(nproc)/4.0)
            assert nodes > 0
            # checks if this job can run on the simulated cluster
            if (nodes > self.cluster.total_nodes):
                if debug:
                    print(f'- Skipping job {jobid} as it requires' +
                          f' {nodes} > {self.cluster.total_nodes}' +
                          ' nodes.')
                continue

            # creates the job and adds it to the list
            newjob = Job(jobid, submission, run, required_run, nodes)
            num_jobs += 1  # another job created
            heapq.heappush(self.events, (submission, Event(True, newjob)))

            # respects the limitation on the number of tasks
            if (task_limit > 0) and (num_jobs >= task_limit):
                break  # we are done adding jobs

        # Closes the file
        infile.close()
        print('Finished reading the input file.' +
              f' {num_jobs} jobs will be scheduled on' +
              f' {self.cluster.total_nodes}' +
              ' nodes. Ready for simulation.')

    def run(self):
        """Simulates the scheduling of tasks on a cluster.

        Returns
        -------
        int
            Makespan of the whole simulation
        """

        print('Starting the simulation.')
        # list of the jobs that were submitted but not executed yet
        queue = []
        # list to keep track of how long the jobs stay in the queue
        wait_times = []
        # list to keep track of the completion time of the jobs
        completion_times = []
        scheduled_jobs = 0

        events = self.events
        # executes jobs until we run out of them
        while (len(events) > 0) or (len(queue) > 0):
            # schedules new jobs while possible
            if len(queue) > 0:  # if there are queued jobs
                if self.debug:
                    print('DEBUG: Jobs in the queue to schedule:' +
                          f'{printable(queue)}')

                # Checks with the scheduler if there are any
                # jobs that it is able to schedule right now
                newdecision = True
                while newdecision and (len(queue) > 0):
                    newdecision, job = self.scheduler(queue,
                                                      self.cluster,
                                                      self.clock)

                    # checks if the scheduler found a suitable job
                    if newdecision:
                        if self.debug:
                            print(f'DEBUG: Scheduling job {job.jobID} on' +
                                  f' {job.nodes} nodes from the' +
                                  f' {self.cluster.available_nodes}' +
                                  ' nodes available in the cluster.')

                        # updates the job and node objects
                        self.cluster.schedule_job(job, self.clock)
                        # removes the job from the queue
                        queue.remove(job)
                        # schedules the event for when this job
                        # finishes its execution
                        heapq.heappush(self.events,
                                       (self.clock + job.run_time,
                                        Event(False, job)))
                        # stores the wait time for this job
                        wait_times.append(job.get_wait_time())
                        # stores the predicted completion time of this job
                        completion_times.append(self.clock + job.run_time)
                        # counts another scheduled job
                        scheduled_jobs += 1
                        if (scheduled_jobs % 1000) == 0:
                            print(f'- Scheduled the {scheduled_jobs}' +
                                  'th job.')

            # All jobs that the scheduler deemed ready for execution
            # are now scheduled.
            # We now fast-forward to the next event.
            self.clock, newEvent = heapq.heappop(events)
            # checks the event type and acts accordingly
            if newEvent.isNewJob:  # submission of a new job
                queue.append(newEvent.job_info)  # adds the job to the queue

                if self.debug:
                    print(f'DEBUG: time moved to timestamp {self.clock}.' +
                          f' Job {newEvent.job_info} was submitted now.' +
                          f' The queue now has {len(queue)} jobs.')
            else:  # a job has finished its execution
                # frees the nodes that were being used by this job
                self.cluster.finish_job(newEvent.job_info, self.clock)

                if self.debug:
                    print(f'DEBUG: time moved to timestamp {self.clock}.' +
                          f' Job {newEvent.job_info} finished now.' +
                          ' The cluster now has' +
                          f' {self.cluster.available_nodes} nodes available.')

        # making sure we emptied the queue too when we finished all events
        assert (len(queue) == 0)

        # End of the simulation: print statistics
        print('Simulation finished.\nStatistics:')
        print(f'- makespan: {self.clock}')
        print(f'- total completion time: {sum(completion_times)}')
        print('- wait times:')
        print(f'-- min: {min(wait_times)}')
        print(f'-- max: {max(wait_times)}')
        print(f'-- mean: {mean(wait_times)}')
        print(f'-- median: {median(wait_times)}')
        print(f'-- total (sum): {sum(wait_times)}')
        print(self.cluster.report_statistics(self.clock))

        return self.clock
