#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb, deprotectclass, re, hashlib, urlparse, base64, binascii, sys, urllib2, os, time
import logging

logger = logging.getLogger('dep')
hdlr = logging.FileHandler('/home/mkron/deprotect.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
fsock = open('/home/mkron/deprotect.log', 'a')
sys.stderr = fsock


#cgitb.enable()
# Create instance of FieldStorage 
form = cgi.FieldStorage() 

# Get data from fields
text = form.getvalue('data')

print "Content-type: text/html\n\n"


#protecao por uso em outro site
logger.info("--- Acessando URL antiga: deprotect.py: "+os.environ.get("HTTP_REFERER", "<not present>")+" - "+os.environ["REMOTE_ADDR"]+" - Metodo: "+os.environ['REQUEST_METHOD'])

time.sleep(180)

