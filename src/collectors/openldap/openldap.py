# coding=utf-8

"""
Collects data from a OpenLDAP server.

#### Dependencies

 * ldap module

"""

import diamond.collector

try:
    import ldap
except ImportError:
    ldap = None


class OpenLDAPCollector(diamond.collector.Collector):

    STATS = {
        'conns.total': {
            'base': 'cn=Total,cn=Connections,cn=Monitor',
            'attr': 'monitorCounter'},
        'conns.current': {
            'base': 'cn=Current,cn=Connections,cn=Monitor',
            'attr': 'monitorCounter'},
        'ops.total': {
            'base': 'cn=Operations,cn=Monitor',
            'attr': 'monitorOpCompleted'},
        'ops.total_initiated': {
            'base': 'cn=Operations,cn=Monitor',
            'attr': 'monitorOpInitiated'},
        'ops.bind': {
            'base': 'cn=Bind,cn=Operations,cn=Monitor',
            'attr': 'monitorOpCompleted'},
        'ops.unbind': {
            'base': 'cn=Unbind,cn=Operations,cn=Monitor',
            'attr': 'monitorOpCompleted'},
        'ops.delete': {
            'base': 'cn=Delete,cn=Operations,cn=Monitor',
            'attr': 'monitorOpCompleted'},
        'ops.modify': {
            'base': 'cn=Modify,cn=Operations,cn=Monitor',
            'attr': 'monitorOpCompleted'},
        'ops.modrdn': {
            'base': 'cn=Modrdn,cn=Operations,cn=Monitor',
            'attr': 'monitorOpCompleted'},
        'ops.compare': {
            'base': 'cn=Compare,cn=Operations,cn=Monitor',
            'attr': 'monitorOpCompleted'},
        'ops.search': {
            'base': 'cn=Search,cn=Operations,cn=Monitor',
            'attr': 'monitorOpCompleted'},
        'ops.extended': {
            'base': 'cn=Extended,cn=Operations,cn=Monitor',
            'attr': 'monitorOpCompleted'},
        'ops.abandon': {
            'base': 'cn=Abandon,cn=Operations,cn=Monitor',
            'attr': 'monitorOpCompleted'},
        'waiter.read': {
            'base': 'cn=Read,cn=Waiters,cn=Monitor',
            'attr': 'monitorCounter'},
        'waiter.write': {
            'base': 'cn=Write,cn=Waiters,cn=Monitor',
            'attr': 'monitorCounter'},
        'stats.bytes': {
            'base': 'cn=Bytes,cn=Statistics,cn=Monitor',
            'attr': 'monitorCounter'},
        'stats.pdu': {
            'base': 'cn=PDU,cn=Statistics,cn=Monitor',
            'attr': 'monitorCounter'},
        'stats.referrals': {
            'base': 'cn=Referrals,cn=Statistics,cn=Monitor',
            'attr': 'monitorCounter'},
        'stats.entries': {
            'base': 'cn=Entries,cn=Statistics,cn=Monitor',
            'attr': 'monitorCounter'},
        'threads.open': {
            'base': 'cn=Open,cn=Threads,cn=Monitor',
            'attr': 'monitoredInfo'},
        'threads.starting': {
            'base': 'cn=Starting,cn=Threads,cn=Monitor',
            'attr': 'monitoredInfo'},
        'threads.active': {
            'base': 'cn=Active,cn=Threads,cn=Monitor',
            'attr': 'monitoredInfo'},
        'threads.max': {
            'base': 'cn=Max,cn=Threads,cn=Monitor',
            'attr': 'monitoredInfo'},
        'threads.max_pending': {
            'base': 'cn=Max Pending,cn=Threads,cn=Monitor',
            'attr': 'monitoredInfo'},
        'threads.pending': {
            'base': 'cn=Pending,cn=Threads,cn=Monitor',
            'attr': 'monitoredInfo'},
        'threads.backload': {
            'base': 'cn=Backload,cn=Threads,cn=Monitor',
            'attr': 'monitoredInfo'},
        }

    def __init__(self, *args, **kwargs):
        super(OpenLDAPCollector, self).__init__(*args, **kwargs)

    def get_default_config_help(self):
        config_help = super(OpenLDAPCollector, self).get_default_config_help()
        config_help.update({
            'host': 'Hostname to collect from',
            'port': 'Port number to collect from',
            'username': 'DN of user we connect with',
            'password': 'Password of user we connect with',
        })
        return config_help

    def get_default_config(self):
        """
        Return default config

:rtype: dict

        """
        config = super(OpenLDAPCollector, self).get_default_config()
        config.update({
            'path': 'openldap',
            'host': 'localhost',
            'port': 389,
            'username': 'cn=monitor',
            'password': 'password',
        })
        return config

    def get_datapoints(self, ldap_url, username, password):
        datapoints = {}

        conn = ldap.initialize(ldap_url)
        conn.start_tls_s()
        conn.simple_bind_s(username, password)

        try:
            for key in self.STATS.keys():
                base = self.STATS[key]['base']
                attr = self.STATS[key]['attr']
                num = conn.search(base, ldap.SCOPE_BASE,
                                  'objectClass=*', [attr])
                result_type, result_data = conn.result(num, 0)
                datapoints[key] = int(result_data[0][1][attr][0])
        except:
            self.log.warn('Unable to query ldap base=%s, attr=%s'
                          % (base, attr))
            raise

        return datapoints

    def collect(self):
        if ldap is None:
            self.log.error('Unable to import module ldap')
            return {}

        ldap_url = 'ldap://%s:%d' % (self.config['host'],
                                     int(self.config['port']))
        try:
            datapoints = self.get_datapoints(ldap_url,
                                             self.config['username'],
                                             self.config['password'])
        except Exception, e:
            self.log.error('Unable to query %s: %s' % (ldap_url, e))
            return {}

        for name, value in datapoints.items():
            self.publish(name, value)
