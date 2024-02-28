import socket
import ds_protocol
import sys
import json  # Make sure to import json if it's used in your ds_protocol module

def send(server: str, port: int, username: str, password: str, message: str, bio: str = None):
    try:
        # Establish connection with the server
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
            client.connect((server, port))
            print(f"Client connected to {server} on port {port}")
            
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
                
                # Send post message if provided
                if message:
                    POST = ds_protocol.post(tkn, message)  # Adjust parameters according to your protocol
                    Send.write(POST + '\r\n')
                    Send.flush()
                    res = recv.readline()  # Consider processing this response as well
                    
                # Send bio if provided
                if bio:
                    BIO = ds_protocol.bio(tkn, bio)  # Adjust parameters according to your protocol
                    Send.write(BIO + '\r\n')
                    Send.flush()
                    res = recv.readline()  # Consider processing this response as well
                
                print("Post successfully published!")
            else:
                print(f"Error joining server: {srv_msg.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"ERROR connecting to the server: {e}", sys.exc_info()[0])
