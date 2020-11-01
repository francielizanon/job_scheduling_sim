class Job:
    """Contains information about a job that is queued or running.

    Attributes
    ----------
    jobID : int
        Identifier for this job (it comes from the input file)
    submit_time : int
        Timestamp of when the job was submitted to the system
    requested_run_time : int
        Amount of time requested by the user when he or she submitted the job
    run_time : int
        Amount of time actually required by the job to run
    nodes : int
        Number of nodes requested by the job
    schedule_time : int
        Timestamp of when the job was scheduled (to calculate the wait time)

    Notes
    -----
    IMPORTANT: the run_time information is NOT available for schedulers.
    It is unknown at submission time.
    We only use it to simulate the execution.
    """
    def __init__(self, jobID, submit_time,
                 run_time, requested_run_time, nodes):
        self.jobID = jobID
        self.submit_time = submit_time
        self.run_time = run_time
        self.requested_run_time = requested_run_time
        self.schedule_time = -1
        self.nodes = nodes

    def schedule(self, clock):
        """Called when a job is scheduled to run

        Parameters
        ----------
        clock : int
            the timestamp of when the job is starting its execution
        """
        self.schedule_time = clock

    def get_wait_time(self):
        """Returns the time spent by the job in the queue

        Returns
        -------
        int
            Wait time (schedule time - submit time)
        """
        assert self.schedule_time >= 0
        assert self.schedule_time >= self.submit_time
        return self.schedule_time - self.submit_time

    def __lt__(self, other):
        """
        This is the < comparator, used to break ties if we want
        to insert objects of this class in heaps, called when
        two Jobs have the same key used for insertion in the
        heap (for instance the same amount of requested time,
        or the same number of nodes). In that case we simply
        order them by id.
        """
        return self.jobID < other.jobID

    def __str__(self):
        """
        Function used when we try to print() an object of this
        class.
        """
        text = ('{' +
                f'{self.jobID}, {self.nodes} nodes' +
                f' for {self.requested_run_time} s' +
                '}')
        return text
