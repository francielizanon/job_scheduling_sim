class Cluster:
    """Holds a list of identical nodes. Handles their use.

    Attributes
    ----------
    total_nodes : int
        Number of nodes in the cluster
    available_nodes : int
        Number of nodes currently available in the cluster
    used_resources : int
        Accumulated seconds-nodes used by jobs.

    Notes
    -----
    used_resources accumulates over the execution the number of
    seconds-nodes used by jobs being executed. This is done so we can
    calculate the usage of the cluster at the end of the simulation.
    """

    def __init__(self, nodes):
        self.total_nodes = nodes
        self.available_nodes = nodes
        self.used_resources = 0

    def schedule_job(self, job, clock):
        """Schedules a job in the cluster.

        Parameters
        ----------
        job : Job object
            Job being scheduled.
        clock : int
            Timestamp of the start of the job's execution

        Returns
        -------
        bool
            True if the job was successfully scheduled

        Notes
        ----
        This method updates the Job object when it is scheduled
        and it starts the job's execution.
        This means calling the schedule() method of the Job
        object and removing nodes from the list of available nodes.
        """
        # Checks if the job can be scheduled right now
        if job.nodes > self.available_nodes:
            print(f'[{clock}] Job {job.jobID} is trying to run on' +
                  f' {job.nodes} but only {self.available_nodes}' +
                  'are available.')
            return False

        # Schedules job, nodes become unavailable for the time being
        self.available_nodes -= job.nodes
        job.schedule(clock)

        return True

    def finish_job(self, job, clock):
        """Finishes a job and frees its resources.

        Parameters
        ----------
        job : Job
            the job object corresponding to the job that
            has finished its execution.
        clock : int
            the timestamp of when the job has finished.

        Notes
        -----
        This method is called when a job has finished its execution.
        It updates the required Job object.
        This includes putting the nodes back into the
        available_nodes list, and updating the used_resources
        counter.
        """
        # Frees the resources
        self.available_nodes += job.nodes
        # Updates the statistics
        self.used_resources += job.nodes * job.run_time

    def report_statistics(self, makespan):
        """Reports statistics on the usage of the machine.
        To be called at the end of the simulation.

        Parameters
        ----------
        makespan : int
            the total time required to run all the submitted jobs

        Returns
        -------
        string
            the statistics as a string, ready to be printed
        """
        # Calculates how many seconds-nodes we could have used in
        # this makespan, and compares it to how much we actually used
        total_resources = makespan * self.total_nodes
        idle = total_resources - self.used_resources
        ret = (f'Usage of the machine:\n' +
               f'- {self.used_resources} node-seconds were used,' +
               f' from {total_resources} available.\n' +
               f'- Nodes spent {idle} seconds in idle,' +
               f' or {((idle*100)/total_resources)}%.')
        return ret
