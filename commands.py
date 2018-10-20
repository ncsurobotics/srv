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
