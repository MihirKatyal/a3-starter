import ds_client

server = "168.235.86.101 "  # replace with actual server ip address
port = 3021   # replace with actual port

# Add more realistic credentials and messages
demo_results = ds_client.send(server, port, "demo_user", "demo_pass", "Hello, this is a demo message!", "This is a demo bio.")
print("Test Results:", demo_results)