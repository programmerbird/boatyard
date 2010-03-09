#!/bin/sh

RUNUSER=`id -nu`

if [ "$RUNUSER" != "root" ]
    then
    echo "This program must be executed as root"
    exit 1
else
    echo "Running as $RUNUSER, good and verified"
fi


if [ ! $# -eq 1 ]
then
	echo "Usage: `basename $0` <USER>"
	exit 65
fi


USER=$1


if [ ! -d /home/$USER ];
then
mkdir -p /home/$USER
chown -R $USER:$USER /home/$USER
yes '' | adduser --home /home/$USER --disabled-password $USER
usermod -a -G boatyard $USER
usermod -a -G $USER www-data
fi

cd /home/$USER

if [ ! -f /home/$USER/private-key.rsa ];
then
mkdir -p .ssh
cd .ssh
ssh-keygen -f id_rsa  -N ''
cat id_rsa.pub >> authorized_keys
cd ../
chown -R $USER:$USER .ssh
fi

