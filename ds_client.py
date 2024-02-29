import socket
import ds_protocol
import time


def send(server:str, port:int, username:str, password:str, message:str=None, bio:str=None):
    """
    The send function joins a ds server and sends a message, bio, or both

    :param server: The ip address for the ICS 32 DS server.
    :param port: The port where the ICS 32 DS server is accepting connections.
    :param username: The user name to be assigned to the message.
    :param password: The password associated with the username.
    :param message: The message to be sent to the server.
    :param bio: Optional, a bio for the user.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((server, port))

        while True:
            join_str = f'{{"join": {{"username": "{username}","password": "{password}","token":""}}}}'
            send = client.makefile('w')
            recv = client.makefile('r')

            send.write(join_str + '\r\n')
            send.flush()

            resp = recv.readline()

            decoded_resp = ds_protocol.extract_json(resp)

            if decoded_resp[1] == "error":
                print(decoded_resp[0])
                return False

            user_token = decoded_resp[1]
            curr_time = time.time()
            if bio:
                bio_str = f'{{"token": "{user_token}", "bio": {{"entry": "{bio}", "timestamp": "{curr_time}"}}}}'
                send_bio = client.makefile('w')
                send_bio.write(bio_str + '\r\n')
                send_bio.flush()
                new_recv = client.makefile('r')
                new_recv = new_recv.readline()
                print(new_recv)

            if message:
                post_str = f'{{"token": "{user_token}", "post": {{"entry": "{message}", "timestamp": "{curr_time}"}}}}'
                send_post = client.makefile('w')
                send_post.write(post_str + '\r\n')
                send_post.flush()
                new_recv = client.makefile('r')
                new_recv = new_recv.readline()
                print(new_recv)
            return True