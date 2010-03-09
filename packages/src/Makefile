all: ../deb/boatyard.deb ../deb/boatyard-nginx.deb ../deb/boatyard-nginx-python.deb

tidy:
	mkdir -p ../deb
	find . -name "*~" -exec rm -f {} \;

../deb/boatyard.deb: tidy
	dpkg -b boatyard $@
	
../deb/boatyard-nginx.deb: 
	make -C boatyard-nginx all
	find boatyard-nginx -name "*~" -exec rm -f {} \;
	dpkg -b boatyard-nginx/deb $@
	
../deb/boatyard-nginx-python.deb: tidy
	dpkg -b boatyard-nginx-python $@
	
clean: 
	make -C boatyard-nginx clean

