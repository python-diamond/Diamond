<!--This file was generated from the python source
Please edit the source to make changes
-->
LibratoHandler
====

[Librato](http://librato.com) is an infrastructure software as a service company
dedicated to delivering beautiful, easy to use tools that make managing your
operations more fun and efficient.

#### Dependencies

 * [librato-metrics](https://github.com/librato/python-librato)


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
apikey |  | Librato API key | str
apply_metric_prefix | False | Allow diamond to apply metric prefix | bool
get_default_config_help |  | get_default_config_help | 
include_filters | ^.*, | A list of regex patterns. Only measurements whose path matches a filter will be submitted. Useful for limiting usage to *only* desired measurements, e.g. `"^diskspace\..*\.byte_avail$", "^loadavg\.01"` or `"^sockets\.",` (note trailing comma to indicate a list) | list
queue_max_interval | 60 | Max seconds to wait before submitting. For best behavior, be sure your highest collector poll interval is lower than or equal to the queue_max_interval setting. | int
queue_max_size | 300 | Max measurements to queue before submitting | int
server_error_interval | 120 | How frequently to send repeated server errors | int
user |  | Librato username | str
