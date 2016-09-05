from test import CollectorTestCase, get_collector_config
from mock import Mock, patch
import mattermost as mod

from mattermost import MattermostCollector


# These two methods are used for overriding the TSDBHandler._connect method.
# Please check the Test class' setUp and tearDown methods
def fake_connect(self):
    # used for 'we can connect' tests
    m = Mock()
    self.conn = m
    self.cursor = Mock()
    self.conn.cursor = MattermostDbCursorFake
    if '__sockets_created' not in self.config:
        self.config['__sockets_created'] = [m]
    else:
        self.config['__sockets_created'].append(m)


def fake_bad_connect(self):
    # used for 'we can not connect' tests
    self.socket = None


# Fake the queries sent to the mattermost DB
class MattermostDbCursorFake:
    queries = {}
    queries['select count(*) from users where deleteat = 0'] = [42]
    queries['select count(*) from users where deleteat = 0 ' +
            'and emailverified'] = [41]
    queries['select count(distinct userid) from posts where createat > ' +
            '(extract(epoch from now()) - 3600)*1000'] = [7]
    queries['select count(*) from teams where deleteat = 0'] = [5]
    queries['select count(*) from teams where deleteat = 0 and ' +
            'allowopeninvite'] = [4]
    queries['select count(*) from channels where deleteat = 0'] = [3]
    queries['select count(*) from posts p, channels c where p.deleteat = 0' +
            ' and p.channelid = c.id and c.teamid <> \'\''] = [176]
    queries['select count(*) from posts p, channels c where p.deleteat = 0' +
            ' and p.channelid = c.id and c.teamid = \'\''] = [350]
    queries['select t.displayname, count(*) ' +
            'from teams t, teammembers tm, users u ' +
            'where t.id = tm.teamid and tm.userid = u.id and tm.deleteat = 0 ' +
            'group by t.displayname;'] = [['team1', 24], ['team2', 36]]
    queries['select t.displayname, count(*) from teams t, channels c ' +
            'where t.id = c.teamid and t.deleteat = 0 and c.deleteat = 0 ' +
            'group by t.displayname;'] = [['team1', 4], ['team2', 6]]
    queries['select t.displayname, count(*) ' +
            'from teams t, channels c, posts p where t.id = c.teamid and ' +
            'c.id = p.channelid and t.deleteat = 0 and c.deleteat = 0 and ' +
            'p.deleteat = 0 group by t.displayname;'] = [['team1', 74],
                                                         ['team2', 76]]
    queries['select t.displayname, c.displayname, count(*) ' +
            'from teams t, channels c, channelmembers cm ' +
            'where t.id = c.teamid and c.id = cm.channelid and t.deleteat = ' +
            '0 and c.deleteat = 0 group by t.displayname, ' +
            'c.displayname;'] = [['team1', 'channel1', 27],
                                 ['team1', 'channel2', 8],
                                 ['team2', 'channel1', 19]]
    queries['select t.displayname, c.displayname, count(*) ' +
            'from teams t, channels c, posts p ' +
            'where t.id = c.teamid and c.id = p.channelid and t.deleteat = ' +
            '0 and c.deleteat = 0 and p.deleteat = 0 group by t.displayname, ' +
            'c.displayname;'] = [['team1', 'channel1', 100],
                                 ['team1', 'channel2', 6],
                                 ['team2', 'channel1', 20]]
    queries['select u.username, t.displayname, c.displayname, count(*) ' +
            'from teams t, channels c, posts p, users u ' +
            'where t.id = c.teamid and c.id = p.channelid and u.id = ' +
            'p.userid and t.deleteat = 0 and c.deleteat = 0 and p.deleteat ' +
            '= 0 group by u.username, t.displayname, ' +
            'c.displayname;'] = [['user1', 'team1', 'channel1', 47],
                                 ['user1', 'team1', 'channel2', 2],
                                 ['user2', 'team1', 'channel1', 27],
                                 ['user.with.points', 'team1', 'channel1', 19],
                                 ['user with space', 'team2', 'channel1', 32]]

    queries['select u.username, \'no_team\' , \'no_channel\', count(*) ' +
            'from  channels c, posts p, users u where \'\' = c.teamid and ' +
            'c.id = p.channelid and u.id = p.userid and  c.deleteat = 0 and ' +
            'p.deleteat = 0 group by u.username' +
            ';'] = [['user1', 'no_team', 'no_channel', 63],
                    ['user2', 'no_team', 'no_channel', 21],
                    ['user.with.points', 'no_team', 'no_channel', 44],
                    ['user with space', 'no_team', 'no_channel', 56]]

    def execute(self, query):
        self.result = self.queries[query]

    def fetchone(self):
        return self.result

    def fetchall(self):
        return self.result

    def close(self):
        self


