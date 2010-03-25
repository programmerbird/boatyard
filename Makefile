
all: deb-packages


deb-packages: build/boatyard.deb build/boatyard-nginx.deb build/boatyard-nginx-python.deb

build/boatyard.deb:
	find . -name "*~" -exec rm -f {} \;
	dpkg -b boatyard $@
	
build/boatyard-nginx.deb: 
	make -C boatyard-nginx all
	find boatyard-nginx -name "*~" -exec rm -f {} \;
	dpkg -b boatyard-nginx/deb $@
	
build/boatyard-nginx-python.deb:
	find . -name "*~" -exec rm -f {} \;
	dpkg -b boatyard-nginx-python $@
	
clean: 
	make -C boatyard-nginx clean

clean: 
	find . -mindepth 2 -maxdepth 2 -name "Makefile" | sed "s/Makefile//g" | sed "s/.*/make -C \\0 clean/g" | sh
	
setupgit:
	@echo "" > .git/info/exclude
	@echo "*~" >> .git/info/exclude
	@echo "*.pyc" >> .git/info/exclude
	@echo "*.deb" >> .git/info/exclude
	@echo "build/" >> .git/info/exclude
