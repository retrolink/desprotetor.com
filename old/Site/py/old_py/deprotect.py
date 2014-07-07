#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb, deprotectclass, re, hashlib, urlparse, base64, binascii, sys, urllib2, os
from BeautifulSoup import BeautifulSoup
from deprotectclass import UrlDeprotect
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

if cgi.escape(os.environ["REMOTE_ADDR"]) == "50.30.32.37":
    logger.info("--- Endereco ip proibido. "+os.environ["REMOTE_ADDR"])
    sys.exit(0)

if cgi.escape(os.environ["REMOTE_ADDR"]) == "109.169.63.141":    
    logger.info("--- Endereco ip proibido. "+os.environ["REMOTE_ADDR"])
    sys.exit(0)
        
ref = os.environ.get("HTTP_REFERER", "<not present>")
if ref.find("desprotetor.com") == -1:
    logger.info("--- Referrer proibido: "+ref+" - "+os.environ["REMOTE_ADDR"])
    sys.exit(0)

if not os.environ['REQUEST_METHOD'] == 'POST':
    logger.info("--- Metodo proibido (get): "+os.environ.get("HTTP_REFERER", "<not present>")+" - "+os.environ["REMOTE_ADDR"])
    sys.exit(0)




    
#if cgi.escape(os.environ["REMOTE_ADDR"]) == "187.108.192.21":
#    print "to te vendo. =)"
#    sys.exit(0)




success = False
try:
    list = text.split("\n")
except Exception:
    sys.exit(0)

