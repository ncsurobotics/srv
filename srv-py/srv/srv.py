from server import *
from source import *
from connection import *
import subprocess
import os
import time

import startServer
import startCams
import watch as watchStreams
import swapCams
import record as recordStream
from multiprocessing import Process, Queue
import psutil

# out_file : process
record_processes = {}

"""
SRV commands to start server, start cams, watch streams, and swapping cams.
"""
def server():
  startServer.main()

def cams():
  startCams.main()

def watch():
  watchStreams.main()

def swap():
  swapCams.main()

#TODO add in ability to record multiple streams
def record(stream, out_file, show_feed=False):
  global record_processes
  record_queue = Queue()
  proc = Process(target=recordStream.main, args=(stream, out_file, record_queue, show_feed))
  proc.start()
  record_pid = record_queue.get()
  record_processes[out_file] = record_pid

def stop_recording(name=None):
  global record_processes
  # kill all if name is none
  if name == None:
    names = []
    for name in record_processes:
      names.append(name)
    for name in names:
      proc = psutil.Process(record_processes[name])
      proc.terminate()
      record_processes.pop(name, None)
  else:
    proc = psutil.Process(record_processes[name])
    proc.terminate()
    record_processes.pop(name, None)


"""
Commands that are probably deprecated, need to remove if never called.
"""
srvp = None

#TODO remove connect, playdown, and kill as they are deprecated. Everything here deprecated except stream.

def connect():
  srvp = os.system('python /usr/local/lib/python2.7/dist-packages/srv/server.py run &')
  #srvp = os.spawnl(os.P_WAIT, 'python /usr/local/lib/python2.7/dist-packages/srv/server.py run')
  #srvp = subprocess.Popen([sys.executable, "sh", "/usr/local/lib/python2.7/dist-packages/srv/startSrv.sh", "&"])
  print "SRV PID:", srvp
  return srvp

def playDown():
  #connect()
  #time.sleep(3)
  clip = os.system('python /usr/local/lib/python2.7/dist-packages/srv/client.py down &')
  #srvp = subprocess.Popen([sys.executable, "sh", "/usr/local/lib/python2.7/dist-packages/srv/startSrv.sh", "&"])
  print "client PID:", clip
  return clip
"""Open connection for client to SRV server."""
def stream(name):
  return Connection(name)

def kill(srvp):
  os.system('python /usr/local/lib/python2.7/dist-packages/srv/client.py kill')
  print "Killed SRV"
"""Start video capture of the cam streams."""