class TestMattermostCollector(CollectorTestCase):

    def setUp(self):
        config = get_collector_config('MattermostCollector', {})
        mod.MattermostCollector.connect = fake_connect
        self.collector = MattermostCollector(config, None)

    def test_import(self):
        self.assertTrue(MattermostCollector)

    @patch.object(MattermostCollector, 'publish')
    def testDefault(self, publish_mock):
        self.collector.collect()

        metrics = {
            'users.count': 42,
            'users.verified': 41,
            'users.active_in_last_hour': 7,
            'teams.count': 5,
            'teams.open': 4,
            'channels.count': 3,
            'posts.in_team.count': 176,
            'posts.direct.count': 350,
            'teamdetails.team1.users': 24,
            'teamdetails.team2.users': 36,
            'teamdetails.team1.channels': 4,
            'teamdetails.team2.channels': 6,
            'teamdetails.team1.posts': 74,
            'teamdetails.team2.posts': 76,
            'channeldetails.team1.channel1.users': 27,
            'channeldetails.team1.channel2.users': 8,
            'channeldetails.team2.channel1.users': 19,
            'channeldetails.team1.channel1.posts': 100,
            'channeldetails.team1.channel2.posts': 6,
            'channeldetails.team2.channel1.posts': 20,
            'userdetails.user1.team1.channel1.posts': 47,
            'userdetails.user1.team1.channel2.posts': 2,
            'userdetails.user_with_points.team1.channel1.posts': 19,
            'userdetails.user_with_space.team2.channel1.posts': 32,
            'userdetails.user1.no_team.no_channel.posts': 63,
            'userdetails.user2.no_team.no_channel.posts': 21,
            'userdetails.user_with_points.no_team.no_channel.posts': 44,
            'userdetails.user_with_space.no_team.no_channel.posts': 56,
            }
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(MattermostCollector, 'publish')
    def testMinimal(self, publish_mock):
        self.collector.config['collectTeamDetails'] = False
        self.collector.config['collectChannelDetails'] = False
        self.collector.config['collectUserDetails'] = False
        self.collector.collect()

        metrics = {
            'users.count': 42,
            'users.verified': 41,
            'users.active_in_last_hour': 7,
            'teams.count': 5,
            'teams.open': 4,
            'channels.count': 3,
            'posts.in_team.count': 176,
            'posts.direct.count': 350,
            }
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(MattermostCollector, 'publish')
    def testOnlyTeam(self, publish_mock):
        self.collector.config['collectTeamDetails'] = True
        self.collector.config['collectChannelDetails'] = False
        self.collector.config['collectUserDetails'] = False
        self.collector.collect()

        metrics = {
            'users.count': 42,
            'users.verified': 41,
            'users.active_in_last_hour': 7,
            'teams.count': 5,
            'teams.open': 4,
            'channels.count': 3,
            'posts.in_team.count': 176,
            'posts.direct.count': 350,
            'teamdetails.team1.users': 24,
            'teamdetails.team2.users': 36,
            'teamdetails.team1.channels': 4,
            'teamdetails.team2.channels': 6,
            'teamdetails.team1.posts': 74,
            'teamdetails.team2.posts': 76,
            }
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(MattermostCollector, 'publish')
    def testOnlyChannel(self, publish_mock):
        self.collector.config['collectTeamDetails'] = False
        self.collector.config['collectChannelDetails'] = True
        self.collector.config['collectUserDetails'] = False
        self.collector.collect()

        metrics = {
            'users.count': 42,
            'users.verified': 41,
            'users.active_in_last_hour': 7,
            'teams.count': 5,
            'teams.open': 4,
            'channels.count': 3,
            'posts.in_team.count': 176,
            'posts.direct.count': 350,
            'channeldetails.team1.channel1.users': 27,
            'channeldetails.team1.channel2.users': 8,
            'channeldetails.team2.channel1.users': 19,
            'channeldetails.team1.channel1.posts': 100,
            'channeldetails.team1.channel2.posts': 6,
            'channeldetails.team2.channel1.posts': 20,
            }
        self.assertPublishedMany(publish_mock, metrics)

    @patch.object(MattermostCollector, 'publish')
    def testOnlyUser(self, publish_mock):
        self.collector.config['collectTeamDetails'] = False
        self.collector.config['collectChannelDetails'] = False
        self.collector.config['collectUserDetails'] = True
        self.collector.collect()

        metrics = {
            'users.count': 42,
            'users.verified': 41,
            'users.active_in_last_hour': 7,
            'teams.count': 5,
            'teams.open': 4,
            'channels.count': 3,
            'posts.in_team.count': 176,
            'posts.direct.count': 350,
            'userdetails.user1.team1.channel1.posts': 47,
            'userdetails.user1.team1.channel2.posts': 2,
            'userdetails.user_with_points.team1.channel1.posts': 19,
            'userdetails.user_with_space.team2.channel1.posts': 32,
            'userdetails.user1.no_team.no_channel.posts': 63,
            'userdetails.user2.no_team.no_channel.posts': 21,
            'userdetails.user_with_points.no_team.no_channel.posts': 44,
            'userdetails.user_with_space.no_team.no_channel.posts': 56,
            }
        self.assertPublishedMany(publish_mock, metrics)
