LibratoHandler
====

[Librato](http://librato.com) is an infrastructure software as a service company
dedicated to delivering beautiful, easy to use tools that make managing your
operations more fun and efficient.

#### Dependencies

 * [librato-metrics](https://github.com/librato/python-librato)

#### Configuration

Enable this handler

 * handlers = diamond.handler.libratohandler.LibratoHandler,

 * user = LIBRATO_USERNAME
 * apikey = LIBRATO_API_KEY

 * queue_max_size = [optional | 300] max measurements to queue before submitting
 * queue_max_interval [optional | 60] @max seconds to wait before submitting
     For best behavior, be sure your highest collector poll interval is lower
     than or equal to the queue_max_interval setting.

 * include_filters = [optional | '^.*'] A list of regex patterns.
     Only measurements whose path matches a filter will be submitted.
     Useful for limiting usage to *only* desired measurements, e.g.
       include_filters = "^diskspace\..*\.byte_avail$", "^loadavg\.01"
       include_filters = "^sockets\.",
                                     ^ note trailing comma to indicate a list

#### Options - [Generic Options](Configuration)

<table><tr><th>Setting</th><th>Default</th><th>Description</th><th>Type</th></tr>
<tr><td>apikey</td><td></td><td></td><td>str</td></tr>
<tr><td>get_default_config_help</td><td></td><td>get_default_config_help</td><td></td></tr>
<tr><td>include_filters</td><td>^.*,</td><td></td><td>list</td></tr>
<tr><td>queue_max_interval</td><td>60</td><td></td><td>int</td></tr>
<tr><td>queue_max_size</td><td>300</td><td></td><td>int</td></tr>
<tr><td>server_error_interval</td><td>120</td><td>How frequently to send repeated server errors</td><td>int</td></tr>
<tr><td>user</td><td></td><td></td><td>str</td></tr>
</table>

### This file was generated from the python source
### Please edit the source to make changes

