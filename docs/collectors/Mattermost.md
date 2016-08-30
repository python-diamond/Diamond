<!--This file was generated from the python source
Please edit the source to make changes
-->
MattermostCollector
=====

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

 * [Psycopg2](http://initd.org/psycopg/docs/) : for postgresql connectivity (via libpq)


#### Options

Setting | Default | Description | Type
--------|---------|-------------|-----
databaseHost | localhost | the hostname/ip address of the database server | str
databasePort | 5432 | the port on which the database is running | int
databaseUser | mmuser | the user to connect to the datbase (see your config.json) | str
databasePwd | mmuser_password | the password to connect to the datbase (see your config.json) | str
collectTeamDetails | True | collect details for the teams. | bool
collectChannelDetails | True | collect details for the channels. | bool
collectUserDetails | True | collect details for the individual users. | bool


#### Example Output

```
servers.hostname.mattermost.channeldetails.firstTeam.Off-Topic.users
servers.hostname.mattermost.channeldetails.firstTeam.Town_Square.posts
servers.hostname.mattermost.channeldetails.firstTeam.Town_Square.users
servers.hostname.mattermost.channeldetails.firstTeam.channel1.posts
servers.hostname.mattermost.channeldetails.firstTeam.channel1.users
servers.hostname.mattermost.channeldetails.firstTeam.channel2.users
servers.hostname.mattermost.channeldetails.second_team.Off-Topic.users
servers.hostname.mattermost.channeldetails.second_team.Town_Square.users
servers.hostname.mattermost.channeldetails.second_teamOff-Topic.users
servers.hostname.mattermost.channeldetails.second_teamTown_Square.users
servers.hostname.mattermost.channels.count
servers.hostname.mattermost.posts.in_team.count
servers.hostname.mattermost.posts.direct.count
servers.hostname.mattermost.teamdetails.firstTeam.channels
servers.hostname.mattermost.teamdetails.firstTeam.posts
servers.hostname.mattermost.teamdetails.firstTeam.users
servers.hostname.mattermost.teamdetails.second_team.channels
servers.hostname.mattermost.teamdetails.second_team.users
servers.hostname.mattermost.teams.count
servers.hostname.mattermost.teams.open
servers.hostname.mattermost.userdetails.myUserName.firstTeam.Town_Square.posts
servers.hostname.mattermost.userdetails.myUserName.firstTeam.channel1.posts
servers.hostname.mattermost.userdetails.otherUserName.firstTeam.Town_Square.posts
servers.hostname.mattermost.users.active_in_last_hour
servers.hostname.mattermost.users.count
servers.hostname.mattermost.users.verified
```