for s in list:   
    s = s.strip().replace("\'","").replace("\"","")    
    #logger.info("Desprotegendo URL: "+s)
    if not s == '':
             
        x = deprotectclass.UrlDeprotect(s)
            
        #string apos separador definido
        if not x.decoded:
            exceptions = {        
            "filmeslegendados.info":"/?",
            "yess.me":"/ir/id/",            
            "www.megafilmesbr.com":"go.php?",
            "www.downloads-completos.info":"go.php?",
            "www.celularbr.com":"/?",
            "www.brasildowns.com.br":"/?Z28h",
            "www.evolutionsurf.net":"/?",
            "www.baixebr.org":"/?",            
            "protegerlinks.com":"/?",
            "clickgratis.org":"ir/id/",
            "linkprotegido.awardspace.biz":"?url*",
            "ftp.marciobgf.com":"/?",
            "www.tudofull.com":"/?",
            "baixakifilmes.info":"/?",
            "www.apgfamily.com":"/?",
            "www.protetordelinksja.net":"?down!",
            "linkprotegido.biz":"?link",
            "www.downloadsemcontrole.org":"/?",
            "www.monitordownloads.net":"cm.php?",
            "www.baixarfilmesdublados.info":"?down!",
            "playcelular.net":"/?",
            "www.planetadownloads.com":"/?/",
            "dualfilmes.com":"/link=",
            "brfreestylepes.forumeiros.com":"go/",
            "protelink.info":"id/",
            "www.planetadownloads.com":"/?",
            "www.wejte.com":"/?",
            "www.downsupremo.com":"?url=#",
            "filmeseseriadosgratis.com":"/?",
            "protegerlinks.net":"?go%21",
            "www.baixeaquifilmes.com":"/?",
            "www.downloadfilmespornos.com":"/?",
            "www.downloadsgratis.us":"?down!",
            "www.elitedosfilmes.com":"/?",
            "www.freefilmeseseries.com":"/?",
            "www.protetordownloads.info":"/?",
            "www.liberadosfree.info":"/?",
            "www.cdscompletos.org":"protetor/",
            "www.topwebgratis.com":"?down!",
            "www.loucosporsoftwares.com":"?go%21",
            "jackao.net":"putaria/",
            "www.downloadsdegraca.com":"continuar/",
            "telona.biz":"/?",
            "topcine.net":"/?",
            "www.baixarfilme.info":"/?",
            "www.girodiario.com":"/?",            
            "www.musicasdegraca.com":"/?",
            "www.protetordelink.gospeldownloads.us":"/?",
            "www.puxandocompleto.com":"/?",
            "www.redirecionamentodeurl.com":"/?",
            "www.romsup.com":"/?",
            "www.somcristao.com":"/?",
            "www.emurama.com":"protetor/?",
            "www.gospelgratis.org":"protetor/",
            "www.quick-downloads.com":"protetorrr/?",
            "topcine.net":"ABC123CBA",
            "protetor.downloadcdsgratis.com":"?url=",
            "somniu.net":"?url$"
            }
            if exceptions.has_key(x.parsedUrl[1]):
                    x.deprotectStringAfterSeparator(exceptions[x.parsedUrl[1]],"first")

        #string apos separador definido -- caso alguem da lista de cima tenha mais de um metodo
        if not x.decoded:
            exceptions = {                    
            "www.brasildowns.com.br":"/?",
            "www.emurama.com":"protetor2/?"
            }
            if exceptions.has_key(x.parsedUrl[1]):
                    x.deprotectStringAfterSeparator(exceptions[x.parsedUrl[1]],"first")

        #string apos ultimo separador definido
        if not x.decoded:
            exceptions = {                    
            "protetordelink.tv":"/"            
            }
            if exceptions.has_key(x.parsedUrl[1]):
                x.deprotectStringAfterSeparator(exceptions[x.parsedUrl[1]],"last")                                    
                      
                        
        #string apos separador go! que eh bastante comum
        if not x.decoded:        
            if x.url.find("go!") > -1:        
                x.deprotectStringAfterSeparator("go!","first")

        #string apos separador /download/? que eh bastante comum
        if not x.decoded:        
            if x.url.find("/download/?") > -1:        
                x.deprotectStringAfterSeparator("/download/?","first")

        #string apos separador ?down! que eh bastante comum
        if not x.decoded:        
            if x.url.find("?down!") > -1:        
                x.deprotectStringAfterSeparator("?down!","first")

        #remover valor da string, e entao tratar normalmente depois de separador
        if not x.decoded:      
            exceptions = {                    
            "link.baixedetudo.net":[".url",".net/"],
            "superdownsmega.paginadedownload.info":[".url",".info/"],
            "protetor.clubedodownload.info":[".url",".info/"]
            }
            if exceptions.has_key(x.parsedUrl[1]):     
                x.url = x.url.replace("#","")                                           
                x.url = x.url.replace(exceptions[x.parsedUrl[1]][0], "")                
                x.deprotectStringAfterSeparator(exceptions[x.parsedUrl[1]][1],"first")
                    
        #string depois de uma certa distancia
        #http://protetordelinks.cont.us/p/9ba0f0f0215e92058fbb2be528c364a9/aHR0cDovL3d3dy5tZWdhdXBsb2FkLmNvbS8/ZD1JUkc0TzA4Ug==
        if not x.decoded:
            exceptions = {
            "protetordelinks.cont.us":66
            }
            if exceptions.has_key(x.parsedUrl[1]):
                x.deprotectStringAfterDistance(exceptions[x.parsedUrl[1]])
    
        #string depois de um numero de ocorrencias de uma outra string
        #http://protetordelinks.cont.us/p/9ba0f0f0215e92058fbb2be528c364a9/aHR0cDovL3d3dy5tZWdhdXBsb2FkLmNvbS8/ZD1JUkc0TzA4Ug==
        #depois do 3o. / no path
        if not x.decoded:
            exceptions = {
            "protetordelinks.cont.us":[3,"/"]
            }
            if exceptions.has_key(x.parsedUrl[1]):
                num = exceptions[x.parsedUrl[1]][0]
                sep = exceptions[x.parsedUrl[1]][1]
                a = 1
                pos = 0
                while a <= num:    
                    #print x.parsed_url[2], sep, pos
                    pos = x.parsedUrl[2].find(sep,pos)
                    pos = pos+1
                    a = a+1
                x.decodeFull(x.parsedUrl[2][pos:])
                                    

        #apenas um dos parametros GET possui a URL, o resto eh decoy
        if not x.decoded:
            exceptions = {                    
            "36.baixevipdown.net":"url"
            }
            if exceptions.has_key(x.parsedUrl[1]):                    
                    for s in x.parsedQueryString:
                        if s[0] == exceptions[x.parsedUrl[1]]:
                            x.decodeFull(s[1])
                    #x.deprotect_string_after_separator(exceptions[x.parsed_url[1]],"first")


                                                    


        #informacao nao esta na url - pegar conteudo da pagina e parsear via regex
        if not x.decoded:
            #dominio:regex
            exceptions = {
            "adf.ly":"((?<=(var url\ \=\ \'))http.*?(?=(')))",
            "www.pqueno.com":"((?<=\<a href\=\')http.*?(?=(\' onMouseDown)))",
            "osfilmes.com":"((?<=location.href\=\')http.*?(?=(\')))",
            "www.promocoesdeprodutos.com":"((?<=(\<a href\=\"))http.*?(?=(\" onclick)))",
            "filmesmegavideo.net":"((?<=(\<a href\=\"))http\:\/\/assistir.*?(?=(\" rel)))",
            "www.linkproteger.com":"((?<=(a href\=\"))http.*?(?=(\" onclick\=)))",
            "linkbee.com":"((?<=(linkurl\' href\=\"))http.*?(?=(\")))",
            "linkbucks.com":"((?<=TargetUrl = \')http.*?(?=(\';)))",
            "www.lockurl.org":"((?<=(\(\'linkk0\'\)\.href\=\"))http.*?(?=(\";)))",
            "www.linkproteger.com":"((?<=(divDLStart\"><a href=\"))http.*?(?=(\" onclick)))",
            "topfilmes.com.br":"((?<=(innerHTML\=\'\<a\ href\=\"))http.*?(?=(\")))",
            "www.protetorlink.com":"((?<=(\<a\ href\=\"))http.*?(?=(\"\ target\=\"\_blank\"\>\<img\ src\=\")))",
            "link-protector.com":"((?<=(name\=\"Continue\"\ onClick\=\"window\.location\=\'))http.*?(?=(\'\")))",
            "linkproteger.com":"((?<=(divDLStart\"\>\<a\ href\=\"))http.*?(?=(\"\ onclick\=\")))",
            "linkprotegido.info":"((?<=(url\=\"))http.*?(?=(\"\>)))"              
            }
            if exceptions.has_key(x.parsedUrl[1]):
                x.getUrlAndRunRegex(exceptions[x.parsedUrl[1]])

        #informacao nao esta na url - alterar url e pegar conteudo da pagina para parsear via regex
        #este eh uma excecao do caso de baixo, arrumar
        if not x.decoded:
            #'dominio':['pattern search','pattern replace','regex buscar']
            exceptions = {
            "www.protetorlink.com":["cdsmusicasgratis/","cdsmusicasgratis/go/","((?<=URL\=)http.*?(?=(\"\>)))"]            
            
            }
            if exceptions.has_key(x.parsedUrl[1]):            
                x.getChangedUrlAndRunRegex(exceptions[x.parsedUrl[1]][0],exceptions[x.parsedUrl[1]][1],exceptions[x.parsedUrl[1]][2])
                    
    
        
        #informacao nao esta na url - alterar url e pegar conteudo da pagina para parsear via regex
        if not x.decoded:
            #'dominio':['pattern search','pattern replace','regex buscar']
            exceptions = {
            "www.protetorlink.com":[".com",".com/go","((?<=URL\=)http.*?(?=(\"\>)))"],
            "upmirror.com":[".com/",".com/intervencao.php?key=","((?<=(\<a href\=\"))http.*?(?=(\"\>)))"],
            "www.assistirfilmesonline.net":[".net/pub-",".net/","((?<=(value\=\"))http.*?(?=(\<param)))"],
            "assistirfilmesonline.net":[".net/pub-",".net/","((?<=(value\=\"))http.*?(?=(\<param)))"],
            "www.megafilmes.net":[".net/pub-",".net/","((?<=(value\=\"))http.*?(?=(\")))"],
            "www.assistirporno.net":[".net/pub-",".net/","((?<=(value\=\"))http.*?(?=[(\")(\<)]))"]
            
            }
            if exceptions.has_key(x.parsedUrl[1]):            
                x.getChangedUrlAndRunRegex(exceptions[x.parsedUrl[1]][0],exceptions[x.parsedUrl[1]][1],exceptions[x.parsedUrl[1]][2])


        #na query string sem parametros
        #desativado para URLs invertidas
        # http://www.celularbr.com/seven/?NP129KKT=d?/moc.daolpuagem.www//:ptth
        if not x.decoded:
            x.deprotectQueryStringWithoutParamName()
        
        #-----------------------------
        #metodos completamente customizados para casos estranhos
        #-----------------------------
        
        #inverter e remover string da URL
        if not x.decoded:
            exceptions = {
            "www.linkstw.com":"Z@E$",
            "filmeseserieshd.com":"Z@E$"
            }
            if exceptions.has_key(x.parsedUrl[1]):
                x.url = x.url.replace(exceptions[x.parsedUrl[1]], "")
                x.parsedUrl = urlparse.urlparse(x.url.strip())
                x.parsedQueryString = cgi.parse_qsl(x.parsedUrl[4])
                x.deprotectSimpleQueryString()
                x.decodeMethod = "custom simple param"        

        #url com pares e impares
        if not x.decoded:
            exceptions = {
            "protetor.downloadcdsgratis.com":"?url="
            }
            if exceptions.has_key(x.parsedUrl[1]):                
                string = x.url            
                string = string.replace("&t=2","")
                string = string.partition(exceptions[x.parsedUrl[1]])            
                string = string[2]

                l = len(string)
                a = 1
                b = ""
                while a<l:
                    b = b+string[a]
                    a = a+2
                if l%2 == 1:
                    l = l-1
                    b = b+string[l]

                while l > 0:
                    l = l-2
                    b = b+string[l]
                string = b
                if string.startswith("http:/"):
                    x.decoded = True
                    x.decodedUrl = string
                    x.decodeMethod = "custom decode even/odd" 


        #furiagames.org -- apenas um dos parametros GET possui a URL, o resto eh decoy
        if not x.decoded:
            exceptions = {                    
            "furiagames.org":"laospqwsado4512asd1",
            "baixai.net":"laospqwsado4512asd1",
            "furiagames360.org":"laospqwsado4512asd1"            
            }
            if exceptions.has_key(x.parsedUrl[1]):                    
                    for s in x.parsedQueryString:
                        if s[0] == exceptions[x.parsedUrl[1]]:
                            string = s[1]                            
                            try:
                                string = binascii.unhexlify(string)
                                string.replace("?","")
                                string = base64.decodestring(string)
                                string = binascii.unhexlify(string)
                            except Exception:
                                pass
                            if string.startswith("http:/"):
                                x.decoded = True
                                x.decodedUrl = string
                                x.decodeMethod = "custom decode hex base64 hex"   


        #www.vinxp.com -- babacas que fazem transformacoes em sequencia e substituicoes bobas, hackeavel
        if not x.decoded:
            exceptions = {                    
            "www.vinxp.com":"id"
            }
            if exceptions.has_key(x.parsedUrl[1]):                    
                    for s in x.parsedQueryString:
                        if s[0] == exceptions[x.parsedUrl[1]]:
                            string = s[1]                            
                            try:
                                string = binascii.unhexlify(string)
                                string = string[::-1]
                                string = base64.decodestring(string)
                                string = string[::-1]
                                string = binascii.unhexlify(string)
                                string = string[::-1]
                            except Exception:
                                pass

                            string = string.replace("_FX01", "a")
                            string = string.replace("_BX02", "e")
                            string = string.replace("_TX03", "i")
                            string = string.replace("_PM04", "o")
                            string = string.replace("_FL05", "u")
                            string = string.replace("_KH06", "http://")
                            string = string.replace("_QK07", "www")
                            string = string.replace("_YL08", ".")
                            string = string.replace("_YT09", ".com")
                            string = string.replace("_PX10", "/?")
                            if string.startswith("http:/"):
                                x.decoded = True
                                x.decodedUrl = string
                                x.decodeMethod = "custom decode hex base64 hex"   


        #inverter, base64, pegar o resultado e traduzir o ascii (documentacao dizia que era unicode -- mesmo resultado de javascript: fromCharCode)
        if not x.decoded:
            exceptions = [
            "www.nixlove.com"            
            ]
            if x.parsedUrl[1] in exceptions:  
                string = x.url
                string = string.rpartition("/")
                string = string[2]                 

                string = string[::-1]
                try:
                    string = base64.decodestring(string)
                except Exception:
                    pass
                
                list = [string[i:i+3] for i in range(0, len(string), 3)]
                result = ""
                for l in list:
                    result = result + chr(int(l))
                
                if result.startswith("http:/"):
                    x.decoded = True
                    x.decodedUrl = result
                    x.decodeMethod = "custom decode electron_encode crypt"   


        #traducao letra a letra
        if not x.decoded:
            exceptions = [
            "www.protetor.org"            
            ]
            if x.parsedUrl[1] in exceptions:  
                string = x.url
                dicio = {
                "a":"l",
                "b":"6",
                "c":"j",
                "d":"1",
                "e":"b",
                "f":"2",
                "g":".",
                "h":"x",
                "i":"8",
                "j":"e",
                "k":"u",
                "l":"n",
                "m":"h",
                "n":"i",
                "o":"9",
                "p":"f",
                "q":"5",
                "r":"-",
                "s":"7",
                "t":"m",
                "u":"/",
                "v":"_",
                "w":"0",
                "x":"o",
                "y":"4",
                "z":"a",
                "0":"c",
                "1":"q",
                "2":"v",
                "3":"w",
                "4":"t",
                "5":"y",
                "6":"r",
                "7":"p",
                "8":"w",
                "9":":",
                ".":"s",
                "-":"d",
                ":":"g",
                "?":"?",
                "-":"d",
                "=":"=",
                "/":"z",
                "_":"k",
                "%":"3"}
                string = string.rpartition("?h=")
                stri = string[2]     
                lista = [c for c in stri]           
                #lista = list("asd")
                #print lista
                result = ""
                for char in lista:
                    result = result + dicio[char]
                if result.startswith("http:/"):
                    x.decoded = True
                    x.decodedUrl = result
                    x.decodeMethod = "custom decode rotate char"   

        #resolver e adicionar http:// no final
        if not x.decoded:
            exceptions = [
            "www2.brasildownloads.net",
            "www.brasildownloads.net"
            ]
            if x.parsedUrl[1] in exceptions:                
                stringOrig = x.url.partition("/?url=")
                parsed = stringOrig[2]
                if not parsed.find(".") == -1:
                    x.decodedUrl = "http://" + parsed
                    x.decoded = True
                    x.decodeMethod = "custom add http://"
                else:
                    string = x.base64decodefix(parsed)
                    if not stringOrig == string:
                        x.decodedUrl = "http://" + string
                        x.decoded = True
                        x.decodeMethod = "custom add http://" 

        #url contem so o parametro que sera passado para o megaupload, o que eu preciso substituir
        if not x.decoded:
            exceptions = {
            "naodiga.com":"http://naodiga.com/b/b/?url=",
            "diretonocelular.com":"http://diretonocelular.com/b/b/?url="
            }
            if exceptions.has_key(x.parsedUrl[1]):
                x.url = x.url.replace(exceptions[x.parsedUrl[1]], "http://www.megaupload.com/")
                x.decoded = True
                x.decodedUrl = x.url
                x.decodeMethod = "custom url replace"
        
        #url contem so o parametro que sera passado para o megaupload
        if not x.decoded:
            if x.url.find("http://protegelinks.info") >= 0:
                x.deprotectStringAfterSeparator("/?","first")
                if x.decodedUrl.find("http://puxae.com") >= 0:
                    string = x.decodedUrl.partition("?url=")
                    string = string[2]
                    if string.startswith("http:/"):
                        x.decoded = True
                        x.decodedUrl = string
                        x.decodeMethod = 'custom reverse duplo protetor'
        
        #url possui um codigo, que deve ser passado para outra URL, e essa deve ser parseada via regex
        if not x.decoded:
            exceptions = [
            "download.vipdownload.com.br",
            "downloadfilmes.biz"
            ]
            if x.parsedUrl[1] in exceptions:
                try:
                    content = x.getUrlContents()
                    match = re.search('((?<=\()\d*?(?=(\,)))',content)
                    id = match.group(0)
                    x.url = "http://" + x.parsedUrl[1] + "/linkdiscover.php?cod=" + id                
                    content = x.getUrlContents()                
                except Exception:
                    pass
                if content.strip().startswith("http:/"):                
                    x.decoded = True
                    x.decodedUrl = content
                    x.decodeMethod = 'custom get url + regex'
        
        #linkbucks - dominio eh dinamico, nao pode usar o generico pq a chave eh o dominio
        if not x.decoded:        
            if x.parsedUrl[1].find("linkbucks") > 0:
                x.getUrlAndRunRegex("((?<=TargetUrl = \')http.*?(?=(\';)))")
                x.decodeMethod = 'custom domain + regex'

        '''
        if not x.decoded:
            if x.parsed_url[1] == "lix.in":
                sid = x.parsed_url[2][1:]
                
                data = 'tiny='+sid
                headers = { 'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.2.9) Gecko/20100824 Firefox/3.6.9 ( .NET CLR 3.5.30729; .NET CLR 4.0.20506)', 'Referer' : 'http://' + x.parsed_url[1]}
                print x.url
                print data
                req = urllib2.Request(x.url, data, headers)
                response = urllib2.urlopen(req)
                response = response.read()
                print response                
        '''             

        
        #decode scramble string
        if not x.decoded:
                if x.parsedUrl[1] == "www.link-protegido.com": 
                    #string = "/:thtp/wwflsrecmfl/JEqJr76ei/o.veei.w"                    
                    try:
                        parsedQueryString = cgi.parse_qs(x.parsedUrl[4]) 
                        string = parsedQueryString['p2'][0]                        

                        init = string.find("thtp")+1
                        num = 0
                        result = ''
                        
                        while len(result) < len(string):
                            if num == 0:
                                result = string[init]
                                num = num+1
                            else:
                                result = result + string[init+num]
                                result = result + string[init+(num*-1)]
                                num = num+1
                        if result.startswith("http:/"):
                            x.decoded = True
                            x.decodedUrl = result
                            x.decodeMethod = 'unscramble'
                    except Exception:
                        pass
                    
                    #string = "em.28www//:ptthiva.zib.mumixameht.www.LL3H.pU.piRDVD.ahnitsifruS.anurB.eD.atloV.A.yxxeS/9e59d2b661136a4e819703e23a143f46/selif/moc.oedivag"    
                    if not x.decoded:
                        try:
                            parsedQueryString = cgi.parse_qs(x.parsedUrl[4]) 
                            string = parsedQueryString['link'][0]     

                            init = string.find(":ptth")
                            init = init+5
                            final = string[init:] + string[0:init]
                            result = final[::-1]
                            
                            if result.startswith("http:/"):
                                x.decoded = True
                                x.decodedUrl = result
                                x.decodeMethod = 'unscramble (on half)'
                        except Exception:
                            pass                    
                        
             
        #link-protegido.com
        if not x.decoded:
            if x.parsedUrl[1] == "www.link-protegido.com":            
                x.parsedQueryString = cgi.parse_qs(x.parsedUrl[4])
                x.url = x.parsedUrl[0] + "://" + x.parsedUrl[1] + x.parsedUrl[2] + 'pag.php?link=' + x.parsedQueryString['link'][0]                
                content = x.getUrlContents()                
                
                soup = BeautifulSoup(content)            
                login = soup.find('input', id="login")['value']
                senha = soup.find('input', id="senha")['value']
                encoded = soup.find('input', id="pdifr")['value']                
                          
                login = int(login)-100300000 
                login = str(login)
                
                m = hashlib.md5()
                m.update(login)
                senha = m.hexdigest()
                
                x.url = x.parsedUrl[0] + "://" + x.parsedUrl[1] + x.parsedUrl[2] + 'trocas.php?link=' + encoded + '&login=' + login + '&senha=' + senha
    
                content = x.getUrlContents()
                if content.strip().startswith("http:/"):                
                    x.decoded = True
                    x.decodedUrl = content
                    x.decodeMethod = 'custom get url x2 with time lapse + regex'
            
        #na query string com parametros, normalmente
        if not x.decoded:            
            x.deprotectSimpleQueryString()        
        
        #se nada ainda deu certo, so reverter, caso nao tenha http escrito normal
        if not x.decoded:
            if x.url.find('http') == -1:
                x.decodeReverse(x.url)

        #se nada ainda deu certo, so base64, caso nao tenha http escrito normal
        if not x.decoded:
            if x.url.find('http') == -1:
                x.decodeBase64(x.url)

        #se nada ainda deu certo, so base64, caso nao tenha http escrito normal
        if not x.decoded:
            if x.url.find('http') == -1:
                x.decodeHex(x.url)


