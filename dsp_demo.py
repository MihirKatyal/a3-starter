# dsp_demo.py

import ds_client
server = "127.0.0.1" # replace with actual server ip address
port = 8080 # replace with actual port
ds_client.send(server, port, "f21demo", "pwd123", "Hello World!")