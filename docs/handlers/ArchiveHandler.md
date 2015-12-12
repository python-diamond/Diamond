ArchiveHandler
====

Write the collected stats to a locally stored log file. Rotate the log file
every night and remove after 7 days.
#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>days</td><td>7</td><td>How many days to store</td><td>int</td></tr>
<tr><td>encoding</td><td>None</td><td></td><td>NoneType</td></tr>
<tr><td>get_default_config_help</td><td></td><td>get_default_config_help</td><td></td></tr>
<tr><td>log_file</td><td></td><td>Path to the logfile</td><td>str</td></tr>
<tr><td>propagate</td><td>False</td><td>Pass handled metrics to configured root logger</td><td>bool</td></tr>
<tr><td>server_error_interval</td><td>120</td><td>How frequently to send repeated server errors</td><td>int</td></tr>
</table>

### This file was generated from the python source
### Please edit the source to make changes

