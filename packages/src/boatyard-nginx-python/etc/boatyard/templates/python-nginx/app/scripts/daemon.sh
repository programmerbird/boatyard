#! /bin/sh

### BEGIN INIT INFO
# Provides:          boatyard-{{BOATYARD_APP}}
# Required-Start:    $all
# Required-Stop:     $all
# Default-Start:     2 3 4 5
# Default-Stop:      0 1 6
# Short-Description: starts the boatyard-{{BOATYARD_APP}} web server
# Description:       starts boatyard-{{BOATYARD_APP}} using start-stop-daemon
### END INIT INFO

PATH=/usr/local/sbin:/usr/local/bin:/sbin:/bin:/usr/sbin:/usr/bin
NAME=boatyard-{{BOATYARD_APP}}
DESC={{BOATYARD_APP}}

DAEMON=/etc/uwsgi/uwsgi26
PIDFILE=/var/run/$NAME.pid
UID=`id --user {{BOATYARD_USER}}`
GID=`id --group {{BOATYARD_USER}}`
SOCKFILE=/tmp/boatyard-{{BOATYARD_APP}}.sock
DAEMON_OPTS="--processes 6 --harakiri 6 --disable-logging --master \
			--pidfile $PIDFILE \
			--daemonize /tmp/boatyard-{{BOATYARD_APP}}.out \
			--socket $SOCKFILE \
			--home /home/{{BOATYARD_USER}}/deployed-apps/{{BOATYARD_APP}}/env
			--chmod-socket --xmlconfig /home/{{BOATYARD_USER}}/deployed-apps/{{BOATYARD_APP}}/scripts/uwsgi.conf"

set -e

. /lib/lsb/init-functions

case "$1" in
  start)
	echo -n "Starting $DESC: "
		touch $PIDFILE
		chown -R {{BOATYARD_USER}}:{{BOATYARD_USER}} $PIDFILE
		sudo -u {{BOATYARD_USER}} start-stop-daemon --start --quiet --pidfile $PIDFILE \
			--exec $DAEMON -- $DAEMON_OPTS || true
	echo "$NAME."
	;;
  stop)
	echo -n "Stopping $DESC: "
	kill -s INT `cat $PIDFILE`
	echo "$NAME."
	;;
  force-reload)
	echo -n "Force Reload $DESC: "
	kill -s TERM `cat $PIDFILE`
	echo "$NAME."
	;;
  restart)
	echo -n "Restart $DESC: "
	kill -s INT `cat $PIDFILE`
	sleep 5
	sudo -u {{BOATYARD_USER}} start-stop-daemon --start --quiet --pidfile $PIDFILE \
		--exec $DAEMON -- $DAEMON_OPTS || true
	echo "$NAME."
	;;
  reload)
	echo -n "Reload $DESC: "
	kill -s HUP `cat $PIDFILE`
	echo "$NAME."
	;;
  status)
	echo -n "Status $DESC: "
	kill -s USR1 `cat $PIDFILE`
	tail -5 /tmp/boatyard-{{BOATYARD_APP}}.out
	echo "$NAME."
	;;
  *)
	echo "Usage: $NAME {start|stop|restart|force-reload|reload|status}" >&2
	exit 1
	;;
esac

exit 0
