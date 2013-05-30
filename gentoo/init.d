#!/sbin/runscript

SVCNAME="diamond"
PIDFILE=`grep pid_file /etc/diamond/diamond.conf | awk '{ print $3 }'`
DIAMOND="/usr/bin/diamond"
DIAMOND_OPTS=""
TIMEOUT="30"

depend() {
	need net
}

start() {
	ebegin "Starting ${SVCNAME}"
	# Use start stop daemon to apply system limits #347301 
	start-stop-daemon --start -- ${DIAMOND} ${DIAMOND_OPTS}

	i=0
	while [ ! -e "${PIDFILE}" ] && [ $i -lt ${TIMEOUT} ]; do
		sleep 1 && i=$(expr $i + 1)
	done

	eend $(test $i -lt ${TIMEOUT})
}

stop() {
	PID=$(cat "${PIDFILE}" 2>/dev/null)
	if [ -z "${PID}" ]; then
		einfo "${SVCNAME} not running (no pid file)"
		return 0
	fi

	ebegin "Stopping ${SVCNAME}"
	kill -9 ${PID}

	i=0
	while ( test -f "${PIDFILE}" && pgrep -P ${PID} diamond >/dev/null ) \
		&& [ $i -lt ${TIMEOUT} ]; do
		sleep 1 && i=$(expr $i + 1)
	done

	eend $(test $i -lt ${TIMEOUT})
}

status() {
    pgrep -F ${PIDFILE} &> /dev/null
    if [ $? -eq 0 ]
    then
        einfo "${SVCNAME} is running"
        return 0
    fi
    
    einfo "${SVCNAME} is not running"
    return 1
}

# vim: ts=4 filetype=gentoo-init-d
