#!/bin/sh


RUNUSER=`id -nu`

if [ "$RUNUSER" != "root" ]
    then
    echo "This program must be executed as root"
    exit 1
fi


if [ $# -lt 2 ]
then
	echo "Usage: `basename $0` <USER> <APP> [<CONFIG>=boatyard]"
	exit 65
fi

USER=$1
APP=$2
CONFIG=${3:-boatyard}
RANDOM=T0k2349H

HOME=/etc/boatyard/templates/python-nginx
GIT_PATH=/home/$USER/$APP.git
APP_PATH=/home/$USER/deployed-apps/$APP

if [ ! -d "$APP_PATH/env" ]
then 
	virtualenv --no-site-packages $APP_PATH/env
fi

mkdir -p $APP_PATH/webs
mkdir -p $APP_PATH/scripts

cd $APP_PATH/webs

if [ ! -d "$GIT_PATH" ]
then
	git init
	git add .
	git commit --allow-empty -a -m "initial import"
	mv .git $GIT_PATH
fi

cd $GIT_PATH
cp $HOME/scripts/post-update hooks/post-update
sed -i "s/{{BOATYARD_APP}}/$APP/g" hooks/post-update
sed -i "s/{{BOATYARD_USER}}/$USER/g" hooks/post-update
sed -i "s/{{BOATYARD_CONFIG}}/$CONFIG/g" hooks/post-update
sed -i "s/{{BOATYARD_RANDOM}}/$RANDOM/g" hooks/post-update

chmod +x hooks/post-update
ln -s $APP_PATH/webs  target

cd $APP_PATH/scripts
cp $HOME/app/scripts/daemon.sh daemon.sh 
cp $HOME/app/scripts/nginx.conf nginx.conf 
cp $HOME/app/scripts/uwsgi.conf uwsgi.conf 
cp $HOME/app/scripts/wsgi.py wsgi_$APP$RANDOM.py 
find . -name "*.*" -exec sed -i "s/{{BOATYARD_APP}}/$APP/g" {} \;
find . -name "*.*" -exec sed -i "s/{{BOATYARD_USER}}/$USER/g" {} \;
find . -name "*.*" -exec sed -i "s/{{BOATYARD_CONFIG}}/$CONFIG/g" {} \;
find . -name "*.*" -exec sed -i "s/{{BOATYARD_RANDOM}}/$RANDOM/g" {} \;

ln -s $APP_PATH/scripts/nginx.conf /etc/boatyard/configs/$APP
cp daemon.sh /etc/init.d/boatyard-$APP

cd $APP_PATH
if [ ! -d "$APP$RANDOM" ]
then
	ln -s webs $APP$RANDOM
fi

chown -R $USER:$USER $APP_PATH
chown -R $USER:$USER $GIT_PATH

mkdir -p /home/$USER/log/$APP
touch /var/log/boatyard/$APP.error
touch /var/log/boatyard/$APP.access
chown www-data:www-data /var/log/boatyard/$APP.error
chown www-data:www-data /var/log/boatyard/$APP.access
ln -s /var/log/boatyard/$APP.error /home/$USER/log/$APP/error.log
ln -s /var/log/boatyard/$APP.access /home/$USER/log/$APP/access.log

/etc/init.d/boatyard-$APP start
update-rc.d boatyard-$APP defaults

