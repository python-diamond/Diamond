# coding=utf-8

"""
Insert the collected values into a mysql table
"""

from handler import Handler
import MySQLdb


class MySQLHandler(Handler):
    """
    Implements the abstract Handler class, sending data to a mysql table
    """
    conn = None

    def __init__(self, config=None):
        """
        Create a new instance of the MySQLHandler class
        """
        # Initialize Handler
        Handler.__init__(self, config)

        # Initialize Options
        self.hostname = self.config['hostname']
        self.port = int(self.config['port'])
        self.username = self.config['username']
        self.password = self.config['password']
        self.database = self.config['database']
        self.table = self.config['table']
        self.col_time = self.config['col_time']
        self.col_metric = self.config['col_metric']
        self.col_value = self.config['col_value']

        # Connect
        self._connect()

    def get_default_config_help(self):
        """
        Returns the help text for the configuration options for this handler
        """
        config = super(MySQLHandler, self).get_default_config_help()

        config.update({
        })

        return config

    def get_default_config(self):
        """
        Return the default config for the handler
        """
        config = super(MySQLHandler, self).get_default_config()

        config.update({
        })

        return config

    def __del__(self):
        """
        Destroy instance of the MySQLHandler class
        """
        self._close()

    def process(self, metric):
        """
        Process a metric
        """
        # Just send the data
        self._send(str(metric))

    def _send(self, data):
        """
        Insert the data
        """
        data = data.strip().split(' ')
        try:
            cursor = self.conn.cursor()
            cursor.execute("INSERT INTO %s (%s, %s, %s) VALUES(%%s, %%s, %%s)"
                           % (self.table, self.col_metric,
                              self.col_time, self.col_value),
                           (data[0], data[2], data[1]))
            cursor.close()
            self.conn.commit()
            # Insert data
            pass
            #self.socket.sendall(data)
            # Done
        except BaseException, e:
            # Log Error
            self.log.error("MySQLHandler: Failed sending data. %s.", e)
            # Attempt to restablish connection
            self._connect()

    def _connect(self):
        """
        Connect to the MySQL server
        """
        self._close()
        self.conn = MySQLdb.Connect(host=self.hostname,
                                    port=self.port,
                                    user=self.username,
                                    passwd=self.password,
                                    db=self.database)

    def _close(self):
        """
        Close the connection
        """
        if self.conn:
            self.conn.commit()
            self.conn.close()
