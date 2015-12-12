HttpPostHandler
====

Send metrics to a http endpoint via POST

#### Dependencies

 * urllib2


#### Configuration
Enable this handler

 * handlers = diamond.handler.httpHandler.HttpPostHandler

 * url = http://www.example.com/endpoint

#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>batch</td><td>100</td><td>How many to store before sending to the graphite server</td><td>int</td></tr>
<tr><td>get_default_config_help</td><td></td><td>get_default_config_help</td><td></td></tr>
<tr><td>server_error_interval</td><td>120</td><td>How frequently to send repeated server errors</td><td>int</td></tr>
<tr><td>url</td><td>http://localhost/blah/blah/blah</td><td>Fully qualified url to send metrics to</td><td>str</td></tr>
</table>

### This file was generated from the python source
### Please edit the source to make changes

