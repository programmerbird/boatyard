all: ../deb/binary/boatyard.deb ../deb/binary/boatyard-nginx.deb ../deb/binary/boatyard-nginx-python.deb

../deb/binary/boatyard.deb:
	mkdir -p ../deb
	mkdir -p ../deb/binary
	find . -name "*~" -exec rm -f {} \;
	dpkg -b boatyard $@
	
../deb/binary/boatyard-nginx.deb: 
	mkdir -p ../deb
	mkdir -p ../deb/binary
	make -C boatyard-nginx all
	find boatyard-nginx -name "*~" -exec rm -f {} \;
	dpkg -b boatyard-nginx/deb $@
	
../deb/binary/boatyard-nginx-python.deb:
	mkdir -p ../deb
	mkdir -p ../deb/binary
	find . -name "*~" -exec rm -f {} \;
	dpkg -b boatyard-nginx-python $@
	
clean: 
	make -C boatyard-nginx clean

