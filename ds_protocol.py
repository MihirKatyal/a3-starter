import json
from collections import namedtuple

DataTuple = namedtuple('DataTuple', ['type','message','token'])
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

def extract_json(json_msg:str) -> DataTuple: #Call the json.loads function on a json string and convert it to a DataTuple object
  try:
    json_obj = json.loads(json_msg)
    response_type = json_obj.get('response', {}).get('type', 'unknown')  # Default to 'unknown' if not found
    message = json_obj.get('response', {}).get('message', '')  # Default to empty string if not found
    token = json_obj.get('response', {}).get('token', None)  # Default to None if not found
  except json.JSONDecodeError:
    print("Json cannot be decoded.")
    return DataTuple('json_error', 'Json cannot be decoded', None)

  return DataTuple(foo, baz)
