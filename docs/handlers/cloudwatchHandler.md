<!--This file was generated from the python source
Please edit the source to make changes
-->
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
#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
collector | loadavg |  | str
get_default_config_help |  | get_default_config_help | 
metric | 01 |  | str
name | Avg01 |  | str
namespace | MachineLoad |  | str
region | us-east-1 |  | str
server_error_interval | 120 | How frequently to send repeated server errors | int
unit | None |  | str
