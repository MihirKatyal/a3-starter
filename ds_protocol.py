import json
from collections import namedtuple

# Definitions for response data structures
DataTuple = namedtuple('DataTuple', ['type', 'message', 'token'])
ErrorTuple = namedtuple('ErrorTuple', ['type', 'message', 'token'])

def join(username, password):
    """Create a join request in JSON format."""
    return json.dumps({
        "join": {
            "username": username,
            "password": password,
            "token": ""  # Assuming initial token is empty for join requests
        }
    })

def post(token, message):
    """Create a post request in JSON format."""
    return json.dumps({
        "token": token,
        "post": {
            "entry": message,
            "timestamp": ""  # Server might fill in the timestamp; verify with your server's API
        }
    })

def bio(token, bio):
    """Create a bio request in JSON format."""
    return json.dumps({
        "token": token,
        "bio": {
            "entry": bio,
            "timestamp": ""  # Same note on timestamp as above
        }
    })

def extract_json(json_msg: str) -> DataTuple:
    """Parse a JSON string and convert it to a DataTuple object."""
    try:
        json_obj = json.loads(json_msg)
        # Default values if not found
        response_type = json_obj.get('type', 'unknown')
        message = json_obj.get('message', '')
        token = json_obj.get('token', None)
        return DataTuple(response_type, message, token)
    except json.JSONDecodeError:
        print("JSON cannot be decoded.")
        return DataTuple('json_error', 'JSON cannot be decoded', None)

def extract_msg(json_msg: str) -> ErrorTuple:
    """Parse server response from a JSON string."""
    try:
        json_obj = json.loads(json_msg)
        if 'response' in json_obj:  # Correct response structure
            response_type = json_obj['response'].get('type', 'unknown')
            message = json_obj['response'].get('message', '')
            token = json_obj['response'].get('token', None)
            return DataTuple(response_type, message, token)  # Returns a DataTuple for valid responses
        else:
            return ErrorTuple('error', 'Unexpected response format', None)  # Return ErrorTuple for unexpected structure
    except json.JSONDecodeError:
        print("JSON cannot be decoded.")
        return ErrorTuple('error', 'Invalid JSON format', None)  # Return ErrorTuple for JSON decoding errors
