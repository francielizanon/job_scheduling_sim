class Node:
	"""
	Contains information about a node from the cluster

	...

	Attributes
	----------
	free : boolean
		if the node is available or not (it is not available
		when it is running a job)
	ETA : int
		if the node is NOT available, when it is expected to
		become available again (that depends on the requested
		time by the job, it might become available earlier)
	ID : int
		identifier of this node 
	"""
	def __init__(self, ID):
		self.free = True
		self.ETA = 0
		self.ID = ID

	def __lt__ (self, other):
		"""
		This is the < comparator, used to break ties if we want
		to insert objects of this class in heaps, called when
		two Nodes have the same key used for insertion in the
		heap. In that case we simply order them by id.
		"""
		return self.ID < other.ID

	def __str__(self):
		"""
		Function used when we try to print() an object of this
		class. We will print only the id.
		"""
		return str(self.ID)

class Cluster:
	"""
	Holds a list of identical nodes and handles the running of jobs
	on them

	...
	
	Attributes
	----------
	nodes : list of Node objects
		list of all the nodes in the system
	available_nodes : list of Node objects
		list of nodes that are currently available to run jobs	
	used_resources : int
		accumulates over the execution the amount of
		seconds-nodes used by jobs  being executed (so we can
		calculate the usage of the machine at the end of the
		simulation)
	"""
	def __init__(self, nodes):
		self.nodes = []
		self.available_nodes=[]
		for i in range(0, nodes):
			newnode = Node(i)
			self.nodes.append(newnode)
			self.available_nodes.append(newnode)
		self.used_resources = 0

	def getFirstAvailableNodes(self, nb):
		"""
		Returns the first nb nodes from the list of available
		nodes.
		Caller must check first if there are nb elements in 
		the list!
		This function will NOT remove the nodes from the list.

		Parameters
		----------
		nb : int
			The number of nodes to be returned

		Returns
		-------
		List
			a list of nb nodes, taken from the
			available_nodes list.
		"""
		assert nb <= len(self.available_nodes)
		ret = []
		for i in range(0, nb):
			ret.append(self.available_nodes[i])
		return ret

	def schedule_job(self, job, node_list, clock):
		"""
		Makes the updates to the Job and Node objects required
		when a job is scheduled and will start its execution.
		That means calling the schedule() method of the Job
		object, updating free and ETA attributes of each Node
		object, and removing all nodes given in the input list
		from the available_nodes list.

		Parameters
		----------
		job : Job
			the Job object corresponding to the job being
			scheduled. 
		node_list : List of Node objects
			the nodes where the job will execute
		clock : int
			the timestamp of when the execution of the job
			is starting
		"""
		job.schedule(clock, node_list)
		ETA = clock + job.requested_run_time 
		for node in node_list:
			self.available_nodes.remove(node)
			node.free = False
			node.ETA = ETA

	def finish_execution(self, job, clock):
		"""
		Called when a job has finished its execution. Makes the
		updates required in the Job and Node objects. That 
		includes putting the nodes back into the
		available_nodes list, and updating the used_resources
		counter.
		
		Parameters
		----------
		job : Job
			the job object corresponding to the job that
			has finished its execution.
		clock : int
			the timestamp of when the job has finished.
		"""
		self.used_resources = len(job.nodes)*job.run_time 
		for node in job.nodes:
			node.free = True
			self.available_nodes.append(node)

	def report_statistics(self,makespan):
		"""
		Reports statistics on the usage of the machine, to be
		called at the end of the simulation.

		Parameters
		----------
		makespan : int
			the total time required to run all the
			submitted jobs
		
		Returns
		-------
		string
			the statistics as a string, ready to be
			printed.
		"""
		#calculate how many seconds-nodes we could have used in
		# this makespan, and compare to how much we actually
		# used to give a metric of usage of the machine
		total_resources = makespan * len(self.nodes) 
		idle = total_resources - self.used_resources
		ret = "Usage of the machine:\n"
		ret += str(self.used_resources)+" seconds were used, "
		ret += "from "+str(total_resources)+" available. Nodes"
		ret += "spent "+str(idle)+" seconds in idle, "
		ret += str((idle*100)/total_resources)+"%."
		return ret
