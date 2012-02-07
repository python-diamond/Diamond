#!/usr/bin/python
import psycopg2
import sys
import diamond.collector

class PostgresqlCollector(diamond.collector.Collector):

    def collect(self):

        self.conn_string = "host=%s user=%s password=%s port=%s" % (
                self.config['host'],
                self.config['user'],
                self.config['password'],
                self.config['port']
                )

        try:
            self.conn = psycopg2.connect(self.conn_string)
            self.cursor = self.conn.cursor()
        except:
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            sys.exit("Database connection failed!\n ->%s" % (exceptionValue))

        # Statistics
        try:
            self.cursor.execute("SELECT pg_stat_database.*, pg_database_size(pg_database.datname) AS size \
                    FROM pg_database JOIN pg_stat_database ON pg_database.datname = pg_stat_database.datname \
                    WHERE pg_stat_database.datname \
                    NOT IN ('template0','template1','postgres')")
            stats = self.cursor.fetchall()
        except:
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            sys.exit("Database connection failed!\n ->%s" % (exceptionValue))

        # Connections
        try:
            self.cursor.execute("SELECT datname, count(datname) \
                    FROM pg_stat_activity GROUP BY pg_stat_activity.datname;")
            connections = self.cursor.fetchall()
        except:
            exceptionType, exceptionValue, exceptionTraceback = sys.exc_info()
            sys.exit("Database connection failed!\n ->%s" % (exceptionValue))

        ret = {}
        for stat in stats:
            info                    = {}
            info['numbackends']     = stat[2]
            info['xact_commit']     = stat[3]
            info['xact_rollback']   = stat[4]
            info['blks_read']       = stat[5]
            info['blks_hit']        = stat[6]
            info['tup_returned']    = stat[7]
            info['tup_fetched']     = stat[8]
            info['tup_inserted']    = stat[9]
            info['tup_updated']     = stat[10]
            info['tup_deleted']     = stat[11]
            info['conflicts']       = stat[12]
            info['size']            = stat[14]

            database                = stat[1]
            ret[database]           = info


        for database in ret:
            for (metric, value) in info.items():
                self.publish("%s.database.%s" % (database.replace("_", "."), metric), value)

        for (database, connection) in connections:
            self.publish("%s.database.connections" % (database.replace("_", ".")), value)

        self.cursor.close()
        self.conn.close()
