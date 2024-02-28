# dsp_demo.py

import ds_client
server = "168.235.86.101" 
port = 3021  
ds_client.send(server, port, "f21demo", "pwd123", "Hello World!")