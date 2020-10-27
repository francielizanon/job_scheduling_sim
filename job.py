class Job:
	"""
	Contains information about a job that is queued or running.

	...
	
	Attributes
	----------
	jobID : int
		an identifier for this job (it comes from the input
		file)
	submit_time : int
		timestamp of when the job was submitted to the system
	requested_run_time : int
		amount of time requested by the user when he or she
		submitted the job
	run_time : int
		the amount of time actually required by the job
		to run. IMPORTANT: this information is NOT available
		for schedulers, it is unknown at submission time (we'll
		only use it to simulate the execution).
	nproc : int
		number of nodes requested by the job
	schedule_time : int
		timestamp of when the job has been scheduled (so we can
		calculate the wait time). It will be -1 until the job
		has been scheduled
	nodes : List of Node objects
		the list of the nodes being used by the job (only
		relevant after the job has been scheduled).

	Methods
	-------
	"""
	def __init__(self, jobID, submit_time, run_time, requested_run_time, nproc):
		self.jobID = jobID
		self.submit_time = submit_time
		self.run_time = run_time
		self.requested_run_time = requested_run_time
		self.nproc = nproc
		self.schedule_time = -1
		self.nodes = []

	def schedule(self, clock, node_list):
		"""
		Called when a job is scheduled to run in a certain set
		of nodes.

		Parameters
		----------
		clock : int
			the timestamp of when the job is starting its
			execution
		node_list : List of Node objects
			the list of the nodes where the job will
			execute
		"""
		self.nodes = node_list
		self.schedule_time = clock

	def get_wait_time(self):
		"""
		Returns the time spent by the job in the queue, waiting
		to be scheduled.
		Only relevant after the job has been scheduled.
		"""
		assert self.schedule_time >= 0
		assert self.schedule_time >= self.submit_time
		return self.schedule_time - self.submit_time

	def __lt__ (self, other):
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
		return "{"+str(self.jobID)+", "+str(self.nproc)+" nodes for "+str(self.requested_run_time)+"s}"
