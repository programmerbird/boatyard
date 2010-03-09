all:
	make -C packages all	
	
upload: all
	cd deb; dpkg-scanpackages binary /dev/null | sed "s/Filename\: \.\//Filename: /g" | gzip > binary/Packages.gz; cd -
	cd deb; rm -f Release; cd -
	cd deb; apt-ftparchive release . > Release; cd -
	cd deb; gpg --sign -ba -o Release.gpg Release; cd -
	cd deb; s3cmd sync --acl-public ./ s3://boatyard/repositories/debian/
	
clean: 
	find . -mindepth 2 -maxdepth 2 -name "Makefile" | sed "s/Makefile//g" | sed "s/.*/make -C \\0 clean/g" | sh

setupgit:
	@echo "" > .git/info/exclude
	@echo "*~" >> .git/info/exclude
	@echo "*.pyc" >> .git/info/exclude
	@echo "*.deb" >> .git/info/exclude
	@echo "build/" >> .git/info/exclude
