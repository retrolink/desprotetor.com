from __future__ import with_statement  # pra rodar no python 2.5 velhao
import urllib
import urllib2
import base64
import urlparse
import re
import binascii
import logging
import simplejson

from settings import settings


logger_dbdata = logging.getLogger('data')
hdlr = logging.FileHandler(settings.data_log)
formatter = logging.Formatter('%(message)s')
hdlr.setFormatter(formatter)
logger_dbdata.addHandler(hdlr)
logger_dbdata.setLevel(logging.INFO)


logger_dbdata.info("ba")


class UrlDeprotect:
    """generic methods for deprotecting urls"""
    def __init__(self, url):
        #setting things up
        self.url = url
        self.originalurl = url
        self.decoded = False
        self.decoded_url = ''
        self.decode_method = ''
        self.content = ''
        self.valid = True
        self.invalid_rls = list()
        self.extension = ""

        #parsing url
        self.parsed_url = urlparse.urlparse(url.strip())
        self.parsed_query_string = urlparse.parse_qsl(self.parsed_url[4])

        if (self.parsed_url[2] == "" or self.parsed_url[2] == "/") and self.parsed_url[4] == "":
            self.valid = False

    def get_url_contents(self):
        data = ''
        headers = {'User-Agent':
                   'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                   'Chrome/35.0.1916.114 Safari/537.36',
                   'Referer': 'http://' + self.parsed_url[1]}
        try:            
            req = urllib2.Request(self.url, data, headers)
            response = urllib2.urlopen(req)
            return response.read()
        except Exception, e:
            if str(e) == "HTTP Error 405: Method Not Allowed":
                data = None
                req = urllib2.Request(self.url, data, headers)
                response = urllib2.urlopen(req)
                return response.read()          

    def post_url_contents(self, data):
        data = urllib.urlencode(data)
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows; Gecko/20100824 Firefox/3.6.9 ',
            'Referer': 'http://' + self.parsed_url[1]}
        try:            
            req = urllib2.Request(self.url, data, headers)
            response = urllib2.urlopen(req)
            return response.read()
        except Exception, e:
            if str(e) == "HTTP Error 405: Method Not Allowed":
                data = None
                req = urllib2.Request(self.url, data, headers)
                response = urllib2.urlopen(req)
                return response.read()       

    def check_correct(self, url):
        correct = False
        correct_protocols = ["http", "https"]
        if url.startswith("http"):
            for protocol in correct_protocols:
                if url.startswith(protocol+":/"):  # comecou certo
                    if not url.startswith(protocol+"://"):  # arrumar uma barra so
                        url = url.replace(protocol+":/", protocol+"://")
                    correct = True
                    
        if correct:
            if len(self.invalid_rls) > 0:
                for invalidUrl in self.invalid_rls:
                    if url.startswith(invalidUrl):
                        correct = False

        if correct:
            self.decoded = True
            try:
                self.decoded_url = str(url)
            except UnicodeEncodeError:
                self.decoded_url = url.encode("ascii", "ignore")

        return correct

    @staticmethod
    def base64decodefix(string):
        if string.endswith("/"):
            string = string[:-1]
        try:
            string = base64.decodestring(string)
        except Exception:            
            string += "="
            try:
                string = base64.decodestring(string)
            except Exception:
                string += "="
                try:
                    string = base64.decodestring(string)
                except Exception:                
                    pass
        return string  

    def find_simple_url(self, string):
        if self.check_correct(string):
            self.decode_method = 'simple'
            return True
        else:
            return False

    def decode_base64(self, string):
        try:            
            string = self.base64decodefix(string)           
        except Exception:
            pass
        if self.check_correct(string):
            self.decode_method = 'base64'
            return True
        else:
            return False

    def decode_double_base64(self, string):
        try:
            string = self.base64decodefix(string)
            string = self.base64decodefix(string)
        except Exception:
            pass
        if self.check_correct(string):
            self.decode_method = 'double base64'
            return True
        else:
            return False

    def decode_base64_then_reverse(self, string):
        #remove trailing slash se houver, e tenta adicionar padding characters a string base64
        try:
            string = self.base64decodefix(string)
        except Exception:            
            pass
        string = string[::-1]
        if self.check_correct(string):
            self.decode_method = 'base 64 then reverse'
            return True
        else:
            return False

    def decode_reverse(self, string):
        string = string[::-1]
        if self.check_correct(string):
            self.decode_method = 'reverse'
            return True
        else:
            return False

    def decode_unescape(self, string):
        string = urllib.unquote(string)        
        if self.check_correct(string):
            self.decode_method = 'unescape'
            return True
        else:
            return False

    def decode_double_unescape(self, string):
        string = urllib.unquote(string)
        string = urllib.unquote(string)        
        if self.check_correct(string):
            self.decode_method = 'double unescape'
            return True
        else:
            return False

    def decode_hex(self, string):
        try:
            if len(string) % 2 > 0:
                string = string[:-1]
            string = binascii.unhexlify(string)
        except Exception:
            pass
        if self.check_correct(string):
            self.decode_method = 'hex unencode'
            return True
        else:
            return False

    #passa por todos os metodos de decode, tentando desproteger 'string'
    def decode_full(self, string):
        if not self.decoded:
            if self.find_simple_url(string):
                return True

        if not self.decoded:
            if self.decode_base64(string):
                return True

        if not self.decoded:
            if self.decode_reverse(string):
                return True

        if not self.decoded:
            if self.decode_base64_then_reverse(string):
                return True                    

        if not self.decoded:
            if self.decode_double_base64(string):
                return True  

        if not self.decoded:
            if self.decode_unescape(string):
                return True  

        if not self.decoded:
            if self.decode_double_unescape(string):
                return True  

        if not self.decoded:
            if self.decode_hex(string):
                return True  

    #testa todos os parametros GET da url contra metodos de decode ja criados
    #precisa ser sempre o ultimo metodo a ser chamado, ja que pode ter excecoes antes, e nao entregar o valor correto
    #ex: http://www.celularbr.com/seven/?NP129KKT=d?/moc.daolpuagem.www//:ptth
    def deprotect_simple_query_string(self):
        if len(self.parsed_url[1]) > 0:
            for s in self.parsed_query_string:
                query_string_value = s[1]
                if self.decode_full(query_string_value):
                    if self.decoded_url.endswith("?d") or self.decoded_url.endswith("?v"):
                        self.decoded = False
                        self.decoded_url = ''
                        self.decode_method = ''
                    else:
                        self.decode_method = 'simple query string ++ ' + self.decode_method
                        return True
    
    #testa querystring direto, no caso de /?valor
    def deprotect_querystring_without_param_name(self):
        if self.url.find(":ptth") == -1:
            if self.decode_full(self.parsed_url[4]):
                self.decode_method = 'query without param ++ ' + self.decode_method
                return True

    #testa string depois de separator, position pode ser first ou last
    def deprotect_string_after_separator(self, separator, position):
        string = ""
        if position == "first":
            string = self.url            
            string = string.partition(separator)            
            string = string[2]
        if position == "last":   
            string = self.url         
            string = string.rpartition(separator)
            string = string[2]            

        if self.decode_full(string):
            self.decode_method = 'string after separator ++ ' + self.decode_method
            return True

    #testa string depois de um determinado numero de caracteres
    def deprotect_string_after_distance(self, distance):
        string = self.url
        string = string[distance:]
        if self.decode_full(string):
            self.decode_method = 'string after separator ++ ' + self.decode_method
            return True

    def get_url_and_run_regex(self, pattern):
        string = ''
        try:
            self.content = self.get_url_contents()
            match = re.search(pattern, self.content)
            string = match.group(0)
        except Exception, e:
            pass
        if self.check_correct(string):
            self.decode_method = 'get url + regex'
            return True

    def get_changed_url_and_run_regex(self, patternsearch, patternreplace, patternregex):
        string = ''
        try:
            self.url = self.url.replace(patternsearch, patternreplace)
            self.content = self.get_url_contents()
            match = re.search(patternregex, self.content)
            string = match.group(0)
        except Exception:
            pass
        if self.check_correct(string):
            self.decode_method = 'get changed url + regex'
            return True
            
    def insert_db_success(self):
        data = dict()
        data["type"] = 1  # desprotecao
        data["success"] = 1  # bem sucedida
        data["originalUrl"] = self.originalurl
        data["decoded_url"] = self.decoded_url
        data["domain"] = self.parsed_url[1]
        data["method"] = self.decode_method
        data["extension"] = self.extension
        logger_dbdata.info(simplejson.dumps(data))

    def insert_db_failure(self):
        if self.originalurl.startswith("http"):
            data = dict()
            data["type"] = 1  # desprotecao
            data["success"] = 0  # mal sucedida
            data["originalUrl"] = self.originalurl
            data["domain"] = self.parsed_url[1]
            data["extension"] = self.extension
            logger_dbdata.info(simplejson.dumps(data))

    def get_db_answer(self):
        domain = self.parsed_url[1]
        with open(settings.answer_json_file, 'r') as f:
            read_data = f.read()
            data = simplejson.loads(read_data)
        
        for url in data:
            if url[0] == domain:
                return url

        return False