# coding=utf-8

"""
Collects Cassandra JMX metrics from the Jolokia Agent.  Extends the
JolokiaCollector to interpret Histogram beans with information about the
distribution of request latencies.

#### Example Configuration
CassandraJolokiaCollector uses a regular expression to determine which
attributes represent histograms. This regex can be overridden by providing a
`histogram_regex` in your configuration.  You can also override `percentiles` to
collect specific percentiles from the histogram statistics.  The format is shown
below with the default values.

CassandraJolokiaCollector.conf

```
    percentiles '50,95,99'
    histogram_regex '.*HistogramMicros$'
```
"""

from jolokia import JolokiaCollector
import math
import string
import re


class CassandraJolokiaCollector(JolokiaCollector):
    # override to allow setting which percentiles will be collected

    def get_default_config_help(self):
        config_help = super(CassandraJolokiaCollector,
                            self).get_default_config_help()
        config_help.update({
            'percentiles':
            'Comma separated list of percentiles to be collected '
            '(e.g., "50,95,99").',
            'histogram_regex':
            'Filter to only process attributes that match this regex'
        })
        return config_help

    # override to allow setting which percentiles will be collected
    def get_default_config(self):
        config = super(CassandraJolokiaCollector, self).get_default_config()
        config.update({
            'percentiles': ['50', '95', '99'],
            'histogram_regex': '.*HistogramMicros$'
        })
        return config

    def __init__(self, *args, **kwargs):
        super(CassandraJolokiaCollector, self).__init__(*args, **kwargs)
        self.offsets = self.create_offsets(91)
        self.update_config(self.config)

    def update_config(self, config):
        if 'percentiles' in config:
            self.percentiles = map(int, config['percentiles'])
        if 'histogram_regex' in config:
            self.histogram_regex = re.compile(config['histogram_regex'])

    # override: Interpret beans that match the `histogram_regex` as histograms,
    # and collect percentiles from them.
    def interpret_bean_with_list(self, prefix, values):
        if not self.histogram_regex.match(prefix):
            return

        buckets = values
        offsets = self.offsets
        for percentile in self.percentiles:
            value = self.compute_percentile(offsets, buckets, percentile)
            cleaned_key = self.clean_up("%s.p%s" % (prefix, percentile))
            self.publish(cleaned_key, value)

    # Adapted from Cassandra docs:
    # https://bit.ly/13M5JPE
    # The index corresponds to the x-axis in a histogram.  It represents buckets
    # of values, which are a series of ranges. Each offset includes the range of
    # values greater than the previous offset and less than or equal to the
    # current offset. The offsets start at 1 and each subsequent offset is
    # calculated by multiplying the previous offset by 1.2, rounding up, and
    # removing duplicates. The offsets can range from 1 to approximately 25
    # million, with less precision as the offsets get larger.
    def compute_percentile(self, offsets, buckets, percentile_int):
        non_zero_points_sum = sum(buckets)
        if non_zero_points_sum is 0:
            return 0
        middle_point_index = math.floor(
            non_zero_points_sum * (percentile_int / float(100)))

        points_seen = 0
        for index, bucket in enumerate(buckets):
            points_seen += bucket
            if points_seen >= middle_point_index:
                return round((offsets[index] - offsets[index - 1]) / 2)

    # Returns a list of offsets for `n` buckets.
    def create_offsets(self, bucket_count):
        last_num = 1
        offsets = [last_num]

        for index in range(bucket_count):
            next_num = round(last_num * 1.2)
            if next_num == last_num:
                next_num += 1
            offsets.append(next_num)
            last_num = next_num

        return offsets
