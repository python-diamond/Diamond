Customizing a collector
===

Diamond collectors run within the diamond process and collect metrics that can
be published to a graphite server.

Collectors are subclasses of diamond.collector.Collector. In their simplest
form, they need to implement a single method called "collect".

```
    import diamond.collector

    class ExampleCollector(diamond.collector.Collector):

        def collect(self):
            # Set Metric Name
            metric_name = "my.example.metric"

            # Set Metric Value
            metric_value = 42

            # Publish Metric
            self.publish(metric_name, metric_value)
```
To run this collector in test mode you can invoke the diamond server with the
-r option and specify the collector path.

```
diamond -f -r full/path/to/ExampleCollector.py -c conf/diamond.conf.example
```

running diamond in the foreground (-f) while logging to stdout (-l) is a good way to quickly see if a custom collector is unable to load.

```
diamond -f -l
```

For detailed description and example please take a look at the example collector in the Collectors Directory.

Please note that not all collectors will be added to the `PYTHONPATH`, depending on configuration, so if you
need to import another collector in your code, please add it to the path yourself:

```
# example: add the proc collector to the path
sys.path.insert(0, '/path/to/diamond/collectors/proc')
```

If your collector is installed with the rest of the diamond collectors, you should do this:

```
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)),
                                'proc'))
```