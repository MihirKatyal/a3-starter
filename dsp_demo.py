# dsp_demo.py

import ds_client
server = "127.0.0.1" # replace with actual server ip address
port = 8080 # replace with actual port
# Add more realistic credentials and messages
demo_results = ds_client.send(server, port, "demo_user", "demo_pass", "Hello, this is a demo message!", "This is a demo bio.")
print("Test Results:", demo_results)