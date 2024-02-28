import socket
import ds_protocol
import sys

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
            srv_msg = ds_protocol.extract_msg(res)  # This should return a namedtuple
            if srv_msg.type == 'ok':  
                tkn = srv_msg.token
                
                # Initialize a result dictionary
                results = {'join': 'Success', 'post': None, 'bio': None}
                
                # Send post message if provided
                if message:
                    POST = ds_protocol.post(tkn, message)
                    Send.write(POST + '\r\n')
                    Send.flush()
                    res = recv.readline()
                    post_response = ds_protocol.extract_msg(res)  #  expecting a namedtuple
                    results['post'] = 'Success' if post_response.type == 'ok' else 'Failed'

                # Send bio if provided
                if bio:
                    BIO = ds_protocol.bio(tkn, bio)
                    Send.write(BIO + '\r\n')
                    Send.flush()
                    res = recv.readline()
                    bio_response = ds_protocol.extract_msg(res)  #  again for bio response
                    results['bio'] = 'Success' if bio_response.type == 'ok' else 'Failed'
                
                return results  # Returning the results dictionary
            else:
                print(f"Error joining server: {srv_msg.message}")
                return {'join': 'Failed'}
    except Exception as e:
        print(f"ERROR connecting to the server: {e}", sys.exc_info())
        return {'error': str(e)}