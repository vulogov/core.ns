#!/bin/sh

# We are executing command "start" which daemonize application and run the main event LOOP
# +daemonize - telling application that we are intending to go background
# +system - will run /sbin/loop in a daemon
# -system - will run /bin/loop in a daemon

python examples/example_2.py --appname abc --listen aaa@127.0.0.1:22334 +truename --hostname abc --bootstrap osfs://examples --conf test_example.cfg start +daemonize +system
