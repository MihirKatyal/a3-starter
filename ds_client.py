import socket
import ds_protocol
import sys
import json  

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
            srv_msg = ds_protocol.extract_msg(res)  
            if srv_msg['type'] == 'ok':
                tkn = srv_msg['token']  
                
                # Send post message if provided
                if message:
                    POST = ds_protocol.post(tkn, message)  
                    Send.write(POST + '\r\n')
                    Send.flush()
                    res = recv.readline()  
                    
                # Send bio if provided
                if bio:
                    BIO = ds_protocol.bio(tkn, bio)  
                    Send.write(BIO + '\r\n')
                    Send.flush()
                    res = recv.readline()  
                
                print("Post successfully published!")
            else:
                print(f"Error joining server: {srv_msg.get('message', 'Unknown error')}")
    except Exception as e:
        print(f"ERROR connecting to the server: {e}", sys.exc_info()[0])

# This is the testing block
if __name__ == '__main__':
    SERVER_ADDRESS = '168.235.86.101'
    SERVER_PORT = 3021
    test_username = 'your_test_username'
    test_password = 'your_test_password'
    test_message = 'Hello, DSP!'
    test_bio = 'This is a test bio.'

    print("Testing DSP Client...")
    results = send(SERVER_ADDRESS, SERVER_PORT, test_username, test_password, test_message, test_bio)
    print("Test Results:", results)