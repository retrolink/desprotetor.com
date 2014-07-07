#!/usr/bin/python

import urllib, urllib2, base64, urlparse, cgi, re, MySQLdb, cgitb, hashlib, binascii
from BeautifulSoup import BeautifulSoup

db = MySQLdb.connect(host="mysql.mkron.net",
            user="kronapps",
            passwd="nemesistk421",
            db="mkronnet_apps")
cursor = db.cursor()

class urlCheck:    
    def __init__(self,url):        
        self.url = url            
        self.parsedUrl = urlparse.urlparse(url.strip())
        self.parsedQueryString = cgi.parse_qsl(self.parsedUrl[4])
        self.content = self.getUrlContents()
        self.recognized = False
        self.online = None    
        self.name = None
        self.description = None
        self.size = None
        self.run()

    def getUrlContents(self):
        try:
            data = ''
            headers = { 'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.2.9) Gecko/20100824 Firefox/3.6.9 ( .NET CLR 3.5.30729; .NET CLR 4.0.20506)', 'Referer' : 'http://' + self.parsedUrl[1]}                            
            req = urllib2.Request(self.url, data, headers)
            response = urllib2.urlopen(req)
            return response.read()
        except Exception:
            return None

    def getRegexStartFinish(self,data,patternstart,patternfinish):
        #encontra tudo entre duas strings, que estejam contidas em data  
        start = re.escape(patternstart)
        end = re.escape(patternfinish)        
        regexp = "((?<=("+start+")).*?(?=("+end+")))"        
        try:
            match = re.search(regexp,str(data))
            return match.group(0)
        except Exception:
            return None
        

    def run(self):
        if self.parsedUrl[1] == "www.megaupload.com":
            self.recognized = True
            try:
                soup = BeautifulSoup(self.content)
                data = soup.find('div', {"class":"down_txt_pad1"})                
                if data != None:
                    self.online = True
                    #self.name = soup.find('span', {"class":"down_txt2"}).string
                    #self.description = self.getRegexStartFinish(data,"description:</strong> ","<br />")
                    self.size = self.getRegexStartFinish(data,"size:</strong> ","<br />")
                else:
                    if self.content.find("Unfortunately") > -1:
                        self.online = False
            except Exception:
                pass

        if self.parsedUrl[1] == "www.fileserve.com":
            self.recognized = True            
            try:
                soup = BeautifulSoup(self.content)                
                data = soup.find('table', {"class":"timing"})                
                if data != None:
                    self.online = True
                    data = soup.find('div', {"class":"panel file_download"})
                    #self.name = self.getRegexStartFinish(data,"<h1>","<br /></h1>")
                    #self.description = None
                    self.size = self.getRegexStartFinish(data,"<span style=\"float:left\"><strong>","</strong>")
                else:                    
                    if self.content.find("File not available") > -1:                         
                        self.online = False
            except Exception:
                pass

        if self.parsedUrl[1].find("easy-share.com") > -1:
            self.recognized = True
            try:
                soup = BeautifulSoup(self.content)
                data = soup.find('h2', {"class":"px18 pb10"})                
                if data != None:
                    self.online = True                    
                    #self.name = self.getRegexStartFinish(data,"</span>","<span class=\"txtgray\">")
                    #self.description = None
                    self.size = self.getRegexStartFinish(data,"<span class=\"txtgray\">(",")</span>")                
            except Exception:
                if self.content == None: #retornou 404
                    self.online = False

        if self.parsedUrl[1] == "hotfile.com":
            self.recognized = True
            try:
                soup = BeautifulSoup(self.content)
                data = soup.find('div', {"class":"arrow_down"})                
                if data != None:
                    self.online = True
                    data = soup.find('div', {"class":"arrow_down"})
                    #self.name = self.getRegexStartFinish(data,"</strong> "," <span>")
                    #self.description = None
                    self.size = self.getRegexStartFinish(data,"</span> <strong>","</strong></div>")
                else:
                    if self.content.find("removed") > -1:
                        self.online = False
            except Exception:
                pass

        if self.parsedUrl[1] == "www.megavideo.com":
            self.recognized = True
            try:
                soup = BeautifulSoup(self.content)
                data = soup.find('div', {"id":"cinemamode"})                
                if data != None:
                    self.online = True                    
                    #self.name = self.getRegexStartFinish(data,"</strong> "," <span>")
                    #self.description = None
                    #self.size = self.getRegexStartFinish(data,"</span> <strong>","</strong></div>")
                else:
                    if self.content.find("st_note_bg1") > -1:
                        self.online = False
            except Exception:
                pass

        if self.parsedUrl[1] == "www.4shared.com":
            self.recognized = True
            try:
                soup = BeautifulSoup(self.content)
                data = soup.find('h2', {"id":"fileDescriptionText"})                
                if data != None:
                    self.online = True                    
                    data = soup.find('div', {"class":"small lgrey"})    
                    #self.name = self.getRegexStartFinish(data,"</strong> "," <span>")
                    #self.description = None
                    self.size = self.getRegexStartFinish(data,"title=\"Size: ","\">")
                else:
                    if self.content.find("not valid") > -1:
                        self.online = False
            except Exception:
                pass

        if self.parsedUrl[1] == "www.2shared.com":
            self.recognized = True
            try:
                soup = BeautifulSoup(self.content)
                data = soup.find('h1', {"class":"header"})                
                if data != None:
                    self.online = True                    
                    data = soup.find('div', {"class":"small lgrey"})    
                    #self.name = self.getRegexStartFinish(data,"</strong> "," <span>")
                    #self.description = None
                    self.size = self.getRegexStartFinish(self.content,"File size:</span>","&nbsp;")
                else:
                    if self.content.find("not valid") > -1:
                        self.online = False
            except Exception:
                pass
                                