<!--This file was generated from the python source
Please edit the source to make changes
-->
cloudwatchHandler
=====

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
collect_by_instance = True
collect_without_dimension = False
collector = loadavg
metric = 01
name = Avg01
namespace = MachineLoad
unit = None

[[[LoadAvg05]]]
collect_by_instance = True
collect_without_dimension = False
collector = loadavg
metric = 05
name = Avg05
namespace = MachineLoad
unit = None

#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
collect_by_instance | True | Collect metrics for instances separately | bool
collect_without_dimension | False | Collect metrics without dimension | bool
collector | loadavg | Diamond collector name | str
metric | 01 | Diamond metric name | str
name | Avg01 | CloudWatch metric name | str
namespace | MachineLoad | CloudWatch metric namespace | str
region | us-east-1 | AWS region | str
unit | None | CloudWatch metric unit | str
