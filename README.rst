######
PyEbox
######

TODO
####

* Add non offpeak account support

Installation
############

::

    pip install pyebox


Usage
#####

Print your current data

::

    pyebox -u MYACCOUNT -p MYPASSWORD


Print help

::

    pyebox -h
    usage: pyebox [-h] -u USERNAME -p PASSWORD [-j] [-t TIMEOUT]

    optional arguments:
      -h, --help            show this help message and exit
      -u USERNAME, --username USERNAME
                            EBox account
      -p PASSWORD, --password PASSWORD
                            Password
      -j, --json            Json output
      -t TIMEOUT, --timeout TIMEOUT
                            Request timeout

Dev env
#######

::

    virtualenv -p /usr/bin/python3.5 env
    pip install -r requirements.txt 
