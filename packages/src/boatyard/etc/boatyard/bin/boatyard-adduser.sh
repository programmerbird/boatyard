#!/bin/sh

RUNAPPUSER=`id -nu`

if [ "$RUNAPPUSER" != "root" ]
    then
    echo "This program must be executed as root"
    exit 1
fi


if [ ! $# -eq 1 ]
then
	echo "Usage: `basename $0` <APPUSER>"
	exit 65
fi


APPUSER=$1


if [ ! -d /home/$APPUSER ];
then
mkdir -p /home/$APPUSER
chown -R $APPUSER:$APPUSER /home/$APPUSER
yes '' | adduser --home /home/$APPUSER --disabled-password $APPUSER
usermod -a -G boatyard $APPUSER
usermod -a -G $APPUSER www-data
fi

