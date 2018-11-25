from multiprocessing import Process, Queue

"""
Function that does the work. Each worker constantly runs this. Tasks is a queue of
(function, args). Calling get() blocks if the queue is empty, meaning the process
running this function waits until a new item appears in the queue. The worker
constantly takes qwork from the queue and does it while it is available, waiting
once there is no work.
"""
def worker(tasks):
  while True:
    func, args = tasks.get()
    func(*args)

"""
Represents a pool of worker objects. Assigns a function to each worker to execute.
If no workers are available, put a function on the back burner. Once a worker becomes free,
the worker, the worker works on the back burner.
"""
class WorkerPool(object):
  def __init__(self, num_workers):
    self.worker_list = []
    self.jobs = Queue()
    for i in range(num_workers):
      p = Process(target=worker, args=(self.jobs,))
      self.worker_list.append(p)
      p.start()
  """Adds work to the job queue"""
  def addWork(self, function, arguments):
    self.jobs.put((function, arguments))