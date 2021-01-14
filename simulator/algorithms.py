"""Scheduling algorithms module.
New algorithms are added here.

Notes
-----

A scheduling algorithm receives two parameters:

jobs : List of Job objects
    the current queue of jobs that were submitted to the system but
    not yet scheduled.
cluster : Cluster object
    the Cluster object, which contains the list of nodes in the
    simulation.

These parameters are read but NEVER modified by the scheduler. It will
return a decision, it will NOT actually schedule jobs.


A scheduling algorithm returns a tuple, with three values in this order:

boolean
    is the algorithm returning a decision? If this value is False,
    that means the algorithm has decided not to schedule tasks at
    this moment. In that case, the other two values are irrelevant.
Job
    the Job object describing the job chosen to be executed next.
"""


def fcfs(jobs, cluster, clock):
    """First Come, First Served scheduler.

    Parameters
    ----------
    jobs : list of Job objects
        Queue of available jobs
    cluster : Cluster object
        Cluster containing the nodes required by jobs
    clock : int
        Current clock. Useful for debugging and advanced functions

    Returns
    -------
    bool, Job
        True if a job can be scheduled + the job to be scheduled

    Notes
    -----
    This scheduler will schedule jobs in arrival order.
    If the next job in arrival order cannot be scheduled (because
    there are not enough nodes available), we DO NOT schedule
    others jobs from the queue (we'll wait).
    """
    nextjob = jobs[0]  # we will schedule the first job from the queue

    if cluster.available_nodes >= nextjob.nodes:
        # if we have enough available nodes, we can run the job.
        # For that we will take the N first available nodes
        # (where N is the number of nodes requested by the job)
        return (True, nextjob)
    else:
        # we do NOT have enough nodes, so we will not schedule applications
        return (False, None)


def ff(jobs, cluster, clock):
    """First Fit scheduler.

    Parameters
    ----------
    jobs : list of Job objects
        Queue of available jobs
    cluster : Cluster object
        Cluster containing the nodes required by jobs
    clock : int
        Current clock. Useful for debugging and advanced functions

    Returns
    -------
    bool, Job
        True if a job can be scheduled + the job to be scheduled

    Notes
    -----
    This scheduler will schedule the first job in the queue that
    fits within the available nodes.
    """
    # TODO


def sjf(jobs, cluster, clock):
    """Shortest-Job First scheduler.

    Parameters
    ----------
    jobs : list of Job objects
        Queue of available jobs
    cluster : Cluster object
        Cluster containing the nodes required by jobs
    clock : int
        Current clock. Useful for debugging and advanced functions

    Returns
    -------
    bool, Job
        True if a job can be scheduled + the job to be scheduled

    Notes
    -----
    This scheduler will schedule the jobs that have the smallest
    requested run times first.
    It only considers jobs that could be run on the available nodes.
    In the case of a tie, it choses the job with the smallest identifier.
    """
    # TODO


def fcfs_easy(jobs, cluster, clock):
    """First Come, First Served scheduler with EASY backfilling.

    Parameters
    ----------
    jobs : list of Job objects
        Queue of available jobs
    cluster : Cluster object
        Cluster containing the nodes required by jobs
    clock : int
        Current clock. Useful for debugging and advanced functions

    Returns
    -------
    bool, Job
        True if a job can be scheduled + the job to be scheduled
    """
    # TODO
    # Tips:
    # 1. Discover if you can schedule the first job
    # 2. If you cannot, then discover when it could be first scheduled.
    #    Use the information on the dict in cluster.running_jobs
    #    for that. Each job has attributes 'expected_end' and
    #    'nodes'.
    # 3. Using the predicted information, check for the first job
    #    on the list that could be scheduled without delaying the
    #    first job (i.e., its requested_run_time should be smaller
    #    than the predicted start of the first job minus the current clock).
