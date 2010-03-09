
all: deb-packages

deb-packages: 
	cd src; make all; cd -

clean: 
	rm -rf testproject
	find . -mindepth 2 -maxdepth 2 -name "Makefile" | sed "s/Makefile//g" | sed "s/.*/make -C \\0 clean/g" | sh

testenv: deb-packages
	sudo dpkg -r boatyard-nginx-python 
	sudo dpkg -r boatyard-nginx
	sudo dpkg -r boatyard
	sudo rm -rf /etc/nginx
	sudo rm -rf /etc/boatyard
	sudo dpkg -i deb/boatyard.deb 
	sudo dpkg -i deb/boatyard-nginx.deb 
	sudo dpkg -i deb/boatyard-nginx-python.deb 
	
testproject:
	django-admin.py startproject testproject 
	echo "from settings import *" > testproject/settings_boatyard.py 
	echo 'ROOT_URLCONF = "urls"' >> testproject/settings_boatyard.py
	echo "Django==1.1.1" >> testproject/requirements.txt
	cd testproject; git init; git add .; git commit -a -m "initial import"; cd -

testaccount:
	rm -rf ~/testapp.git
	sudo rm -rf ~/deployed-apps/testapp
	sudo boatyard-startapp-python `whoami` testapp
	sudo /etc/init.d/nginx restart
	
test: testenv testproject testaccount
	cd testproject; git remote add production ~/testapp.git; cd -
	cd testproject; git pull production master; git add .; git commit -a -m "initial import"; git push production master; cd -
	

