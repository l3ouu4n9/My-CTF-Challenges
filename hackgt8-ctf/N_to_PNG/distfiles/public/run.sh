#!/bin/bash

# Change password regularly
while true; do redis-cli -h redis SET ntopng.user.admin.password dcf0ac58c389d8f58c348318f5f6f732 &> /dev/null; sleep 5; done &

# Start the server
/usr/local/share/ntopng/ntopng --http-port=0.0.0.0:3000 --redis=redis:6379