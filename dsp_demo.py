import ds_client

server = "168.235.86.101"
port = 3021
username = "f21demo"  
password = "pwd123"  

# Test sending a message and/or bio
ds_client.send(server, port, username, password, "This is a test message.", "This is a test bio.")
