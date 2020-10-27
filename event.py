class Event:
	"""
	Contains information about an upcoming event, which will be
	included in a heap.
	
	...

	Attributes
	----------
	isNewJob : boolean
		is this event a job submission? if False, then the 
		event is actually the ending of a job
	job_info : Job object
		the job involved in this event (either being submitted
		or finishing its execution).

	Methods
	-------
	"""
	def __init__(self, isnewjob, job_info):
		self.isNewJob = isnewjob
		self.job_info = job_info
	
	def __lt__(self, other):
		"""
		This is the < comparator, used to break ties in the
		events heap (how to choose the order between events
		with the same timestamp?).
		We give priority for jobs finishing their execution.
		If they are both events of the same type, we order by
		job ID.

		Parameters
		----------
		other : Event
			other object of the same class to be compared
			with this one.

		Returns
		-------
		bool
			is this object smaller than the other object?
		"""
		if (not self.isNewJob) and other.isNewJob:
			return True
		elif self.isNewJob and (not other.isNewJob):
			return False
		else: #they are both arrivals or departs
			return self.job_info.jobID < other.job_info.jobID
