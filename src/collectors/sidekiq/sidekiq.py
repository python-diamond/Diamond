# coding=utf-8

"""
Collects sidekiq data from Redis

#### Dependencies

 * redis

"""
from itertools import izip

try:
    import redis
    from redis.sentinel import Sentinel
except ImportError:
    redis = None

import diamond.collector


class SidekiqCollector(diamond.collector.Collector):

    def get_default_config_help(self):
        config_help = super(SidekiqCollector,
                            self).get_default_config_help()
        config_help.update({
            'host': 'Redis hostname',
            'ports': 'Redis ports',
            'password': 'Redis Auth password',
            'databases': 'how many database instances to collect',
            'sentinel_ports': 'Redis sentinel ports',
            'sentinel_name': 'Redis sentinel name',
            'cluster_prefix': 'Redis cluster name prefix'
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(SidekiqCollector, self).get_default_config()
        config.update({
            'path': 'sidekiq',
            'host': 'localhost',
            'ports': '6379',
            'password': None,
            'databases': 16,
            'sentinel_ports': None,
            'sentinel_name': None,
            'cluster_prefix': None
        })
        return config

    def get_master(self, host, port, sentinel_port, sentinel_name):
        """
        :param host: Redis host to send request
        :param port: Redis port to send request
        :param sentinel_port: sentinel_port optional
        :param sentinel_name: sentinel_name optional
        :return: master ip and port
        """
        if sentinel_port and sentinel_name:
            master = Sentinel([(host, sentinel_port)], socket_timeout=1)\
                .discover_master(sentinel_name)
            return master
        return host, port

    def get_redis_client(self):
        """
        :param db: Redis database index
        :return: Redis client
        """
        host = self.config['host']
        ports = self.config['ports']
        sentinel_ports = self.config['sentinel_ports']
        sentinel_name = self.config['sentinel_name']
        password = self.config['password']
        databases = self.config['databases']

        if not isinstance(ports, list):
            ports = [ports]

        if not isinstance(sentinel_ports, list):
            sentinel_ports = [sentinel_ports]

        if sentinel_ports:
            assert len(sentinel_ports) == len(ports)
        else:
            sentinel_ports = [None for _ in xrange(len(ports))]

        for port, sentinel_port in izip(ports, sentinel_ports):
            for db in xrange(0, int(databases)):
                master = self.get_master(
                    host, port, sentinel_port, sentinel_name
                )
                pool = redis.ConnectionPool(
                    host=master[0], port=int(master[1]),
                    password=password, db=db
                )
                yield redis.Redis(connection_pool=pool), port, db

    def collect(self):
        """
        Collect Sidekiq metrics
        :return:
        """
        if redis is None:
            self.log.error('Unable to import module redis')
            return {}

        try:
            for redis_client, port, db in self.get_redis_client():
                try:
                    self.publish_queue_length(redis_client, port, db)
                    self.publish_schedule_length(redis_client, port, db)
                    self.publish_retry_length(redis_client, port, db)
                except Exception as execption:
                    self.log.error(execption)
        except Exception as execption:
            self.log.error(execption)

    def publish_schedule_length(self, redis_client, port, db):
        """
        :param redis_client: Redis client
        :param db: Redis Database index
        :param port: Redis port
        :return: Redis schedule length
        """
        schedule_length = redis_client.zcard('schedule')
        self.__publish(port, db, 'schedule', schedule_length)

    def publish_retry_length(self, redis_client, port, db):
        """
        :param redis_client: Redis client
        :param db: Redis Database index
        :param port: Redis port
        :return: Redis schedule length
        """
        retry_length = redis_client.zcard('retry')
        self.__publish(port, db, 'retry', retry_length)

    def publish_queue_length(self, redis_client, port, db):
        """
        :param redis_client: Redis client
        :param db: Redis Database index
        :param port: Redis port
        :return: Redis queue length
        """
        for queue in redis_client.smembers('queues'):
            queue_length = redis_client.llen('queue:%s' % queue)
            self.__publish(port, db, queue, queue_length)

    def __publish(self, port, db, queue, queue_length):
        """
        :param port: Redis port
        :param db: Redis db index to report
        :param queue: Queue name to report
        :param queue_length: Queue length to report
        :return:
        """
        metric_name_segaments = ['queue']
        cluster = self.config['cluster_prefix']
        if cluster:
            metric_name_segaments.append(cluster)
        metric_name_segaments.append(port)
        metric_name_segaments.append(str(db))
        metric_name_segaments.append(queue)
        self.publish_gauge(
            name='.'.join(metric_name_segaments), value=queue_length
        )
