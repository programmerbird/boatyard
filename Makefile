
all: deb-packages


deb-packages: build/boatyard.deb build/boatyard-nginx.deb build/boatyard-nginx-python.deb

build/boatyard.deb:
	mkdir -p build
	find . -name "*~" -exec rm -f {} \;
	echo 'VERSION=`git describe`; sed -i "s@^Version.*@Version\: $${VERSION}@g" boatyard/DEBIAN/control' | sh
	dpkg -b boatyard $@
	
build/boatyard-nginx.deb: 
	mkdir -p build
	make -C boatyard-nginx all
	find boatyard-nginx -name "*~" -exec rm -f {} \;
	echo 'VERSION=`git describe`; sed -i "s@^Version.*@Version\: $${VERSION}@g" boatyard-nginx/deb/DEBIAN/control' | sh
	dpkg -b boatyard-nginx/deb $@
	
build/boatyard-nginx-python.deb:
	mkdir -p build
	find . -name "*~" -exec rm -f {} \;
	echo 'VERSION=`git describe`; sed -i "s@^Version.*@Version\: $${VERSION}@g" boatyard-nginx-python/DEBIAN/control' | sh
	dpkg -b boatyard-nginx-python $@
	
clean: 
	make -C boatyard-nginx clean
	find . -mindepth 2 -maxdepth 2 -name "Makefile" | sed "s/Makefile//g" | sed "s/.*/make -C \\0 clean/g" | sh
	
setupgit:
	@echo "" > .git/info/exclude
	@echo "*~" >> .git/info/exclude
	@echo "*.pyc" >> .git/info/exclude
	@echo "*.deb" >> .git/info/exclude
	@echo "build/" >> .git/info/exclude
