<!--This file was generated from the python source
Please edit the source to make changes
-->
SentryHandler
====

Diamond handler that check if values are too high or too low, if so send an
alert to a Sentry server

This handler requires the Python module Raven:
http://raven.readthedocs.org/en/latest/index.html

To work this handler need a similar configuration:

[[SentryHandler]]

# Create a new project in Sentry and copy the DSN here:
dsn = http://user:pass@hostname/id

[[[load]]]

name = Load Average
# check for load average of the last 15 minutes
path = loadavg.15
max = 8.5

[[[free_memory]]]

name = Free Memory
path = memory.MemFree
min = 66020000
#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
dsn |  |  | str
get_default_config_help |  | get_default_config_help | 
server_error_interval | 120 | How frequently to send repeated server errors | int
