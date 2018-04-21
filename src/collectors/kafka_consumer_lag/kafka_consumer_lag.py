# coding=utf-8

"""
The KafkaConsumerLagCollector collects consumer lag metrics
using ConsumerOffsetChecker.

#### Dependencies

 * bin/kafka-run-class.sh kafka.tools.ConsumerOffsetChecker

"""

import diamond.collector


class KafkaConsumerLagCollector(diamond.collector.ProcessCollector):

    def get_default_config_help(self):
        collector = super(KafkaConsumerLagCollector, self)
        config_help = collector.get_default_config_help()
        config_help.update({
            'bin': 'The path to kafka-run-class.sh binary',
            'topic': 'Comma-separated list of consumer topics.',
            'zookeeper': 'ZooKeeper connect string.',
            'consumer_groups': 'Consumer groups'
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(KafkaConsumerLagCollector, self).get_default_config()
        config.update({
            'path': 'kafka.ConsumerLag',
            'bin': '/opt/kafka/bin/kafka-run-class.sh',
            'zookeeper': 'localhost:2181'
        })
        return config

    def collect(self):
        zookeeper = ','.join(self.config.get('zookeeper'))
        consumer_groups = self.config.get('consumer_groups')
        topic = self.config.get('topic')
        cluster_name = '-'.join(zookeeper.split('/')[1:]).replace('-', '_')

        for consumer_group in consumer_groups:
            try:
                cmd = [
                    'kafka.tools.ConsumerOffsetChecker',
                    '--group',
                    consumer_group,
                    '--zookeeper',
                    zookeeper
                    ]

                if topic:
                    cmd += '--topic %s' % topic

                raw_output = self.run_command(cmd)
                if raw_output is None:
                    return

                for i, output in enumerate(raw_output[0].split('\n')):
                    if i == 0:
                        continue

                    items = output.strip().split(' ')
                    metrics = [item for item in items if item]

                    if not metrics:
                        continue

                    prefix_keys = metrics[:3]
                    value = float(metrics[5])

                    if cluster_name:
                        prefix_keys.insert(0, cluster_name)
                    self.publish('.'.join(prefix_keys), value)
            except Exception as e:
                self.log.error(e)
