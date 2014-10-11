# coding=utf-8

"""
The TCPCollector class collects metrics on TCP stats

#### Dependencies

 * /proc/net/netstat
 * /proc/net/snmp

#### Allowed Metric Names
<table>
<tr><th>Name</th><th>Description</th></tr>
<tr><td>SyncookiesSent</td><td>An application wasn't able to accept a
connection fast enough, so the kernel couldn't store an entry in the queue for
this connection. Instead of dropping it, it sent a cookie to the client.
</td></tr>
<tr><td>SyncookiesRecv</td><td>After sending a cookie, it came back to us
and passed the check.</td></tr>
<tr><td>SyncookiesFailed</td><td>After sending a cookie, it came back to us
but looked invalid.</td></tr>
<tr><td>EmbryonicRsts</td><td></td></tr>
<tr><td>PruneCalled</td><td></td></tr>
<tr><td>RcvPruned</td><td>If the kernel is really really desperate and cannot
give more memory to this socket even after dropping the ofo queue, it will
simply discard the packet it received.  This is Really Bad.</td></tr>
<tr><td>OfoPruned</td><td>When a socket is using too much memory (rmem), the
kernel will first discard any out-of-order packet that has been queued (with
SACK).</td></tr>
<tr><td>OutOfWindowIcmps</td><td></td></tr>
<tr><td>LockDroppedIcmps</td><td></td></tr>
<tr><td>ArpFilter</td><td></td></tr>
<tr><td>TW</td><td></td></tr>
<tr><td>TWRecycled</td><td></td></tr>
<tr><td>TWKilled</td><td></td></tr>
<tr><td>PAWSPassive</td><td></td></tr>
<tr><td>PAWSActive</td><td></td></tr>
<tr><td>PAWSEstab</td><td></td></tr>
<tr><td>DelayedACKs</td><td>We waited for another packet to send an ACK, but
didn't see any, so a timer ended up sending a delayed ACK.</td></tr>
<tr><td>DelayedACKLocked</td><td>We wanted to send a delayed ACK but failed
because the socket was locked.  So the timer was reset.</td></tr>
<tr><td>DelayedACKLost</td><td>We sent a delayed and duplicated ACK because the
remote peer retransmitted a packet, thinking that it didn't get to us.</td></tr>
<tr><td>ListenOverflows</td><td>We completed a 3WHS but couldn't put the socket
on the accept queue, so we had to discard the connection.</td></tr>
<tr><td>ListenDrops</td><td>We couldn't accept a connection because one of: we
had no route to the destination, we failed to allocate a socket, we failed to
allocate a new local port bind bucket.  Note: this counter also include all the
increments made to ListenOverflows</td></tr>
<tr><td>TCPPrequeued</td><td></td></tr>
<tr><td>TCPDirectCopyFromBacklog</td><td></td></tr>
<tr><td>TCPDirectCopyFromPrequeue</td><td></td></tr>
<tr><td>TCPPrequeueDropped</td><td></td></tr>
<tr><td>TCPHPHits</td><td></td></tr>
<tr><td>TCPHPHitsToUser</td><td></td></tr>
<tr><td>TCPPureAcks</td><td></td></tr>
<tr><td>TCPHPAcks</td><td></td></tr>
<tr><td>TCPRenoRecovery</td><td>A packet was lost and we recovered after a
fast retransmit.</td></tr>
<tr><td>TCPSackRecovery</td><td>A packet was lost and we recovered by using
selective acknowledgements.</td></tr>
<tr><td>TCPSACKReneging</td><td></td></tr>
<tr><td>TCPFACKReorder</td><td>We detected re-ordering using FACK (Forward ACK
-- the highest sequence number known to have been received by the peer when
using SACK -- FACK is used during congestion control).</td></tr>
<tr><td>TCPSACKReorder</td><td>We detected re-ordering using SACK.</td></tr>
<tr><td>TCPRenoReorder</td><td>We detected re-ordering using fast retransmit.
</td></tr>
<tr><td>TCPTSReorder</td><td>We detected re-ordering using the timestamp option.
</td></tr>
<tr><td>TCPFullUndo</td><td>We detected some erroneous retransmits and undid our
CWND reduction.</td></tr>
<tr><td>TCPPartialUndo</td><td>We detected some erroneous retransmits, a partial
ACK arrived while we were fast retransmitting, so we were able to partially undo
some of our CWND reduction.</td></tr>
<tr><td>TCPDSACKUndo</td><td>We detected some erroneous retransmits, a D-SACK
arrived and ACK'ed all the retransmitted data, so we undid our CWND reduction.
</td></tr>
<tr><td>TCPLossUndo</td><td>We detected some erroneous retransmits, a partial
ACK arrived, so we undid our CWND reduction.</td></tr>
<tr><td>TCPLoss</td><td></td></tr>
<tr><td>TCPLostRetransmit</td><td></td></tr>
<tr><td>TCPRenoFailures</td><td></td></tr>
<tr><td>TCPSackFailures</td><td></td></tr>
<tr><td>TCPLossFailures</td><td></td></tr>
<tr><td>TCPFastRetrans</td><td></td></tr>
<tr><td>TCPForwardRetrans</td><td></td></tr>
<tr><td>TCPSlowStartRetrans</td><td></td></tr>
<tr><td>TCPTimeouts</td><td></td></tr>
<tr><td>TCPRenoRecoveryFail</td><td></td></tr>
<tr><td>TCPSackRecoveryFail</td><td></td></tr>
<tr><td>TCPSchedulerFailed</td><td></td></tr>
<tr><td>TCPRcvCollapsed</td><td></td></tr>
<tr><td>TCPDSACKOldSent</td><td></td></tr>
<tr><td>TCPDSACKOfoSent</td><td></td></tr>
<tr><td>TCPDSACKRecv</td><td></td></tr>
<tr><td>TCPDSACKOfoRecv</td><td></td></tr>

<tr><td>TCPSACKDiscard</td><td>We got a completely invalid SACK block and
discarded it.</td></tr>
<tr><td>TCPDSACKIgnoredOld</td><td>We got a duplicate SACK while retransmitting
so we discarded it.</td></tr>
<tr><td>TCPDSACKIgnoredNoUndo</td><td>We got a duplicate SACK and discarded it.
</td></tr>

<tr><td>TCPAbortOnSyn</td><td>We received an unexpected SYN so we sent a RST to
the peer.</td></tr>
<tr><td>TCPAbortOnData</td><td>We were in FIN_WAIT1 yet we received a data
packet with a sequence number that's beyond the last one for this connection,
so we RST'ed.</td></tr>
<tr><td>TCPAbortOnClose</td><td>We received data but the user has closed the
socket, so we have no wait of handing it to them, so we RST'ed.</td></tr>
<tr><td>TCPAbortOnMemory</td><td>This is Really Bad.  It happens when there are
too many orphaned sockets (not attached a FD) and the kernel has to drop a
connection. Sometimes it will send a reset to the peer, sometimes it wont.
</td></tr>
<tr><td>TCPAbortOnTimeout</td><td>The connection timed out really hard.
</td></tr>
<tr><td>TCPAbortOnLinger</td><td>We killed a socket that was closed by the
application and lingered around for long enough.</td></tr>
<tr><td>TCPAbortFailed</td><td>We tried to send a reset, probably during one of
teh TCPABort* situations above, but we failed e.g. because we couldn't allocate
enough memory (very bad).</td></tr>
<tr><td>TCPMemoryPressures</td><td>Number of times a socket was put in "memory
pressure" due to a non fatal memory allocation failure (reduces the send buffer
size etc).</td></tr>

<tr><td>TCPBacklogDrop</td><td>We received something but had to drop it because
the socket's receive queue was full.</td></tr>

<tr><td>RtoAlgorithm</td><td>The algorithm used to determine the timeout value
used for retransmitting unacknowledged octets.</td></tr>
<tr><td>RtoMin</td><td>The minimum value permitted by a TCP implementation
for the retransmission timeout, measured in milliseconds.
More refined semantics for objects of this type depend upon the algorithm used
to determine the retransmission timeout. In particular,
when the timeout algorithm is ``rsre '' (3), an object of this type has the
semantics of the LBOUND quantity described in RFC 793.</td></tr>
<tr><td>RtoMax</td><td>The maximum value permitted by a TCP implementation for
the retransmission timeout, measured in milliseconds. More refined semantics
for objects of this type depend upon the algorithm used to determine the
retransmission timeout. In particular, when the timeout algorithm is ``rsre''
(3), an object of this type has the semantics of the UBOUND quantity described
in RFC 793.</td></tr>
<tr><td>MaxConn</td><td>The limit on the total number of TCP connections the
entity can support. In entities where the maximum number of connections is
dynamic, this object should contain the value -1.</td></tr>
<tr><td>ActiveOpens</td><td>The number of times TCP connections have made a
direct transition to the SYN-SENT state from the CLOSED state.</td></tr>
<tr><td>PassiveOpens</td><td>The number of times TCP connections have made a
direct transition to the SYN-RCVD state from the LISTEN state.</td></tr>
<tr><td>AttemptFails</td><td>The number of times TCP connections have made a
direct transition to the CLOSED state from either the SYN-SENT state or the
SYN-RCVD state, plus the number of times TCP connections have made a direct
transition to the LISTEN state from the SYN-RCVD state.</td></tr>
<tr><td>EstabResets</td><td>The number of times TCP connections have made a
direct transition to the CLOSED state from either the ESTABLISHED state or the
CLOSE-WAIT state.</td></tr>
<tr><td>CurrEstab</td><td>The number of TCP connections for which the current
state is either ESTABLISHED or CLOSE- WAIT.</td></tr>
<tr><td>InSegs</td><td>The total number of segments received, including those
received in error. This count includes segments received on currently
established connections.</td></tr>
<tr><td>OutSegs</td><td>The total number of segments sent, including those on
current connections but excluding those containing only retransmitted octets.
</td></tr>
<tr><td>RetransSegs</td><td>The total number of segments retransmitted - that
is, the number of TCP segments transmitted containing one or more previously
transmitted octets.</td></tr>
<tr><td>InErrs</td><td>The total number of segments received in error (for
example, bad TCP checksums).</td></tr>
<tr><td>OutRsts</td><td>The number of TCP segments sent containing the RST
flag.</td></tr>
</table>

"""

