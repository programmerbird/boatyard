all:
	make -C nginx build/uwsgi
	mkdir -p deb/etc/
	cp -rf nginx/build/uwsgi deb/etc/uwsgi

	make -C nginx build/nginx
	mkdir -p deb/usr/sbin/
	cp -rf nginx/build/nginx deb/usr/sbin/nginx
	
clean:
	make -C nginx clean
	rm -rf deb/usr/sbin/nginx
	rm -rf deb/etc/uwsgi
