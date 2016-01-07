<!--This file was generated from the python source
Please edit the source to make changes
-->
ArchiveHandler
====

Write the collected stats to a locally stored log file. Rotate the log file
every night and remove after 7 days.
#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
days | 7 | How many days to store | int
encoding | None |  | NoneType
get_default_config_help |  | get_default_config_help | 
log_file |  | Path to the logfile | str
propagate | False | Pass handled metrics to configured root logger | bool
server_error_interval | 120 | How frequently to send repeated server errors | int
