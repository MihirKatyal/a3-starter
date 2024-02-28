import socket
import ds_protocol
import sys
import json

def send(server:str, port:int, username:str, password:str, message:str, bio:str=None):
  '''
  The send function joins a ds server and sends a message, bio, or both

  :param server: The ip address for the ICS 32 DS server.
  :param port: The port where the ICS 32 DS server is accepting connections.
  :param username: The user name to be assigned to the message.
  :param password: The password associated with the username.
  :param message: The message to be sent to the server.
  :param bio: Optional, a bio for the user.
  '''
  try:
    # Establish socket connection
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
      client.connect((server, port))
      print(f'Connected to {server} on port {port}')
            
      # Set up file-like communication channels
      Send = client.makefile('w')
      recv = client.makefile('r')

      # Send join request to the server
      Join = ds_protocol.join(username, password)
      Send.write(Join + '\r\n')
      Send.flush()

    # Receive and process server response for join request
    res = recv.readline()
    srv_msg = ds_protocol.extract_msg(res)  # Make sure this function exists and properly extracts server messages
    if srv_msg['type'] == 'ok':
      tkn = srv_msg['token']  # Adjust these fields based on actual server response structure

