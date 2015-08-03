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


configuration
----------------------

Create a file named "keywords.txt" in the root of the project. Write every keyword in a new line or to use several keywords in the same request, write the keywords in the same line separated by an space.
The same applies to "locations.txt". If this file doesn't exist or doesn' have any locations, the requests will be perform without location.

To use several proxies, create a file named "proxies.json" inside of the data directory. The format is:

    [
       "http://ip1:port1",
       "http://ip2:port2"
    ]

In scrapyscrappers/settings.py, ensure that "USE_PROXY = True" and "FAHttpProxyMiddleware" is present in DOWNLOADER_MIDDLEWARES 

More about scrapyscrappers/settings.py: TBD
    
running
--------------

To list the scrappers:

    scrapy list

To run one of the scrappers

    scrapy crawl scrappername

To run one of the scrappers using keywords like command like argument and json file name like command line arguments:

    scrapy crawl scrappername -o json/scrappername.json -a keywords=python,ruby

currently is not possible to have a keyword composed by 2 (or more) words separated by spaces in the command line.
    
To run all the spiders from an script:

    run.py
    
