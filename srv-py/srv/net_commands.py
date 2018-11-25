"""The command that connects a client."""
class Connect(object):
    dummy = []

"""The command that disconnects a client."""
class Disconnect(object):
    dummy = []

"""The command that kills the server."""
class Kill(object):
    """Dummy variable. This object carries no extra data."""
    dummy = []

"""The command that lets a client know that the stream is over"""
class StreamEnd(object):
    """Dummy variable. This object carries no extra data."""
    dummy = []

"""The command that lets a client know that the source name is not found"""
class UnknownSource(object):
    """Dummy variable. This object carries no extra data."""
    dummy = []

"""Request an image. Requires the name of the camera
to send it to."""
class Image(object):
    cam = []
    ip_port = []

    """Construct a RequestImage object.
Use the cam parameter to determine which camera to request."""
    def __init__(self, cam):
        self.cam = cam
        return
"""Request from client to SRV to post an image to SRV with the given name."""
class Post(object):
    def __init__(self, name, compressedImg):
        self.name = name
        self.compressedImg = compressedImg

"""Request to get all sources in SRV."""
class GetSources(object):
    dummy = []

"""Request to start camera feed."""
class StartCams(object):
    dummy = []

"""Request to swap down and front cameras"""
class SwapCams(object):
    dummy = []

"""Lets client connections know when the server has been killed."""
class ServerKilled(object):
    dummy = []