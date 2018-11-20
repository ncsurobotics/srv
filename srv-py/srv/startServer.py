import server

server.run()

try:
  server.run()
except BaseException as e:
  #if any error happens, make the server call its exit function then die
  server.exit()
  #should be extended for signal interrupt too
  #need to let clients know it died
  #connection can throw an exception once it gets a message seerver has died