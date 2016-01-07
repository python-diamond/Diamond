<!--This file was generated from the python source
Please edit the source to make changes
-->
HttpPostHandler
====

Send metrics to a http endpoint via POST
#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
batch | 100 | How many to store before sending to the graphite server | int
get_default_config_help |  | get_default_config_help | 
server_error_interval | 120 | How frequently to send repeated server errors | int
url | http://localhost/blah/blah/blah | Fully qualified url to send metrics to | str
