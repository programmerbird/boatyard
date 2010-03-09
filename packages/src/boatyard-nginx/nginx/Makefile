

NGINX_VERSION=0.7.65
UWSGI_VERSION=0.9.4.2

NGINX=nginx-${NGINX_VERSION}
UWSGI=uwsgi-${UWSGI_VERSION}
CURDIR=`pwd`
UWSGI_URL=http://projects.unbit.it/downloads/${UWSGI}.tar.gz
NGINX_URL=http://nginx.org/download/${NGINX}.tar.gz
NGINX_OPTS= --conf-path=/etc/nginx/nginx.conf \
		--sbin-path=/usr/sbin/ \
	    --error-log-path=/var/log/nginx/error.log \
	    --pid-path=/var/run/nginx.pid \
	    --lock-path=/var/lock/nginx.lock \
	    --http-log-path=/var/log/nginx/access.log \
	    --http-client-body-temp-path=/var/lib/nginx/body \
	    --http-proxy-temp-path=/var/lib/nginx/proxy \
	    --http-fastcgi-temp-path=/var/lib/nginx/fastcgi \
	    --with-debug \
	    --with-http_stub_status_module \
	    --with-http_flv_module \
	    --with-http_ssl_module \
	    --with-http_dav_module \
	    --with-http_gzip_static_module \
        --with-mail \
        --with-mail_ssl_module \
	    --with-ipv6 \
        --add-module=${CURDIR}/../${UWSGI}/nginx

all: build/nginx build/uwsgi

src/${NGINX}.tar.gz:
	mkdir -p src 
	wget ${NGINX_URL} -O $@
	
src/${UWSGI}.tar.gz:
	mkdir -p src 
	wget ${UWSGI_URL} -O $@

build/uwsgi: src/${UWSGI}.tar.gz
	mkdir -p build
	rm -rf build/uwsgi
	rm -rf build/${UWSGI}
	tar -C build/ -xvzf src/${UWSGI}.tar.gz 
	cd build/${UWSGI}; make -f Makefile.Py26; cd -
	cp -rf build/${UWSGI} build/uwsgi
	
build/nginx: src/${NGINX}.tar.gz build/uwsgi
	mkdir -p build
	rm -rf build/${NGINX}
	tar -C build/ -xvzf src/${NGINX}.tar.gz
	cd build/${NGINX}; ./configure ${NGINX_OPTS}; make; make -f objs/Makefile objs/nginx; cd -
	cp build/${NGINX}/objs/nginx build/nginx
	
clean:
	rm -rf build
	rm -rf src
	
	

