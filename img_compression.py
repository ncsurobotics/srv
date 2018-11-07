import cv2
from srv_settings import IMG_BUFFER, START_QUALITY, MIN_QUALITY, QUALITY_SHRINK_RATE
import pickle

def compress(img):
  #goal here is to automatically scale down quality until length is small enough to be sent
  quality = START_QUALITY
  mustBeMoreCompressed = True
  while mustBeMoreCompressed and quality > MIN_QUALITY:
      result, encodedImg = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
      data = pickle.dumps(encodedImg)
      mustBeMoreCompressed = (len(data) > IMG_BUFFER)
      quality -= QUALITY_SHRINK_RATE
  #print "Compressed data to size: ", len(data)
  return data

def decompress(compressedImg):
  return cv2.imdecode(compressedImg, 1)