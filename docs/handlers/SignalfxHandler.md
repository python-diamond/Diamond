<!--This file was generated from the python source
Please edit the source to make changes
-->
SignalfxHandler
====

Send metrics to signalfx

#### Dependencies

 * urllib2


#### Configuration
Enable this handler

 * handers = diamond.handler.httpHandler.SignalfxHandler

 * auth_token = SIGNALFX_AUTH_TOKEN
 * batch_size = [optional | 300 ] will wait for this many requests before
     posting
#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
auth_token |  | Org API token to use when sending metrics | str
batch | 300 | How many to store before sending | int
get_default_config_help |  | get_default_config_help | 
server_error_interval | 120 | How frequently to send repeated server errors | int
url | https://ingest.signalfx.com/v2/datapoint | Where to send metrics | str
