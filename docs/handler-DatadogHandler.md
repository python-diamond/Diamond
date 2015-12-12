DatadogHandler
====

[Datadog](http://www.datadoghq.com/) is a monitoring service for IT,
Operations and Development teams who write and run applications
at scale, and want to turn the massive amounts of data produced
by their apps, tools and services into actionable insight.

#### Dependencies

  * [dogapi]

#### Configuration

Enable handler

  * handlers = diamond.handler.datadog.DatadogHandler,

  * api_key = DATADOG_API_KEY

  * queue_size = [optional | 1]

#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>api_key</td><td></td><td></td><td>str</td></tr>
<tr><td>get_default_config_help</td><td></td><td>get_default_config_help</td><td></td></tr>
<tr><td>queue_size</td><td></td><td></td><td>str</td></tr>
<tr><td>server_error_interval</td><td>120</td><td>How frequently to send repeated server errors</td><td>int</td></tr>
</table>

### This file was generated from the python source
### Please edit the source to make changes

