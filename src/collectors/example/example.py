import diamond.collector

class ExampleCollector(diamond.collector.Collector):
    """
    An example collector that verifies the answer to life, the universe, and everything does not change.
    
    #### Dependencies

    * A sane universe
    
    """

    def get_default_config_help(self):
        config_help = super(ExampleCollector, self).get_default_config_help()
        config_help.update({
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(ExampleCollector, self).get_default_config()
        config.update( {
            'path':     'example'
        } )
        return config

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
