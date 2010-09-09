all: deb-packages 

deb-packages:
	cd nginx; make all
	mkdir -p deb/etc/
	cp -rf nginx/build/uwsgi deb/etc/uwsgi
	cd nginx; make build/nginx
	mkdir -p deb/usr/sbin/
	cp -rf nginx/build/nginx deb/usr/sbin/nginx
	
clean:
	cd nginx; make clean
	rm -rf deb/usr/sbin/nginx
	rm -rf deb/etc/uwsgi
