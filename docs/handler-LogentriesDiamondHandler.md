LogentriesDiamondHandler
====

[Logentries: Log Management & Analytics Made Easy ](https://logentries.com/).
Send Diamond stats to your Logentries Account where you can monitor and alert
based on data in real time.

#### Dependencies


#### Configuration

Enable this handler

 * handers = diamond.handler.logentries.LogentriesDiamondHandler

 * log_token = [Your Log Token](https://logentries.com/doc/input-token/)

 * queue_size = Integer value


#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>get_default_config_help</td><td></td><td>get_default_config_help</td><td></td></tr>
<tr><td>log_token</td><td></td><td></td><td>str</td></tr>
<tr><td>queue_size</td><td>100</td><td></td><td>int</td></tr>
<tr><td>server_error_interval</td><td>120</td><td>How frequently to send repeated server errors</td><td>int</td></tr>
</table>

### This file was generated from the python source
### Please edit the source to make changes

