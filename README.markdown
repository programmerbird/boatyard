# Boatyard 

## Who Should Use Boatyard ?

If you just want to use it, you are not. 
We are not ready for production yet.

If you want to help, you are welcome.

## What does it do ?

1. Install nginx + uwsgi to your ubuntu server.
2. Provide a convenient way to add a new website.
3. Git push to deploy!

## Add a new website 

    sudo boatyard-adduser alice 
    sudo boatyard-startapp-python alice aliceweb 
    
## Deploying a web site
The server will automatically install the require packages using 
pip requirements file store in the project <requirements.ini> and 
reload the server after each git push. 
 
    git push ssh://alice@servername/~/aliceweb master 

## Installing
Add our repository to your /etc/apt/sources.list

    sudo echo "deb http://boatyard.s3.amazonaws.com/packages/ubuntu karmic main" > /etc/apt/sources.list.d/x10studio.list
    gpg --keyserver keyserver.ubuntu.com --recv-keys 9CE8C487
    gpg -a --export 9CE8C487 | sudo apt-key add -

Install Package

    sudo aptitude install boatyard-nginx-python
    
