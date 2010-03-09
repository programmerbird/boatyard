all: ../deb/boatyard.deb ../deb/boatyard-nginx.deb ../deb/boatyard-nginx-python.deb

../deb/boatyard.deb:
	mkdir -p ../deb
	find . -name "*~" -exec rm -f {} \;
	dpkg -b boatyard $@
	
../deb/boatyard-nginx.deb: 
	mkdir -p ../deb
	make -C boatyard-nginx all
	find boatyard-nginx -name "*~" -exec rm -f {} \;
	dpkg -b boatyard-nginx/deb $@
	
../deb/boatyard-nginx-python.deb:
	mkdir -p ../deb
	find . -name "*~" -exec rm -f {} \;
	dpkg -b boatyard-nginx-python $@
	
clean: 
	make -C boatyard-nginx clean

