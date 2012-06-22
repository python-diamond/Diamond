import diamond.collector

class ExampleCollector(diamond.collector.Collector):

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        return {
            'path':     'example'
        }

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
