import json
from collections import namedtuple

# Definitions for response data structures
DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])

def join(username, password):
    return json.dumps({
        "join": {
            "username": username,
            "password": password,
            "token": "" 
        }
    })

def post(token, message, timestamp=time.time()):
    return json.dumps({
        "token": token,
        "post": {
            "entry": message,
            "timestamp": str(timestamp)  
        }
    })

def bio(token, bio, timestamp=time.time()):
    return json.dumps({
        "token": token,
        "bio": {
            "entry": bio,
            "timestamp": str(timestamp) 
        }
    })

def extract_msg(json_msg: str) -> DataTuple:
    try:
        json_obj = json.loads(json_msg)
        if 'response' in json_obj:
            response = json_obj['response']
            return DataTuple(response.get('type', ''), response.get('message', ''), response.get('token', ''))
        else:
            return DataTuple('error', 'Invalid response format', None)
    except json.JSONDecodeError:
        return DataTuple('error', 'JSON cannot be decoded', None)
