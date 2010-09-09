## What does it do ?

1. nginx + uwsgi on your ubuntu server.
2. Provide a convenient way to add a new website. (required http://github.com/ssimasanti/rockets/) 
3. Git push to deploy! (required http://github.com/ssimasanti/rockets/)

## Installing
Add our repository to your /etc/apt/sources.list

    sudo echo "deb http://boatyard.s3.amazonaws.com/packages/ubuntu karmic main" > /etc/apt/sources.list.d/boatyard.list
    gpg --keyserver keyserver.ubuntu.com --recv-keys 9CE8C487
    gpg -a --export 9CE8C487 | sudo apt-key add -

Install Package

    sudo aptitude update 
    sudo aptitude install nginx-uswgi
    
