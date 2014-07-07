import urllib, urllib2, base64, urlparse, cgi, re, MySQLdb, cgitb, hashlib, binascii

 
#cgitb.enable()

db = MySQLdb.connect(host="mysql.mkron.net",
            user="kronapps",
            passwd="nemesistk421",
            db="mkronnet_apps")
cursor = db.cursor()

class urlCheck:    
    def __init__(self,url):
    	self.url = url
    	self.online = False
        self.content = self.getUrlContents()
        pass

    def getUrlContents(self):
        try:
            data = ''
            headers = { 'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.2.9) Gecko/20100824 Firefox/3.6.9 ( .NET CLR 3.5.30729; .NET CLR 4.0.20506)', 'Referer' : 'http://' + self.parsedUrl[1]}                
            print 'entrei'
            req = urllib2.Request(self.url, data, headers)
            response = urllib2.urlopen(req)
            return response.read()
        except Exception:
            pass
    