all: ../boatyard.deb ../boatyard-nginx.deb ../boatyard-nginx-python.deb

../boatyard.deb:
	find . -name "*~" -exec rm -f {} \;
	dpkg -b boatyard $@
	
../boatyard-nginx.deb: 
	make -C boatyard-nginx all
	find boatyard-nginx -name "*~" -exec rm -f {} \;
	dpkg -b boatyard-nginx/deb $@
	
../boatyard-nginx-python.deb:
	find . -name "*~" -exec rm -f {} \;
	dpkg -b boatyard-nginx-python $@
	
clean: 
	make -C boatyard-nginx clean

