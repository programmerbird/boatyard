
all: deb 

deb: 
	make -C src 

clean: 
	rm -rf deb 
	find . -mindepth 2 -maxdepth 2 -name "Makefile" | sed "s/Makefile//g" | sed "s/.*/make -C \\0 clean/g" | sh

