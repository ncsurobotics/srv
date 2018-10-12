from srv_settings import client_ip_port


"""The command that kills the server."""
class Kill(object):
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
        self.ip_port = client_ip_port
        return
