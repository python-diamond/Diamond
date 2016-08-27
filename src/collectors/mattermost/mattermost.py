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
            'collectTeamDetails':  'should details be calculated per team',
            'collectChannelDetails': 'should details be calculated per channel',
            'collectUserDetails':   'should details be calculated per user',
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
            'collectTeamDetails':  True,
            'collectChannelDetails': True,
            'collectUserDetails':   False,
        })
        # self.log.error("CONFIG "+str(config))
        return config

    def collect(self):
        if self.conn is None:
            self.connect()
        if self.conn is not None:
            self.collectUserStats()
            self.collectTeamStats()
            self.collectChannelStats()
            if self.config['collectTeamDetails']:
                self.collectTeamDetails()

    def collectUserStats(self):
        cur = self.conn.cursor()
        query = "select count(*) from users where deleteat = 0"
        cur.execute(query)
        self.publishMyCounter("users.count", cur.fetchone()[0])

        cur.execute(query+" and emailverified")
        self.publishMyCounter("users.verified", cur.fetchone()[0])

        cur.execute("select count(*) from sessions")
        self.publishMyCounter("users.logged", cur.fetchone()[0],
                              mtype='GAUGE')
        cur.close()

    def collectTeamStats(self):
        cur = self.conn.cursor()
        query = "select count(*) from teams where deleteat = 0"
        cur.execute(query)
        self.publishMyCounter("teams.count", cur.fetchone()[0])

        cur.execute(query+" and allowopeninvite")
        self.publishMyCounter("teams.open", cur.fetchone()[0])
        cur.close()

    def collectChannelStats(self):
        cur = self.conn.cursor()
        query = "select count(*) from channels where deleteat = 0"
        cur.execute(query)
        self.publishMyCounter("channels.count", cur.fetchone()[0])
        cur.close()

    def collectTeamDetails(self):
        cur = self.conn.cursor()
        query = "select t.displayname, count(*) "
        query += "from teams t, teammembers tm, users u "
        query += "where t.id = tm.teamid and tm.userid = u.id and "
        query += "tm.deleteat = 0 group by t.displayname;"
        cur.execute(query)
        for entry in cur.fetchall():
            teamName = entry[0].replace(" ", "_")
            self.publishMyCounter("teamdetails."+teamName+".users", entry[1])
        query = "select t.displayname, count(*) "
        query += "from teams t, channels c "
        query += "where t.id = c.teamid and c.deleteat = 0 "
        query += "group by t.displayname;"
        cur.execute(query)
        for entry in cur.fetchall():
            teamName = entry[0].replace(" ", "_")
            self.publishMyCounter("teamdetails."+teamName+".channels", entry[1])

        cur.close()

    def publishMyCounter(self, metricName, value, mtype='COUNTER'):
        self.log.debug(metricName+"="+str(value))
        self.publish(metricName, value, raw_value=value,
                     precision=0, metric_type=mtype,
                     instance=None)

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
