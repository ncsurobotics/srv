"""
Executed to start the server.
If the server is killed or crashes, clients are notified.
"""
import server
import traceback

"""
Run the server normally. If an exception, error, or signal occurs, clean up the server.
"""
def main():
  try:
    server.run()
  except BaseException as e:
    #only print out error messages
    if e.__class__.__name__ != 'KeyboardInterrupt':
      print traceback.format_exc()

    #if any error happens, make the server call its exit function then die
    server.cleanUp()
    raise e

if __name__ == "__main__":
  main()