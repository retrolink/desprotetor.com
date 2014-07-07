#!/usr/bin/python

import verifyclass, cgi, logging, sys, os

logger = logging.getLogger('dep')
hdlr = logging.FileHandler('/home/mkron/deprotect.log')
formatter = logging.Formatter('%(asctime)s %(levelname)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
fsock = open('/home/mkron/deprotect.log', 'a')
sys.stderr = fsock

form = cgi.FieldStorage() 

text = form.getvalue('url')

print "Content-type: text/html\n\n"

ref = os.environ.get("HTTP_REFERER", "<not present>")
if ref.find("desprotetor.com") == -1:
    logger.info("--- Referrer proibido - verify: "+ref)
    sys.exit(0)

if not os.environ['REQUEST_METHOD'] == 'POST':
    logger.info("--- Metodo proibido (get) - verify: "+os.environ.get("HTTP_REFERER", "<not present>"))
    sys.exit(0)


x = verifyclass.urlCheck(text)
if x.recognized:		
	if x.online == True:	
		if x.size == None:
			x.size = ""
		print str([1,x.size])		
		logger.info("URL ON: "+text+ " - size: "+x.size)
#		print x.name, x.description, x.size 
	if x.online == False:	
		print str([0])
		logger.info("URL OFF: "+text)
	if x.online == None:
		logger.error("----- verify.py - Logica desatualizada para: "+text)
