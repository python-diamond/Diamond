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
            'collectTeamDetails':  'calculate details per team',
            'collectChannelDetails': 'calculate details per channel',
            'collectUserDetails':   'calculate details per user',
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
            'collectUserDetails':   True,
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
            self.collectPostStats()
            if self.config['collectTeamDetails']:
                self.collectTeamDetails()
            if self.config['collectChannelDetails']:
                self.collectChannelDetails()
            if self.config['collectUserDetails']:
                self.collectUserDetails()

    def collectUserStats(self):
        cur = self.conn.cursor()
        query = "select count(*) from users where deleteat = 0"
        cur.execute(query)
        self.publishMyCounter("users.count", cur.fetchone()[0])

        cur.execute(query+" and emailverified")
        self.publishMyCounter("users.verified", cur.fetchone()[0])

        query = "select count(*) from sessions where lastactivityat > "
        query += "(extract(epoch from now()) - 3600)*1000"
        cur.execute(query)
        self.publishMyCounter("users.active_in_last_hour", cur.fetchone()[0],
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

    def collectPostStats(self):
        cur = self.conn.cursor()
        query = "select count(*) from posts p, channels c where p.deleteat = 0"
        query += " and p.channelid = c.id and c.teamid <> ''"
        cur.execute(query)
        self.publishMyCounter("posts.in_team.count", cur.fetchone()[0])

        query = "select count(*) from posts p, channels c where p.deleteat = 0"
        query += " and p.channelid = c.id and c.teamid = ''"
        cur.execute(query)
        self.publishMyCounter("posts.direct.count", cur.fetchone()[0])
        cur.close()

    def collectTeamDetails(self):
        cur = self.conn.cursor()
        query = "select t.displayname, count(*) "
        query += "from teams t, teammembers tm, users u "
        query += "where t.id = tm.teamid and tm.userid = u.id and "
        query += "tm.deleteat = 0 group by t.displayname;"
        cur.execute(query)
        for entry in cur.fetchall():
            teamName = entry[0].replace(" ", "_").replace(".", "_")
            self.publishMyCounter("teamdetails."+teamName+".users", entry[1])
        query = "select t.displayname, count(*) "
        query += "from teams t, channels c "
        query += "where t.id = c.teamid and t.deleteat = 0 and c.deleteat = 0 "
        query += "group by t.displayname;"
        cur.execute(query)
        for entry in cur.fetchall():
            teamName = entry[0].replace(" ", "_").replace(".", "_")
            self.publishMyCounter("teamdetails."+teamName+".channels", entry[1])
        query = "select t.displayname, count(*) "
        query += "from teams t, channels c, posts p "
        query += "where t.id = c.teamid and c.id = p.channelid "
        query += "and t.deleteat = 0 and c.deleteat = 0 and p.deleteat = 0"
        query += "group by t.displayname;"
        cur.execute(query)
        for entry in cur.fetchall():
            teamName = entry[0].replace(" ", "_").replace(".", "_")
            self.publishMyCounter("teamdetails."+teamName+".posts", entry[1])
        cur.close()

    def collectChannelDetails(self):
        cur = self.conn.cursor()
        query = "select t.displayname, c.displayname, count(*) "
        query += "from teams t, channels c, channelmembers cm "
        query += "where t.id = c.teamid and c.id = cm.channelid "
        query += "and t.deleteat = 0 and c.deleteat = 0 "
        query += "group by t.displayname, c.displayname;"
        cur.execute(query)
        for entry in cur.fetchall():
            teamName = entry[0].replace(" ", "_").replace(".", "_")
            channelName = entry[1].replace(" ", "_").replace(".", "_")
            metricName = "channeldetails." + teamName + "." + channelName
            metricName += ".users"
            self.publishMyCounter(metricName, entry[2])
        query = "select t.displayname, c.displayname, count(*) "
        query += "from teams t, channels c, posts p "
        query += "where t.id = c.teamid and c.id = p.channelid "
        query += "and t.deleteat = 0 and c.deleteat = 0 and p.deleteat = 0 "
        query += "group by t.displayname, c.displayname;"
        cur.execute(query)
        for entry in cur.fetchall():
            teamName = entry[0].replace(" ", "_").replace(".", "_")
            channelName = entry[1].replace(" ", "_").replace(".", "_")
            metricName = "channeldetails." + teamName + "." + channelName
            metricName += ".posts"
            self.publishMyCounter(metricName, entry[2])

        cur.close()

    def collectUserDetails(self):
        cur = self.conn.cursor()
        query = "select u.username, t.displayname, c.displayname, count(*) "
        query += "from teams t, channels c, posts p, users u where "
        query += "t.id = c.teamid and c.id = p.channelid and u.id = p.userid "
        query += "and t.deleteat = 0 and c.deleteat = 0 and p.deleteat = 0 "
        query += "group by u.username, t.displayname, c.displayname;"
        cur.execute(query)
        for entry in cur.fetchall():
            userName = entry[0].replace(" ", "_").replace(".", "_")
            teamName = entry[1].replace(" ", "_").replace(".", "_")
            channelName = entry[2].replace(" ", "_").replace(".", "_")
            metricName = "userdetails." + userName + "." + teamName + "."
            metricName += channelName + ".posts"
            self.publishMyCounter(metricName, entry[3])
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
