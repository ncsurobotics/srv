"""
Package for compressing and decompressing images.
"""
import cv2
from srv_settings import IMG_BUFFER, START_QUALITY, MIN_QUALITY, QUALITY_SHRINK_RATE
import pickle

def compress(img, quality=80):
  #compress at 80% quality
  result, encodedImg = cv2.imencode('.jpg', img, [int(cv2.IMWRITE_JPEG_QUALITY), quality])
  return encodedImg

def decompress(compressedImg):
  return cv2.imdecode(compressedImg, 1)