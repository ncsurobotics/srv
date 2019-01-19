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
