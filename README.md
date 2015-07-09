Work in progress...

installation
--------------------

### with virtualenv

#### obtain virtualenv

Check https://virtualenv.pypa.io/en/latest/installation.html or follow these instructions:

##### if Debian equal/newer than jessie (virtualenv version equal or greater than 1.9)

    sudo apt-get install python-virtualenv
    
##### if Debian older  than jessie (or virtualenv version prior to 1.9)

    sudo apt-get install ca-certificates gnupg
    curl https://pypi.python.org/packages/source/v/virtualenv/virtualenv-13.1.0.tar.gz#md5=70f63a429b7dd7c3e10f6af09ed32554 > /pathtovirtualenvdownload/virtualenv-13.1.0.tar.gz # or latest
    curl https://pypi.python.org/packages/source/v/virtualenv/virtualenv-13.1.0.tar.gz.asc > /pathtovirtualenvdownload/virtualenv-13.1.0.tar.gz.asc # or latest
    mkdir /tmp/.gnupg
    chmod 700 /tmp/.gnupg
    gpg --homedir /tmp/.gnupg --keyserver hkps.pool.sks-keyservers.net --recv-keys 3372DCFA
    gpg --homedir /tmp/.gnupg --fingerprint 3372DCFA # check is 7C6B 7C5D 5E2B 6356 A926  F04F 6E3C BCE9 3372 DCFA
    gpg --homedir /tmp/.gnupg --verify /pathtovirtualenvdownload/virtualenv-13.1.0.tar.gz.asc
    tar xzf /pathtovirtualenvdownload/virtualenv-13.1.0.tar.gz --directory /pathtovirtualenvbin/
    echo "alias virtualenv='python  /pathtovirtualenvbin/virtualenv-13.1.0/virtualenv.py'" >> ~/.bashrc # or other shell start
    source ~/.bashrc # or other shell start

#### create a virtualenv 

    virtualenv /pathto/scrapyenv
    source /pathto/scrapyenv/bin/activate
    
#### install dependencies in virtualenv
    git clone https://github.com/davete/scrapyscrappers
    cd scrapyscrappers
    pip install -r requirements.txt

running
--------------

to list the scrappers:

    scrapy list

to run one of the scrappers

    scrapy crawl scrappername


