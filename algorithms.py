"""
Scheduling algorithms module.
New algorithms are added here. 

An algorithm receives two parameters:
------------------------------------
jobs : List of Job objects
	the current queue of jobs that were submitted to the system but
	not yet scheduled.
cluster : Cluster object
	the Cluster object, which contains the list of nodes in the
	simulation.

These parameters are read but NEVER modified by the scheduler. It will
return a decision, it will NOT actually schedule jobs.

The algorithm returns a tuple, with three values in this order:
--------------------------------------------------------------
boolean
	is the algorithm returning a decision? If this value is False,
	that means the algorithm has decided not to schedule tasks at
	this moment. In that case, the other two values are irrelevant.
Job
	the Job object describing the job chosen to be executed next.
List of Node objects
	a list of nproc Node objects that will run the chosen job. 
	nproc is the number of nodes requested by the job.
"""

def fifo(jobs, cluster):
	"""
	This scheduler will schedule jobs in arrival order.
	If the next job in arrival order cannot be scheduled (because
	there are not enough nodes available), we DO NOT schedule
	others jobs from the queue (we'll wait).
	"""
	nextjob = jobs[0] #we will schedule the first job from the 
			  #queue
	
	if len(cluster.available_nodes) >= nextjob.nproc:
		#if we have enough available nodes, we can run the job.
		# For that we will take the N first available nodes
		# (where N is the number of nodes requested by the job)
		return (True,nextjob,cluster.getFirstAvailableNodes(nextjob.nproc))
	else: #we do NOT have enough nodes, so we will not schedule applications
		return (False, None, [])
