import MySQLdb
from MySQLdb import MySQLError
import diamond
import re

class MySQLCollector(diamond.collector.Collector):

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        return {
            'path':     'mysql',
            # Connection settings
            'host':     'localhost',
            'port':     3306,
            'db':       'yourdatabase',
            'user':     'yourusername',
            'passwd':   'yourpassword',
            
            # Which rows of 'SHOW GLOBAL STATUS' you would like to publish.
            # http://dev.mysql.com/doc/refman/5.1/en/show-status.html
            # Leave unset to publish all
            #'publish' : '',
        }

    def get_stats(self):
        params = {}
        metrics = {}

        params['host']   = self.config['host']
        params['port']   = int(self.config['port'])
        params['db']     = self.config['db']
        params['user']   = self.config['user']
        params['passwd'] = self.config['passwd']

        try:
            db = MySQLdb.connect(**params)
        except MySQLError, e:
            self.log.error('Couldnt connect to database %s', e)
            return {}

        self.log.info('Connected to database.')

        cursor = db.cursor()

        cursor.execute('SHOW GLOBAL STATUS')
        stats['status'] = dict(cursor.fetchall())
        for key in stats['status']:
            try:
                metrics[key] = float(stats['status'][key])
            except:
                pass

        db.close()

        return metrics

    def collect(self):
        metrics = self.get_stats()

        for metric_name in metrics:
            metric_value = metrics[metric_name]
            
            if type(metric_value) is not float:
                continue
            
            if 'publish' not in self.config or metric_name in self.config['publish']:
                metric_value = self.derivative(metric_name, metric_value)
                self.publish(metric_name, metric_value)
        else:
            for k in self.config['publish'].split():
                if not metrics.has_key(k):
                    self.log.error("No such key '%s' available, issue 'show global status' for a full list", k)
                else:
                    self.publish(k, metrics[k])
