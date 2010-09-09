
all: deb-packages

deb-packages: build/nginx-uwsgi.deb
	
build/nginx-uwsgi.deb:
	cd nginx-uwsgi; make all
	mkdir -p build
	find . -name "*~" -exec rm -f {} \;
	echo 'VERSION=`git describe --tags`; sed -i "s@^Version.*@Version\: $${VERSION}@g" nginx-uwsgi/deb/DEBIAN/control' | sh
	dpkg -b nginx-uwsgi/deb $@

tests: deb-packages
	sudo dpkg -r nginx-uwsgi
	sudo rm -rf /etc/nginx
	sudo dpkg -i build/nginx-uwsgi.deb
	
clean: 
	make -C nginx-uwsgi clean
	find . -mindepth 2 -maxdepth 2 -name "Makefile" | sed "s/Makefile//g" | sed "s/.*/make -C \\0 clean/g" | sh
	
setupgit:
	@echo "" > .git/info/exclude
	@echo "*~" >> .git/info/exclude
	@echo "*.pyc" >> .git/info/exclude
	@echo "*.deb" >> .git/info/exclude
	@echo "build/" >> .git/info/exclude