import diamond.collector
import os


class TCPCollector(diamond.collector.Collector):

    PROC = [
        '/proc/net/netstat',
        '/proc/net/snmp'
    ]

    GAUGES = [
        'CurrEstab',
        'MaxConn',
    ]

    def process_config(self):
        if self.config['allowed_names'] is None:
            self.config['allowed_names'] = []

    def get_default_config_help(self):
        config_help = super(TCPCollector, self).get_default_config_help()
        config_help.update({
            'allowed_names': 'list of entries to collect, empty to collect all',
        })
        return config_help

    def get_default_config(self):
        """
        Returns the default collector settings
        """
        config = super(TCPCollector, self).get_default_config()
        config.update({
            'path':             'tcp',
            'allowed_names':    'ListenOverflows, ListenDrops, TCPLoss, '
            + 'TCPTimeouts, TCPFastRetrans, TCPLostRetransmit, '
            + 'TCPForwardRetrans, TCPSlowStartRetrans, CurrEstab, '
            + 'TCPAbortOnMemory, TCPBacklogDrop, AttemptFails, '
            + 'EstabResets, InErrs, ActiveOpens, PassiveOpens',
        })
        return config

    def collect(self):
        metrics = {}

        for filepath in self.PROC:
            if not os.access(filepath, os.R_OK):
                self.log.error('Permission to access %s denied', filepath)
                continue

            header = ''
            data = ''

            # Seek the file for the lines that start with Tcp
            file = open(filepath)

            if not file:
                self.log.error('Failed to open %s', filepath)
                continue

            while True:
                line = file.readline()

                # Reached EOF?
                if len(line) == 0:
                    break

                # Line has metrics?
                if line.startswith("Tcp"):
                    header = line
                    data = file.readline()
                    break
            file.close()

            # No data from the file?
            if header == '' or data == '':
                self.log.error('%s has no lines with Tcp', filepath)
                continue

            header = header.split()
            data = data.split()

            for i in xrange(1, len(header)):
                metrics[header[i]] = data[i]

        for metric_name in metrics.keys():
            if (len(self.config['allowed_names']) > 0
                    and metric_name not in self.config['allowed_names']):
                continue

            value = long(metrics[metric_name])

            # Publish the metric
            if metric_name in self.GAUGES:
                self.publish_gauge(metric_name, value, 0)
            else:
                self.publish_counter(metric_name, value, 0)
