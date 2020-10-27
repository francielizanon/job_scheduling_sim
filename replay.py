"""
Script that replays the jobs from the ANL-Intrepid-2009-1.swf.gz dataset,
considering a different scheduling algorithm and a simplified, 
configurable-sized system.
"""
import heapq
import math
import sys
from numpy import min,max,mean,median,sum
from job import Job
from node import Node,Cluster
from event import Event
from utils import printable
import algorithms

def usage_and_out(argv):
	print("Usage: python "+argv[0]+" scheduling_algorithm number_of_nodes number_of_jobs (optional)")
	exit()


debug = False

#get the input parameters
if len(sys.argv) < 3:
	usage_and_out(sys.argv)
algorithm = sys.argv[1]
nodes_nb = int(sys.argv[2])
if debug:
	print("I will run the simulation using the "+algorithm+" scheduler for a machine of "+str(nodes_nb)+" nodes.")
if len(sys.argv) == 4:
	task_limit = int(sys.argv[3])
	if debug:
		print("For that I will only read the first "+str(task_limit)+" jobs from the input file")
else:
	task_limit = -1

try: #get the scheduling function identified by its name
	schedule = getattr(algorithms, algorithm) 
except AttributeError:
	print("PANIC! Could not find scheduling algorithm "+algorithm)
	exit()

cluster = Cluster(nodes_nb) #creates the list of nodes, initially all 
			 #available
if debug:
	print("Created the list of "+str(len(cluster.nodes))+" nodes, "+str(cluster.nodes[0])+" to "+str(cluster.nodes[len(cluster.nodes)-1]))

events = [] #we'll have a heap of events, which may be arrival of new 
	    #jobs, or jobs finishing their execution.
clock = 0

#read all jobs from the input file and add their arrivals to the heap
# of events.
# we also keep a list of all jobs so we can gather statistics at the end
alljobs = [] 
infile = open("ANL-Intrepid-2009-1.swf", "r")
print("I'm reading the input file")
for line in infile:
	if line[0] == ";": #skip the first line
		continue
	parsed = line.split()
	assert (len(parsed) == 18)
	#add an event for this job's submission time
	submission = int(parsed[1])
	nproc = int(parsed[7])
	nproc = math.ceil(float(nproc)/4.0)
	jobid = int(parsed[0])
	run = int(parsed[3])
	required_run = int(parsed[8])
	if nproc > nodes_nb: #sanity check: we cannot submit a task asking
			  # for more nodes than what we have in the
			  # machine.
		print("PANIC! The number of nodes in the machine has to be at least "+str(nproc))
		print(line)
		infile.close()
		exit()
	assert nproc > 0
	newjob = Job(jobid, submission, run, required_run, nproc) 
	alljobs.append(newjob)
	heapq.heappush(events, (submission, Event(True, newjob))) 
	#respect the limitation on the number of tasks 
	if (task_limit > 0) and (len(alljobs) >= task_limit):
		break #we are done adding jobs
infile.close()
print("I'm done reading the input file, I will start the simulation now")

queue = [] #list of the jobs that were submitted but not executed yet 
wait_times = []	#to keep track of how long the jobs stay in the queue
scheduled_jobs = 0
queue_length = []
#execute jobs until we run out of them
while len(events) > 0:
	#schedule new jobs while possible
	if len(queue) > 0:	#if there are queued jobs
		if debug:
			print("There are "+str(len(queue))+" jobs in the queue, so we will try to schedule! "+printable(queue))
		newdecision = True
		while newdecision and (len(queue)>0):
			newdecision,job,node_list = schedule(queue, cluster)
			if newdecision:	#if our scheduler has decided
					# to schedule a job
				assert len(node_list) == job.nproc
				if debug:
					print("The scheduler has decided to schedule the job "+str(job)+" in the nodes "+str(node_list[0])+" to "+str(node_list[len(node_list)-1]))
					print("Available nodes from "+str(cluster.available_nodes[0])+" to "+str(cluster.available_nodes[len(cluster.available_nodes)-1]))
				#update the job and node objects
				cluster.schedule_job(job, node_list, clock)
				if debug:
					print("There are now "+str(len(cluster.available_nodes))+" available nodes")
				#remove the job from the queue
				queue.remove(job) 
				#schedule the event for when this jobs
				# finishes its execution
				heapq.heappush(events, (clock + job.run_time, Event(False, job)))
				wait_times.append(job.get_wait_time())
				scheduled_jobs += 1
				if (scheduled_jobs % 1000) == 0:
					print(scheduled_jobs)
	#we are done scheduling jobs, so we fast-forward to the next
	#event
	clock,newEvent = heapq.heappop(events)
	#check the event type and act accordingly
	if newEvent.isNewJob: #submission of a new job
		queue.append(newEvent.job_info) #add it to our queue
		queue_length.append(len(queue))
		if debug:
			print("Time moved to timestamp "+str(clock)+", when job "+str(newEvent.job_info)+" was submitted. We now have "+str(len(queue))+" queued jobs.") 
	else: #a job has finished its execution
		#free the nodes that were being used by this job
		cluster.finish_execution(newEvent.job_info, clock) 
		if debug:
			print("Time moved to timestamp "+str(clock)+", when job "+str(newEvent.job_info)+" finished its execution. We now have "+str(len(cluster.available_nodes))+" available nodes.")
assert (len(queue) == 0)
#end of the simulation, give statistics
print("I've finished the simulation.")
print("makespan: "+str(clock))
print("wait times: ")
print("min: "+str(min(wait_times))+" max: "+str(max(wait_times))+" mean: "+str(mean(wait_times))+" median: "+str(median(wait_times))+" total (sum): "+str(sum(wait_times)))
print(cluster.report_statistics(clock))
