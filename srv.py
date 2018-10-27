from server import *
from source import *
import subprocess
import time

srvp = None

def connect():
  srvp = subprocess.Popen([sys.executable, "server.py", "run"])
  print "SRV PID:", srvp
  return srvp

def stream(name):
  return getSource(name)

def kill(srvp):
  srvp = subprocess.Popen([sys.executable, "client.py", "kill"])
  print "Killed SRV"

def test():
  s = connect()
  time.sleep(2)
  for i in range(100):
    print "moo"
  kill(s)