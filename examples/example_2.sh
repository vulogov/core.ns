#!/bin/sh
# In this example we are demonstrating how you can pass configuration information
# to core.NS
# Default keyword --conf can be used many times in default and on command level
# in this configuration keyword you are passing name of the configuration files
# Default keyword --bootstrap can be used many times on default level. Using this keyword you can pass
# FS locations of your configuration files, which could be locations on local filesystem
# such as
# 1. osfs://PATH
# 2. ftp://ftp.example.org/PATH
# 3. http://www.example.org/PATH
python examples/example_2.py --listen aaa@127.0.0.1:22334 +truename --bootstrap osfs://examples --conf a --conf test_example.cfg c --conf ccc d e
