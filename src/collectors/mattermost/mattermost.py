# coding=utf-8

"""
Mattermost (https://www.mattermost.org/) is an open source, self-hosted
Slack-alternative. Out of the box it comes with only support for the number
of users and messages on limited historical data.

This collector aims at extracting the data from the Mattermost database, so
you can store it in your favorite metrics backend and do your own processing.

The collector lets you define in what detail you want the counters to be. Be
aware that for large numbers of groups/channels/users, the number of counters
may grow quickly. Also since the collection performs GROUP BY queries for these
cases, running the collection too frequently may have an impact on the
performance of your system.

Mattermost supports both postgresql and mysql. At this moment, the collector
only support postgresql.

#### Dependencies

 * Psycopg2 : for postgresql connectivity

"""

import diamond.collector
import psycopg2


class MattermostCollector(diamond.collector.Collector):

    RETRY = 5

    def __init__(self, *args, **kwargs):
        super(MattermostCollector, self).__init__(*args, **kwargs)
        self.conn = None

    def get_default_config_help(self):
        config_help = super(MattermostCollector,
                            self).get_default_config_help()
        config_help.update({
            'databaseHost':   'location of the server',
            'databasePort':   'port of the server',
            'databaseUser':   'username of the database',
            'databasePwd':    'password of the user',
            'collectGroups':  'should counters be calculated per group',
            'collectChannels': 'should counters be calculated per channel',
            'collectUsers':   'should counters be calculated per user',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(MattermostCollector, self).get_default_config()
        config.update({
            'path':     'mattermost',
            'databaseHost':   'localhost',
            'databasePort':   '5432',
            'databaseUser':   'mmuser',
            'databasePwd':    'mmuser_password',
            'collectGroups':  True,
            'collectChannels': True,
            'collectUsers':   False,
        })
        # self.log.error("CONFIG "+str(config))
        return config

    def collect(self):
        if self.conn is None:
            self.connect()
        if self.conn is not None:
            self.collectUserStats()

    def collectUserStats(self):
        cur = self.conn.cursor()
        query = "select count(*) from users where deleteat = 0"
        cur.execute(query)
        self.publishMyCounter("users.count", cur.fetchone()[0])

        cur.execute(query+" and emailverified")
        self.publishMyCounter("users.verified", cur.fetchone()[0])

    def publishMyCounter(self, metricName, value):
        self.log.debug(metricName+"="+str(value))
        self.publish_counter(metricName, value, time_delta=False)

    def connect(self):
        retry = self.RETRY
        # Attempt to connect to the db
        while retry > 0:
            connectStr = "dbname='mattermost'"
            connectStr += "host='"+self.config['databaseHost']+"' "
            connectStr += "port="+self.config['databasePort']+" "
            connectStr += "user='"+self.config['databaseUser']+"' "
            connectStr += "password='"+self.config['databasePwd']+"' "

            try:
                self.conn = psycopg2.connect(connectStr)
                self.log.info("Connected to Mattermost DB")
                retry = -1
            except Exception as e:
                self.log.error("Cannot connect to "+connectStr+": "+str(e))
                retry -= 1