#decidir o que fazer quando passou por todo o algoritmo
        if x.decoded:
            success = True            
            if not x.decodedUrl.startswith("http://"):
                x.decodedUrl = x.decodedUrl.replace("http:/", "http://")

            if x.decodedUrl.endswith("=lru"):
                x.decodedUrl = x.decodedUrl.replace("=lru", "")

            if x.decodedUrl.endswith("=knil"):
                x.decodedUrl = x.decodedUrl.replace("=knil", "")

            if x.decodedUrl.endswith("!og"):
                x.decodedUrl = x.decodedUrl.replace("!og", "")

            x.decodedUrl = x.decodedUrl.strip()
                            
            
            print "<BR><img style='border:0px' src='http://desprotetor.com/static/correto.png'> &nbsp; <a href='" + x.decodedUrl + "' target='_blank'>" + x.decodedUrl + "</a>"                
            x.insertDbSuccess()
            logger.info("Desprotecao bem sucedida para: "+os.environ["REMOTE_ADDR"]+" - "+x.decodedUrl)

        else: #not decoded
            
            response = x.getDbAnswer()
            if response:
                success = True                
                if len(x.url) > 90:
                    print "<BR><img style='border:0px' src='http://desprotetor.com/static/alert.png'> (" + x.url[:90] + "...) <BR><BR>"
                else:
                    print "<BR><img style='border:0px' src='http://desprotetor.com/static/alert.png'>" + x.url + "<BR><BR>"                
                print response[1] + "<BR>"
                logger.info("Desprotecao nao executada. Blacklist para: "+response[0]+ " - "+x.url)
                if response[2] == 1:
                    x.insertDbFailure()
            else:
                if not x.valid:
                    success = True
                    if len(x.url) > 90:
                        print "<BR><img style='border:0px' src='http://desprotetor.com/static/alert.png'> (" + x.url[:90] + "...) <BR><BR>"
                    else:
                        print "<BR><img style='border:0px' src='http://desprotetor.com/static/alert.png'>" + x.url + "<BR><BR>"                       
                    logger.info("Desprotecao de url nao protegida: "+x.url)
                    print "<BR><BR>Isto nao se parece com um protetor de links. Confira a URL alimentada no Desprotetor.com.<BR>"
                else:
                    if len(x.url) > 90:
                        print "<BR><img style='border:0px' src='http://desprotetor.com/static/erro.png'> (" + x.url[:90] + "...) <BR><BR>"
                    else:
                        print "<BR><img style='border:0px' src='http://desprotetor.com/static/erro.png'>" + x.url + "<BR><BR>"                       
                    logger.info("Desprotecao falhou: "+x.url)    
                    x.insertDbFailure()        
            
if success:    
    print '<BR><BR>Volte sempre ao desprotetor.com e bom download. =)'
else:
    print "<BR><BR>Infelizmente sua URL nao foi desprotegida com sucesso. A equipe do Desprotetor.com verificara a questao. A ferramenta esta sendo sempre atualizada para melhorar sua experiencia de download. Volte sempre."