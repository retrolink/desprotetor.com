#!/usr/bin/python

import os, hashlib, datetime, cgi, Cookie

formGET = cgi.FormContent() 

now = datetime.datetime.now()


class checksec:    
    def __init__(self):   
        self.valid = False 
        self.error = None                
        try:
            self.passedKey = formGET['key'][0]
        except Exception:
            self.passedKey = None
        try:
            self.passedAuth = formGET['auth'][0]
        except Exception:
            self.passedAuth = None
        try:
            self.passedToken = formGET['token'][0]
        except Exception:
            self.passedToken = None                       
        
        self.ip = os.environ["REMOTE_ADDR"]
        self.salt = "andmaytheforcebewithyou"
        self.hour = now.hour

        h = hashlib.md5()
        h.update(str(self.ip)+self.salt+str(self.hour))
        self.token = h.hexdigest()


        h = hashlib.md5()
        h.update(str(self.ip)+self.salt+str(self.hour-1))
        self.tokenLastHour = h.hexdigest()



        if (self.passedKey != None) and (self.passedAuth != None) and (self.passedToken != None):            
            self.passedKey = self.passedKey.replace("z","0")
            self.passedKey = self.passedKey.replace("x","1")
            self.passedKey = self.passedKey.replace("u","2")
            self.passedKey = self.passedKey.replace("v","3")
            self.passedKey = self.passedKey.replace("y","4")
            self.passedKey = self.passedKey.replace("n","5")
            self.passedKey = self.passedKey.replace("m","6")
            self.passedKey = self.passedKey.replace("t","7")
            self.passedKey = self.passedKey.replace("s","8")
            self.passedKey = self.passedKey.replace("p","9")
            
            if (self.passedKey == self.token) or (self.passedKey == self.tokenLastHour):
            	self.valid = True
            else:
                self.error = "token nao foi igual ao esperado. Passed: "+self.passedKey+" Token: "+self.token+" TokenLastHour: "+self.tokenLastHour+" Auth: "+self.passedAuth
                self.valid = False
        else:
            self.error = "nao foi preenchido key, auth ou token"
            self.valid = False

        if self.valid:
            if os.environ.get("HTTP_REFERER", "not present").find("desprotetor.com") == -1:
                self.error = "referrer diferente de desprotetor.com"
                self.valid = False

        if self.valid:
            if not os.environ['REQUEST_METHOD'] == 'POST':
                self.error = "metodo diferente de POST"
                self.valid = False

        if self.valid:
            try:
                cookie = Cookie.SimpleCookie(os.environ["HTTP_COOKIE"])

                h = hashlib.md5()
                h.update(str(self.ip)+"salt")

                cookieexpected = h.hexdigest()
                if cookie["key"].value != "":
                    self.valid = True
                else:
                    self.error = "cookie com valor diferente: Passado: "+cookie["key"].value+" Esperado: "+cookieexpected
                    self.valid = False
            except (Cookie.CookieError, KeyError):
                #self.error = "cookie sem valor"
                #self.valid = False
                pass