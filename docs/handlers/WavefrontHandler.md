<!--This file was generated from the python source
Please edit the source to make changes
-->
WavefrontHandler
====

A handler to send metrics to a Wavefront proxy.  The code is derived
from the OpenTSDB handler, as the two protocols are very similar. Tested
with the Wavefront Test Proxy.

[Wavefront](https://www.wavefront.com/) is a hosted analytics service. It
can accept data in various formats, but has the following native format:

```
<metricName> <metricValue> [<timestamp>] source=<source> [<k1>=<"v1"> ..
                                                          <kn>=<"vn">]
```

where kn=vn are "point tags".  These are key=value pairs which apply to
individual points. You can add point tags in the Handler configuration
stanza:

```
[[WavefrontHandler]]
port = 2878
tags = mytag1=myval1,mytag2=myval2
```

in which case they will be applied to all points the handler sends.

You can also set point tags through the publish() method in your
collector, using the `point_tags` parameter, with a dict as the
argument.

```
self.publish('metric', value, point_tags={'mytag1': 'myval1',
                                          'mytag2': 'myval2',})
```

Both the key and value will automatically be wrapped in soft quotes.

This handler will *not* speak directly to the Wavefront API: that is a
different problem.

#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
format | {Collector}.{Metric} {value} {timestamp} source={host} {tags} |  | str
get_default_config_help |  | get_default_config_help | 
host |  | Wavefront proxy endpoint | str
port | 2878 | port on Wavefront proxy | int
server_error_interval | 120 | How frequently to send repeated server errors | int
tags |  | key=value point tags | str
timeout | 5 |  | int
