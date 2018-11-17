"""Default settings for this program. Will be used until a settings file is made."""
 
"""The ip and port where the server receives requests"""
SVR_ADDRESS = ("127.0.0.1", 5005)

"""The size of the image buffer"""
IMG_BUFFER = 30000


"""Initial quality image compressed to"""
START_QUALITY = 70
"""Min jpeg quality is 5"""
MIN_QUALITY = 5
"""rate quality decreases at"""
QUALITY_SHRINK_RATE = 10