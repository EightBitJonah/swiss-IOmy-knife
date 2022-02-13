from operator import contains
import os,subprocess,time,pprint,re
from re import match

__location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__))) 
accessfile = open(os.path.join(__location__, '..','accesskey.txt'))
accesskey = accessfile.read()
secretfile = open(os.path.join(__location__, '..','secretkey.txt'))
secretkey = secretfile.read()
from tenable.io import TenableIO
tio = TenableIO(accesskey,secretkey)

def mescans():
    for scan in tio.scans.list():
        print(scan)

    return










