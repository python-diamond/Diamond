cloudwatchHandler
====

Output the collected values to AWS CloudWatch

Automatically adds the InstanceId Dimension

#### Dependencies

 * [boto](http://boto.readthedocs.org/en/latest/index.html)

#### Configuration

Enable this handler

 * handers = diamond.handler.cloudwatch.cloudwatchHandler

Example Config:

[[cloudwatchHandler]]
region = us-east-1

[[[LoadAvg01]]]
collector = loadavg
metric = 01
namespace = MachineLoad
name = Avg01
unit = None

[[[LoadAvg05]]]
collector = loadavg
metric = 05
namespace = MachineLoad
name = Avg05
unit = None
#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>collector</td><td>loadavg</td><td></td><td>str</td></tr>
<tr><td>get_default_config_help</td><td></td><td>get_default_config_help</td><td></td></tr>
<tr><td>metric</td><td>01</td><td></td><td>str</td></tr>
<tr><td>name</td><td>Avg01</td><td></td><td>str</td></tr>
<tr><td>namespace</td><td>MachineLoad</td><td></td><td>str</td></tr>
<tr><td>region</td><td>us-east-1</td><td></td><td>str</td></tr>
<tr><td>server_error_interval</td><td>120</td><td>How frequently to send repeated server errors</td><td>int</td></tr>
<tr><td>unit</td><td>None</td><td></td><td>str</td></tr>
</table>

### This file was generated from the python source
### Please edit the source to make changes

