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
            join_request = ds_protocol.join(username, password)
            Send.write(join_request + '\r\n')
            Send.flush()

            # Receive and process server response for join request
            join_response = recv.readline()
            srv_msg = ds_protocol.extract_msg(join_response)  
            if srv_msg.type == 'ok':  
                token = srv_msg.token
                
                # Initialize a result dictionary
                results = {'join': 'Success', 'post': None, 'bio': None}
                
                # Send post message if provided
                if message:
                    post_request = ds_protocol.post(token, message)
                    Send.write(post_request + '\r\n')
                    Send.flush()
                    post_response = recv.readline()
                    post_response_msg = ds_protocol.extract_msg(post_response) 
                    results['post'] = 'Success' if post_response_msg.type == 'ok' else 'Failed'

                # Send bio if provided
                if bio:
                    bio_request = ds_protocol.bio(token, bio)
                    Send.write(bio_request + '\r\n')
                    Send.flush()
                    bio_response = recv.readline()
                    bio_response_msg = ds_protocol.extract_msg(bio_response)  
                    results['bio'] = 'Success' if bio_response_msg.type == 'ok' else 'Failed'
                
                return results  
            else:
                print(f"Error joining server: {srv_msg.message}")
                return {'join': 'Failed'}
    except Exception as e:
        print(f"ERROR connecting to the server: {e}", sys.exc_info())
        return {'error': str(e)}


# This is the testing block
if __name__ == '__main__':
    SERVER_ADDRESS = '168.235.86.101'
    SERVER_PORT = 3021
    test_username = 'f21demo' 
    test_password = 'pwd123'  
    test_message = 'Hello, DSP!'
    test_bio = 'This is a test bio.'

    print("Testing DSP Client...")
    results = send(SERVER_ADDRESS, SERVER_PORT, test_username, test_password, test_message, test_bio)
    print("Test Results:", results)

