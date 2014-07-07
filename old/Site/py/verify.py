#!/usr/bin/python

import verifyclass, cgi, logging, sys, os
import security
import settings

logger = logging.getLogger('dep')
hdlr = logging.FileHandler(settings.application_log)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
fsock = open(settings.application_log, 'a')
sys.stderr = fsock

form = cgi.FormContent() 

text = form['url'][0]

print "Content-type: text/html\n\n"

#desabilitando para economizar recursos do dreamhost
sys.exit(0)


ref = os.environ.get("HTTP_REFERER", "<not present>")
security = security.checksec()
if security.valid != True:
    pass
    logger.error("::: SECURITY ::: verify.py - Motivo: "+security.error+". Ref: "+ref+" - IP: "+os.environ["REMOTE_ADDR"]+" - UA: "+os.environ.get("HTTP_USER_AGENT"))
    #print []
    #sys.exit(0)
else:    
    pass



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
