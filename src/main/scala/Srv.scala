import jnr.posix.POSIXFactory
import jnr.posix.POSIX

/**
 * The entry point for the server.
 * This file starts up the server, then 
 * @author Jacob Salzberg
 */
object Srv {
  /**
   * Main function
   * @param args command line arguments. Should be the path of the server's jar.
   */
  def main(args: Array[String]): Unit = {
    // Get a posix implementation from the posix factory
    val posix = POSIXFactory.getNativePOSIX()
  }
}
