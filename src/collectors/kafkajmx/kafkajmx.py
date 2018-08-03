# coding: utf-8
#!/usr/bin/env python
import os
import json
import jpype
import diamond.collector

from collections import namedtuple
from jpype import java, javax
from kazoo.client import KazooClient, KazooState

_zk_client = None
PRECISION = 2
ZK_SESSION_TIMEOUT = 30  # seconds
CLUSTER = ['cluster1', 'cluster2']
KAFKA_ZK_BROKERS_KEY = '/kafka_{cluster}/brokers/ids'
ZKS = 'zk1:2181,zk2:2181,zk3:2181,zk4:2181,zk5:2181'  # zk addresss
USER, PASS = "", ""  # jmx username/password
JVM_PATH = os.path.join(os.environ.get('JAVA_HOME'), 'jre/lib/amd64/server/libjvm.so')
Metric = namedtuple(
    typename='Metric',
    field_names=(
        'name',      
        'jmx_metric',  
        'jmx_attribute',     
    )
)
Metric.__new__.__defaults__ = (None,) * len(Metric._fields)
METRICS = [
    Metric(name='BytesInPerSec', jmx_metric='kafka.server:type=BrokerTopicMetrics,name=BytesInPerSec', jmx_attribute='Count'),
    Metric(name='BytesOutPerSec', jmx_metric='kafka.server:type=BrokerTopicMetrics,name=BytesOutPerSec', jmx_attribute='Count'),
    Metric(name='PartitionCount', jmx_metric='kafka.server:type=ReplicaManager,name=PartitionCount', jmx_attribute='Value'),
    Metric(name='MessagesInPerSec', jmx_metric='kafka.server:type=BrokerTopicMetrics,name=MessagesInPerSec', jmx_attribute='Count'),
    Metric(name='RequestQueueSize', jmx_metric='kafka.network:type=RequestChannel,name=RequestQueueSize', jmx_attribute='Value'),
    Metric(name='LogFlushRateAndTimeMs', jmx_metric='kafka.log:type=LogFlushStats,name=LogFlushRateAndTimeMs', jmx_attribute='Count'),
    Metric(name='OfflinePartitionsCount', jmx_metric='kafka.controller:type=KafkaController,name=OfflinePartitionsCount', jmx_attribute='Value'),
    Metric(name='RequestQueueTimeMsProducer', jmx_metric='kafka.network:type=RequestMetrics,name=RequestQueueTimeMs,request=Produce', jmx_attribute='Count'),
    Metric(name='RequestQueueTimeMsConsumer', jmx_metric='kafka.network:type=RequestMetrics,name=RequestQueueTimeMs,request=FetchConsumer', jmx_attribute='Count'),
    Metric(name='RequestQueueTimeMsFollower', jmx_metric='kafka.network:type=RequestMetrics,name=RequestQueueTimeMs,request=FetchFollower', jmx_attribute='Count'),
]


def get_zk_client():
    global _zk_client
    if _zk_client is None:
        zk = KazooClient(ZKS, timeout=ZK_SESSION_TIMEOUT)
    if zk.state != KazooState.CONNECTED:
        zk.start()
    _zk_client = zk
    return _zk_client


class KafkaJMXCollector(diamond.collector.Collector):
    def get_default_config_help(self):
        config_help = super(KafkaJMXCollector, self).get_default_config_help()
        config_help.update({
            'host': "",
            'port': "",
        })
        return config_help

    def get_default_config(self):
        config = super(KafkaJMXCollector, self).get_default_config()
        config.update({
            'host': '127.0.0.1',
            'port': 2222,
        })
        return config

    def start_jvm(self, jvm_path):
        """Load JVM library and start JVM"""
        try:
            jpype.startJVM(jvm_path)
            return True
        except Exception, e:
            self.log.exception(e) 
            return False

    def poll_metrics(self, metrics):
        """
        :param list metrics: JMX metrics name and attribute
        :rtype: dict
        :return: data returned by JMX request
        """
        self.log.info('start to poll metrics')
        uri = "service:jmx:rmi:///jndi/rmi://%s:%s/jmxrmi" % (self.config['host'], self.config['port'])
        jhash = java.util.HashMap()
        jarray = jpype.JArray(java.lang.String)([USER, PASS])
        jhash.put(javax.management.remote.JMXConnector.CREDENTIALS, jarray)
        jmxurl = javax.management.remote.JMXServiceURL(uri)
        jmxsoc = javax.management.remote.JMXConnectorFactory.connect(jmxurl, jhash)
        connection = jmxsoc.getMBeanServerConnection()
        for metric in metrics:
            try:
                attr = connection.getAttribute(javax.management.ObjectName(metric.jmx_metric), metric.jmx_attribute)
                yield metric.name, attr.value
            except Exception, e:
                self.log.error("Cannot get metric: {jmxobj} - {attribute} from JMX, err {err}".format(
                    jmxobj=metric.jmx_metric, attribute=metric.jmx_attribute, err=e))
                continue

    def collect(self):
        try:
            zk_client = get_zk_client()
            brokers = []
            
            def _get_brokers(cluster):
                k = KAFKA_ZK_BROKERS_KEY.format(cluster=cluster)
                if not zk_client.exists(k):
                    return
                for _id in zk_client.get_children(k):
                    bk = json.loads(zk_client.get("{k}/{id}".format(k=k, id=_id))[0])
                    brokers.append(bk['host'])

            map(_get_brokers, CLUSTER)

            if not self.start_jvm(JVM_PATH):
                self.log.error('Failed to start jvm')
                return 

            for server in brokers:
                for k, v in self.poll_metrics(METRICS):
                    stat = 'stats.gauge.kafka.%s.%s' % (server, k)
                    self.publish_gauge(stat, v, precision=PRECISION)
        except Exception, e:
            self.log.exception(e)
