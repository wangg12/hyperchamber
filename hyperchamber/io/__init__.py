import requests
import json

import sys

from json import JSONEncoder

class HCEncoder(JSONEncoder):
  def default(self, o):
    if(hasattr(o, '__call__')): # is function
      return "function:" +o.__module__+"."+o.__name__
    else:
      return o.__dict__    

def get_api_path(end):
  return "https://hyperchamber.255bits.com/api/v1/"+end

def apikey(apikey):
  """Sets up your api key."""
  print("TODO: Api keys")

def sample(config, images):
  """Upload a series of images.  Images are ignored if the rate limit is hit."""
  url = get_api_path('intrinsic.json')
  multiple_files = []
  for image in images:
    multiple_files.append(('images', (image, open(image, 'rb'), 'image/png')))
  headers = {"config": json.dumps(config, cls=HCEncoder)}
  try:
      r = requests.post(url, files=multiple_files, headers=headers, timeout=30)
      return r.text
  except:
      e = sys.exc_info()[0]
      print("Error while calling hyperchamber - ", e)
      return None

def record(config, result, max_retries=10):
  """Records results on hyperchamber.io.  Used when you are done testing a config."""
  url = get_api_path('run.json')
  data = {'config': config, 'result': result}
  retries = 0
  while(retries < max_retries):
      try:
          r = requests.post(url, data=json.dumps(data, cls=HCEncoder), headers={'Content-Type': 'application/json'}, timeout=30)
          return r.text
      except:
          e = sys.exc_info()[0]
          print("Error while calling hyperchamber - retrying ", e)
          retries += 1
