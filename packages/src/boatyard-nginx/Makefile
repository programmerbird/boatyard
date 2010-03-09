all:
	make -C nginx build/uwsgi
	cp -rf nginx/build/uwsgi deb/etc/uwsgi

	make -C nginx build/nginx
	cp -rf nginx/build/nginx deb/usr/sbin/nginx
	
clean:
	make -C nginx clean
	rm -rf deb/usr/sbin/nginx
	rm -rf deb/etc/uwsgi
