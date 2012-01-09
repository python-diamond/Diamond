import MySQLdb
from MySQLdb import MySQLError
import diamond
from pprint import pprint

class MySQLCollector(diamond.collector.Collector):

    def get_stats(self):
        params = self.config.dict()
        if params.has_key('port'):
            params['port'] = int(params['port'])

        for key in ('interval', 'splay', 'path', 'path_prefix', 'publish', 'byte_unit', 'enabled', 'method'):
            del params[key]

        try:
            db = MySQLdb.connect(**params)
        except MySQLError, e:
            self.log.error('Couldnt connect to database %s', e)
            return {}

        self.log.info('Connected to database.')

        cursor = db.cursor()
        cursor.execute('show session status')
        stats = dict(cursor.fetchall())
        db.close()

        return stats

    def collect(self):
        stats = self.get_stats()

        if 'publish' not in self.config:
            self.log.error('Please provide list of keys to publish')
            return

        for k in self.config['publish'].split():
            if k not in stats:
                self.log.error("No such key '%s' available, issue 'show session status' for a full list", k)
            else:
                self.publish(k, stats[k])
                self.log.info("Published %s => %s", k, stats[k])
