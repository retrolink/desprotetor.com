import urllib, urllib2, base64, urlparse, cgi, re, MySQLdb, cgitb, hashlib, binascii

 
#cgitb.enable()

try:
    db = MySQLdb.connect(host="mysql.mkron.net",user="kronapps",passwd="nemesistk421",db="mkronnet_apps")
    cursor = db.cursor()
except Exception:
    pass

class UrlDeprotect:
    """generic methods for deprotecting urls"""
    def __init__(self,url):
        #setting things up
        self.url = url
        self.originalurl = url
        self.decoded = False
        self.decodedUrl = ''
        self.valid = True
        self.invalidUrls = list()

        #parsing url
        self.parsedUrl = urlparse.urlparse(url.strip())                
        #using cgi.parse_qsl instead of urllib.parse_qsl because of python 2.5 on dreamhost
        self.parsedQueryString = cgi.parse_qsl(self.parsedUrl[4])        

        if (self.parsedUrl[2] == "" or self.parsedUrl[2] == "/") and self.parsedUrl[4] == "":
            self.valid = False

    def getUrlContents(self):
        try:
            data = ''
            headers = { 'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.2.9) Gecko/20100824 Firefox/3.6.9 ( .NET CLR 3.5.30729; .NET CLR 4.0.20506)', 'Referer' : 'http://' + self.parsedUrl[1]}                
            req = urllib2.Request(self.url, data, headers)
            response = urllib2.urlopen(req)
            return response.read()
        except Exception:
            pass

    def checkCorrect(self,url):
        correct = False
        correctProtocols = ["http","https"]
        if url.startswith("http"):
            for protocol in correctProtocols:                
                if url.startswith(protocol+":/"): #comecou certo                    
                    if not url.startswith(protocol+"://"): #arrumar uma barra so                                
                        url = url.replace(protocol+":/",protocol+"://") #so posso substituir a primeira ocorrencia, arrumar depois                        
                    correct = True
                    
        if correct:            
            if len(self.invalidUrls) > 0:                              
                for invalidUrl in self.invalidUrls:
                    if url.startswith(invalidUrl):
                        correct = False

        if correct:
            self.decoded = True
            self.decodedUrl = str(url)
        return correct







    

    def base64decodefix(self,string):
        if string.endswith("/"):
            string = string[:-1]
        try:
            string = base64.decodestring(string)
        except Exception:            
            string = string + "="
            try:
                string = base64.decodestring(string)
            except Exception:
                string = string + "="
                try:
                    string = base64.decodestring(string)
                except Exception:                
                    pass
        return string  

    def findSimpleUrl(self,string):
        if self.checkCorrect(string):        
            self.decodeMethod = 'simple'            
            return True
        else:
            return False

    def decodeBase64(self,string):        
        try:            
            string = self.base64decodefix(string)           
        except Exception:
            pass
        if self.checkCorrect(string):                    
            self.decodeMethod = 'base64'
            return True
        else:
            return False

    def decodeDoubleBase64(self,string):
        try:
            string = self.base64decodefix(string)
            string = self.base64decodefix(string)
        except Exception:
            pass
        if self.checkCorrect(string):            
            self.decodeMethod = 'double base64'
            return True
        else:
            return False

    def decodeBase64ThenReverse(self,string):
        #remove trailing slash se houver, e tenta adicionar padding characters a string base64
        #TODO: colocar essa mecanica num metodo isolado e aplica-lo a todos os base64        
        try:
            string = self.base64decodefix(string)
        except Exception:            
            pass
        string = string[::-1]
        if self.checkCorrect(string):            
            self.decodeMethod = 'base 64 then reverse'
            return True
        else:
            return False

    def decodeReverse(self,string):
        string = string[::-1]
        if self.checkCorrect(string):            
            self.decodeMethod = 'reverse'
            return True
        else:
            return False

    def decodeUnescape(self,string):
        string = urllib.unquote(string)        
        if self.checkCorrect(string):            
            self.decodeMethod = 'unescape'            
            return True
        else:
            return False

    def decodeDoubleUnescape(self,string):
        string = urllib.unquote(string)
        string = urllib.unquote(string)        
        if self.checkCorrect(string):            
            self.decodeMethod = 'double unescape'            
            return True
        else:
            return False

    def decodeHex(self,string):                
        try:
            if len(string)%2 > 0:
                string = string[:-1]
            string = binascii.unhexlify(string)
        except Exception, e:
            #print str(e)
            pass
        if self.checkCorrect(string):            
            self.decodeMethod = 'hex unencode'            
            return True
        else:
            return False

                
    #passa por todos os metodos de decode, tentando desproteger 'string'
    def decodeFull(self,string):
        if not self.decoded:
            if self.findSimpleUrl(string):
                return True

        if not self.decoded:
            if self.decodeBase64(string):
                return True

        if not self.decoded:
            if self.decodeReverse(string):
                return True

        if not self.decoded:
            if self.decodeBase64ThenReverse(string):
                return True                    

        if not self.decoded:
            if self.decodeDoubleBase64(string):
                return True  

        if not self.decoded:
            if self.decodeUnescape(string):
                return True  

        if not self.decoded:
            if self.decodeDoubleUnescape(string):
                return True  

        if not self.decoded:
            if self.decodeHex(string):
                return True  

                        
    #testa todos os parametros GET da url contra metodos de decode ja criados
    #precisa ser sempre o ultimo metodo a ser chamado, ja que pode ter excecoes antes, e nao entregar o valor correto
    #ex: http://www.celularbr.com/seven/?NP129KKT=d?/moc.daolpuagem.www//:ptth
    def deprotectSimpleQueryString(self):
        if len(self.parsedUrl[1]) > 0:
            for s in self.parsedQueryString:
                queryStringValue = s[1]             
                if self.decodeFull(queryStringValue):
                    if self.decodedUrl.endswith("?d") or self.decodedUrl.endswith("?v"):
                        self.decoded = False
                        self.decodedUrl = ''
                        self.decodeMethod = ''                        
                    else:
                        self.decodeMethod = 'simple query string ++ ' + self.decodeMethod
                        return True
    
    #testa querystring direto, no caso de /?valor
    def deprotectQueryStringWithoutParamName(self):
        if self.url.find(":ptth") == -1:
            if self.decodeFull(self.parsedUrl[4]):
                self.decodeMethod = 'query without param ++ ' + self.decodeMethod
                return True

    #testa string depois de separator, position pode ser first ou last
    def deprotectStringAfterSeparator(self,separator,position):
        if position == "first":
            string = self.url            
            string = string.partition(separator)            
            string = string[2]
        if position == "last":   
            string = self.url         
            string = string.rpartition(separator)
            string = string[2]            

        if self.decodeFull(string):
            self.decodeMethod = 'string after separator ++ ' + self.decodeMethod
            return True

    #testa string depois de um determinado numero de caracteres
    def deprotectStringAfterDistance(self,distance):
        string = self.url
        string = string[distance:]
        if self.decodeFull(string):
            self.decodeMethod = 'string after separator ++ ' + self.decodeMethod
            return True

    def getUrlAndRunRegex(self,pattern):
        string = ''
        try:
            self.content = self.getUrlContents()
            match = re.search(pattern,self.content)
            string = match.group(0)            
        except Exception:
            pass
        if self.checkCorrect(string):            
            self.decodeMethod = 'get url + regex'            
            return True

    def getChangedUrlAndRunRegex(self,patternsearch,patternreplace,patternregex):                
        string = ''
        try:
            self.url = self.url.replace(patternsearch,patternreplace)        
            self.content = self.getUrlContents()
            match = re.search(patternregex,self.content)
            string = match.group(0)            
        except Exception:
            pass
        if self.checkCorrect(string):            
            self.decodeMethod = 'get changed url + regex'            
            return True
            
    def insertDbSuccess(self):
        hash = self.parsedUrl[1] + self.decodeMethod
        m = hashlib.md5()
        m.update(hash)
        hash = m.hexdigest()        
        query = """INSERT INTO deprotect_py_success_data (hash,domain,method,num) VALUES ('""" + hash + """','""" + self.parsedUrl[1] + """','""" + self.decodeMethod + """',1) ON DUPLICATE KEY UPDATE num = num +  VALUES(num);"""        
        db.query(query)
        query = """INSERT INTO deprotect_py_success_urls (url,result,date) VALUES ('""" + self.originalurl + """','""" + self.decodedUrl + """',DATE_ADD(NOW(),INTERVAL 6 HOUR));"""        
        db.query(query)        
        r = db.store_result()

    def insertDbFailure(self):  
        if self.originalurl.startswith("http:/"):            
            query = """INSERT INTO deprotect_py_fail (domain,url) VALUES ('"""+ self.parsedUrl[1] +"""', '""" + self.originalurl + """');"""        
            db.query(query)        
            r = db.store_result()

    def getDbAnswer(self):            
            query = """select domain,answer,log_as_fail from deprotect_py_answer where domain = '"""+ self.parsedUrl[1] + """'"""
            numRows = cursor.execute(query)
            if numRows > 0:
                data = cursor.fetchone()       
                return data
            else:
                return False
