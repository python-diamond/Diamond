# Copyright (C) 2009 Brightcove, Inc. All Rights Reserved. No use,
# copying or distribution of this work may be made except in
# accordance with a valid license agreement from Brightcove, Inc. This
# notice must be included on all copies, modifications and derivatives
# of this work.
#
# Brightcove, Inc MAKES NO REPRESENTATIONS OR WARRANTIES ABOUT THE
# SUITABILITY OF THE SOFTWARE, EITHER EXPRESS OR IMPLIED, INCLUDING
# BUT NOT LIMITED TO THE IMPLIED WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE, OR NON-INFRINGEMENT. Brightcove
# SHALL NOT BE LIABLE FOR ANY DAMAGES SUFFERED BY LICENSEE AS A RESULT
# OF USING, MODIFYING OR DISTRIBUTING THIS SOFTWARE OR ITS
# DERIVATIVES.
#
# "Brightcove" is a trademark of Brightcove, Inc.

import diamond.collector

class ExampleCollector(diamond.collector.Collector):
    
    def collect(self):
        """
        Overrides the Collector.collect method
        """

        # Set Metric Name
        metric_name = "my.example.metric"
        # Set Metric Value
        metric_value = 42

        # Publish Metric
        self.publish(metric_name, metric_value)
