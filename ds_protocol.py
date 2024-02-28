import json
from collections import namedtuple

# Namedtuple to hold the values retrieved from json messages.
# TODO: update this named tuple to use DSP protocol keys
DataTuple = namedtuple('DataTuple', ['foo','baz'])

ErrorTuple = namedtuple('ErrorTuple', ['type', 'message', 'token'])

def join(username, password): # Create a join request in JSON formt
  return json.dumps({
    "join": {
      "username": username,
      "password": password,
      "token": ""
    }
  })

def post(token, message): # Create a post request in JSON format
  return json.dumps({
    "token": token,
    post: {
      "entry": message,
      "timestamp": "" 
    }
  })

def bio(token, bio): # Create a bio request in JSON format
  return json.dumps({
    "token": token,
    "bio": {
      "entry": bio,
      "timestamp": ""
    }
  })

def extract_json(json_msg: str):
    try:
        return json.loads(json_msg)
    except json.JSONDecodeError:
        print("JSON cannot be decoded.")
        return None

def extract_json(json_msg:str) -> DataTuple:
  '''
  Call the json.loads function on a json string and convert it to a DataTuple object
  
  TODO: replace the pseudo placeholder keys with actual DSP protocol keys
  '''
  try:
    json_obj = json.loads(json_msg)
    foo = json_obj['foo']
    baz = json_obj['bar']['baz']
  except json.JSONDecodeError:
    print("Json cannot be decoded.")

  return DataTuple(foo, baz)
