
all: deb-packages

deb-packages: build/nginx-uwsgi.deb
	
build/nginx-uwsgi.deb:
	mkdir -p build
	find . -name "*~" -exec rm -f {} \;
	echo 'VERSION=`git describe`; sed -i "s@^Version.*@Version\: $${VERSION}@g" nginx-uwsgi/DEBIAN/control' | sh
	dpkg -b nginx-python $@
	
clean: 
	make -C boatyard-nginx clean
	find . -mindepth 2 -maxdepth 2 -name "Makefile" | sed "s/Makefile//g" | sed "s/.*/make -C \\0 clean/g" | sh
	
setupgit:
	@echo "" > .git/info/exclude
	@echo "*~" >> .git/info/exclude
	@echo "*.pyc" >> .git/info/exclude
	@echo "*.deb" >> .git/info/exclude
	@echo "build/" >> .git/info/exclude
