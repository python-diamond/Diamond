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
collect_by_instance = True
collect_without_dimension = False

[[[LoadAvg05]]]
collector = loadavg
metric = 05
namespace = MachineLoad
name = Avg05
unit = None
collect_by_instance = True
collect_without_dimension = False
#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
region | us-east-1 |  | str
collector | loadavg |  | str
metric | 01 |  | str
name | Avg01 |  | str
namespace | MachineLoad |  | str
unit | None |  | str
collect_by_instance | True | Collect metrics for instances separately | bool
collect_without_dimension | False | Collect metrics without dimension | bool
