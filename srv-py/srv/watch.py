"""
Watch some or all SRV video streams.
"""
import srv
import cv2
import connection
from StreamFinishedException import StreamFinishedException
import sys
import signal
import socket
from windows import window, destroyWindow, imshow
from multiprocessing import Queue
import time

keep_playing = True

def getSources(sourcesConnection):
  sources = sourcesConnection.getSources()
  return sources


"""
Looks for any windows that need to be killed.
"""
def endWindows(queues, ignored):
  global keep_playing
  for name in queues:
    try:
      msg = queues[name].get(False)
      if msg == 'kill' and name not in ignored:
        ignored.append(name)
      if msg == 'kill all':
        keep_playing = False
    except:
      pass

"""
Forever loop and play SRV streams.
"""
def run(sourcesConnection):
  global keep_playing
  keep_playing = True
  #update_sources_constantly = True
  connections = []
  sources = []
  ignoredSources = []
  
  windowQueues = {}
  start = time.clock()

  while keep_playing:
    
    #if the system argument just wanted to watch all videos, constantly update sources
    #TODO fix this so that it blocks when there are no sources
    #TODO fix this so that the server notifies it when sources are added and removed

    #if update_sources_constantly:
    newSources = getSources(sourcesConnection)
  
    """
    Find old sources and remove them.
    """
    finished_source_indexes = []
    for i in range(len(sources)):
      # if a source isn't in new sources, it has been closed
      if sources[i] not in newSources or sources[i] in ignoredSources:
        finished_source_indexes.append(i)
    for idx in finished_source_indexes:
      connections.pop(idx)
      src = sources.pop(idx)
      destroyWindow(src)
      print  src, "not in SRV Sources or closed."
      if len(sources):
        print "Now showing", ', '.join(sources)
      else:
        print "Now showing no sources"

    """
    Find new sources and add windows for them.
    """
    for i in range(len(newSources)):
      if newSources[i] not in sources and newSources[i] not in ignoredSources:
        windowQueues[newSources[i]] = Queue()
        window(newSources[i], responseQueue=windowQueues[newSources[i]])
        connections.append(connection.Connection(newSources[i]))
        print "Adding source to watch:", newSources[i]
    # sources can now be the sources on the server
    sources = newSources
    # remove ignored sources
    for src in ignoredSources:
      if src in sources:
        sources.remove(src)

    # go through and show the next frame from each video source
    for i in range(len(sources)):
      try:
        imshow(sources[i], connections[i].getNextFrame())
      except StreamFinishedException as finExcp:
        connections.pop(i)
        src = sources.pop(i)
        windowQueues.pop(sources[i])
        destroyWindow(src)
        print src, "stream finished."
        break
      except Exception as excp:
        print "Haven't heard from srv connection or watch application quit."
        keep_playing = False
        break
    endWindows(windowQueues, ignoredSources)
  for sourceName in sources:
    destroyWindow(sourceName)
    


"""
Print out help messages.
"""
def help():
  print "To play specific sources:"
  print "\tusage: python watch.py source_1 source_2 ..."
  print "(indefinite amount of listed sources to be played)"
  print "To play all sources:"
  print "\tusage: python watch.py"

def main():
  """
  Connection and function to get sources from SRV.
  """
  sourcesConnection = connection.Connection("get sources")

  """
  Parse command line arguments and start playing windows.
  The main function area.
  """

  #srvSources = getSources(sourcesConnection)

  if len(sys.argv) == 1:
    sources = getSources(sourcesConnection)
  elif len(sys.argv) == 2:
    if sys.argv[1].lower() == "help":
      help()
    else:
      #just 1 source
      sources = [sys.argv[1]]
  else:
    #each command line argument is a source name
    sources = []
    for i in range(1,len(sys.argv)):
      sources.append(sys.argv[i])
  
  # what to do when ctrl-c is hit
  signal.signal(signal.SIGINT, quit)
  run(sourcesConnection)

"""
Tell program to stop playing.
"""
def quit(*args):
  global keep_playing
  print "QUITTING"
  keep_playing = False
    

if __name__ == "__main__":
  main()