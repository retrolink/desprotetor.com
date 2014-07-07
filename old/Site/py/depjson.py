#!/usr/bin/python

# Import modules for CGI handling 
import cgi, cgitb, deprotectclass, re, hashlib, urlparse, base64, binascii, sys, urllib2, os
from BeautifulSoup import BeautifulSoup
from deprotectclass import UrlDeprotect
import logging
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


#cgitb.enable()
# Create instance of FieldStorage 
form = cgi.FormContent() 

# Get data from fields

ref = os.environ.get("HTTP_REFERER", "<not present>")
print "Content-type: text/html\n\n"

security = security.checksec()
if security.valid != True:
    pass
    logger.error("::: SECURITY ::: depjson.py - Motivo: "+security.error+". Ref: "+ref+" - IP: "+os.environ["REMOTE_ADDR"]+" - UA: "+os.environ.get("HTTP_USER_AGENT"))
    #print []
    #sys.exit(0)
else:    
    pass


try:
    text = form['data'][0]    
except Exception:
    print []
    sys.exit(0)




outputlist = []

    
#if cgi.escape(os.environ["REMOTE_ADDR"]) == "187.108.192.21":
#    print "to te vendo. =)"
#    sys.exit(0)




success = False
try:
    list = text.split("\n")
except Exception:
    sys.exit(0)

for s in list:   
    s = s.strip()
    #logger.info("Desprotegendo URL: "+s)
    if not s == '':

        if s.endswith(".url"):
            s = s.replace(".url", "")
        s = s.replace("<","").replace(">","").replace("\'","").replace("\"","")    

        x = deprotectclass.UrlDeprotect(s)

        if 'ext' in form: #se veio parametro indicando que request veio de extension
            x.extension = form['ext'][0]           

        x.invalidUrls = ["http://www.link-protegido.com","http://desprotetordelink.com","http://www.desprotetordelink.com","http://track.ozonion.com/","http://www.megaupload.com/?d=R1010212A883"]

            
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
            "www.baixarfilmesdublados.info":"kbskd",
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
            "telona.org":"/?",
            "topcine.net":"/?",
            "www.baixarfilme.info":"/?",
            "www.girodiario.com":"/?",            
            "www.musicasdegraca.com":"/?",
            "www.protetordelink.gospeldownloads.us":"/?",
            "www.puxandocompleto.com":"/?",
            "www.redirecionamentodeurl.com":"/?",
            "redirecionando.me":"/?",
            "www.romsup.com":"/?",
            "www.somcristao.com":"/?",
            "www.emurama.com":"protetor/?",
            "www.gospelgratis.org":"protetor/",
            "www.quick-downloads.com":"protetorrr/?",
            "topcine.net":"ABC123CBA",
            "protetor.downloadcdsgratis.com":"?url=",
            "somniu.net":"?url$",
            "castordownloads.net":"protetor/#/",
            "www.linkagratis.info":"6hnyh35yd3",
            "www.baixarjogoscompletos.info":"262565156",
            "zorrofilmes.com":"aHR0cDovL/",
            "protetor.zorrofilmes.com":"aHR0cDovL/",
            "www.baixardownload.org":"ac54a56a4",
            "redezorro.com":"protcaHR0cDovL/",
            "protetordelinks.com.br":"/?",
            "dicasdedicas.com":"/?",
            "buskaqui.in":"0cDovL/",
            "br4.us":"/2/",
            "www.jardimgospel.org":"/?",
            "www.tecnotech.net":"link=",
            "novoprotetor.zorrofilmes.com":"protcaHR0cDovL/",
            "www.baixarjafilmes.com":"php?link=",
            "www.filmescompletos.info":"/?"
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
            "protetordelink.tv":"/",
            "www.vamola.in":"&"
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
            "www.pqueno.com":"((?<=a\ href\=\")http.*?(?=(\" onmouse)))",
            "osfilmes.com":"((?<=location.href\=\')http.*?(?=(\')))",
            "www.promocoesdeprodutos.com":"((?<=(\<a href\=\"))http.*?(?=(\" onclick)))",
            "filmesmegavideo.net":"((?<=(\<a href\=\"))http\:\/\/assistir.*?(?=(\" rel)))",
            "www.linkproteger.com":"((?<=(a href\=\"))http.*?(?=(\" onclick\=)))",
            "linkbee.com":"((?<=(linkurl\' href\=\"))http.*?(?=(\")))",
            "linkbucks.com":"((?<=TargetUrl = \')http.*?(?=(\';)))",
            "www.lockurl.org":"((?<=(\(\'linkk0\'\)\.href\=\"))http.*?(?=(\";)))",
            "www.linkproteger.com":"((?<=(divDLStart\"><a href=\"))http.*?(?=(\" onclick)))",
            "topfilmes.com.br":"((?<=(innerHTML\=\'\<a\ href\=\"))http.*?(?=(\")))",
            "www.protetorlink.com":"((?<=(\<a\ href\=\"))http.*?(?=(\"\ onMouseOut\=\"MM_)))",
            "link-protector.com":"((?<=(name\=\"Continue\"\ onClick\=\"window\.location\=\'))http.*?(?=(\'\")))",
            "linkproteger.com":"((?<=(divDLStart\"\>\<a\ href\=\"))http.*?(?=(\"\ onclick\=\")))",
            "linkprotegido.info":"((?<=(url\=\"))http.*?(?=(\"\>)))",
            "assistirfilmesonline.biz":"((?<=(\%\]\" href=\"))http.*?(?=(\"\ title=\")))",
            "adv.li":"((?<=("+re.escape("""_url='""")+"))http.*?(?=("+re.escape("""',""")+")))",
            "www.centrodedownload.com":"((?<=("+re.escape("""href=\"""")+"))http.*?(?=("+re.escape("""\">Download""")+")))",
            "www.linkproteger.com":"((?<=("+re.escape("""divDLStart\"><a href=\"""")+"))http.*?(?=("+re.escape("""\">""")+")))"

            }
            if exceptions.has_key(x.parsedUrl[1]):
                x.getUrlAndRunRegex(exceptions[x.parsedUrl[1]])

        #get url and run regex, mas o resultado eh uma url encodada Ex: base64
        if not x.decoded:
            #dominio:regex
            ''' start = re.escape(patternstart)
                end = re.escape(patternfinish)        
                regexp = "((?<=("+start+")).*?(?=("+end+")))"  
            '''
            exceptions = {
            "www.agaleradodownload.com":"((?<=(var\ audhaiud\ \=\ \"))aHR0.*?(?=(\"\;)))",
            "www.filmesmegavideo.net":"((?<=("+re.escape('''<a href="http://assistir.filmesmegavideo.net/?v=''')+"))aHR0.*?(?=("+re.escape('''"''')+")))"
            }
            if exceptions.has_key(x.parsedUrl[1]):                
                x.content = x.getUrlContents()
                match = re.search(exceptions[x.parsedUrl[1]],x.content)                                
                string = match.group(0)
                x.decodeFull(string)

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
                if x.checkCorrect(string):                    
                    x.decodeMethod = "custom decode even/odd" 

        #base 64 que quando decodado fica Nome do Filme|Url
        if not x.decoded: #10/12/2012        
            exceptions = [                    
            "direcionando.baixedetudo.net",
            "www.baixarfilmesdublados.info",
            "linkprotegido.info"
            ]
            if x.parsedUrl[1] in exceptions:  
                try:              
                    parsedQueryString = cgi.parse_qs(x.parsedUrl[4]) 
                    string = parsedQueryString['url'][0]   
                                    
                    #logger.info(string)        
                    string = base64.decodestring(string)
                    #logger.info(string)        
                    string = string.split("|")
                    #logger.info(string)        
                    string = string[1]        
                    #logger.info(string)        
                    if string.startswith("http"):
                        x.decoded = True
                        x.decodedUrl = string
                        x.decodeMethod = "special (direcionando.baixetudo) split string b64"
                except Exception:
                    pass


        #furiagames.org -- apenas um dos parametros GET possui a URL, o resto eh decoy
        if not x.decoded:
            exceptions = {                    
            "furiagames.org":"laospqwsado4512asd1",
            "baixai.net":"laospqwsado4512asd1",
            "furiagames360.org":"laospqwsado4512asd1"            
            }
            if exceptions.has_key(x.parsedUrl[1]):                    
                    for s in x.parsedQueryString:                        
                        string = s[1]                            
                        try:
                            string = binascii.unhexlify(string)
                            string.replace("?","")
                            string = base64.decodestring(string)
                            string = binascii.unhexlify(string)
                        except Exception:
                            pass
                        if x.checkCorrect(string):                            
                            x.decodeMethod = "custom decode hex base64 hex"   

        #pegar casos de hex invertido com 0s intercalados
        if not x.decoded:                        
            for s in x.parsedQueryString:
                s = str(s[1])
                if s.find("70074074068") > -1:                       
                    list1 = []
                    for a in s:
                        list1.append(a)                    

                    position = 0
                    for a in list1:
                        if position % 3 == 0 or position == 0:
                            list1[position] = ""
                        position = position+1

                    newurl = "".join(list1)
                    try:
                        s = binascii.unhexlify(newurl)                    
                        s = s[::-1]                    
                    except Exception:
                        pass                    
                    if x.checkCorrect(s):                        
                        x.decodeMethod = "custom decode inverted s with 0s between"    



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
                            if x.checkCorrect(string):                                
                                x.decodeMethod = "custom decode hex base64 hex"   

        if not x.decoded: #18/07/2011
            exceptions = {                    
            "www.emurama.com":"id"
            }
            if exceptions.has_key(x.parsedUrl[1]):                    
                    for s in x.parsedQueryString:
                        if s[0] == exceptions[x.parsedUrl[1]]:
                            string = s[1]                            
                            try:
                                string = binascii.unhexlify(string)
                                string = base64.decodestring(string)
                                string = string[::-1]
                            except Exception:
                                pass
                            
                            if x.checkCorrect(string):                                
                                x.decodeMethod = "custom decode hex base64 reverse" 

        if not x.decoded:
            exceptions = {                    
            "protetor.download-jogo.com":"url"
            }
            if exceptions.has_key(x.parsedUrl[1]):                    
                    for s in x.parsedQueryString:
                        if s[0] == exceptions[x.parsedUrl[1]]:
                            string = s[1]                            
                            string = string[3:len(string)-3]                            
                            pos = 1
                            a = 0
                            result = ""
                            b = 0
                            try:
                                while a < len(string):
                                    result = result + string[pos+a]        
                                    a = a+2
                            except Exception, a:
                                if str(a) == "string index out of range":
                                    string = string[::-1]
                                    pos = 0
                                    while b < len(string):
                                        result = result + string[pos+b]            
                                        b = b+2
                            if x.checkCorrect(result):
                                x.decodeMethod = "custom decode even roundabout" 


        #simple cypher        
        if not x.decoded:
            exceptions = [
            "www.linkbuy.com.br"            
            ]
            if x.parsedUrl[1] in exceptions:                                 
                for s in x.parsedQueryString[0]:                                        
                    s = x.parsedQueryString[0][1]
                    try:
                        string = base64.decodestring(s) #modelo 2: vinxp (na verdade muda so o 'h')
                        dicio = {"025":"a",
                        "a56":"b",
                        "bA5":"c",
                        "Bc7":"d",
                        "AdD":"e",            
                        "ec3":"f",
                        "e2d":"g",
                        "a2d":"h",
                        "ge4":"i",
                        "i6A":"j",
                        "F7e":"k",
                        "kf4":"l",
                        "21F":"m",
                        "f25":"n",
                        "m91":"o",
                        "ij5":"p",
                        "j32":"q",
                        "q56":"r",
                        "f0j":"s",
                        "f0d":"t",
                        "qs0":"u",
                        "r02":"v",
                        "5fg":"w",
                        "ppN":"x",
                        "f0C":"y",
                        "56s":"z",
                        "x5F":":",
                        "x15":"/",
                        "sx0":".",
                        "pxw":"?",
                        "zc0":"="}
                        for a in dicio:
                            string = string.replace(a,dicio[a])
                        
                        if x.checkCorrect(string):                        
                            x.decodeMethod = "custom simple cypher - linkbuy"
                    except Exception, e:
                        logger.error("erro: "+str(e)+" -- "+str(x.url))

        #simple cypher        
        if not x.decoded:
            exceptions = [
            "www.linkbuy.com.br"            
            ]
            if x.parsedUrl[1] in exceptions:                                 
                for s in x.parsedQueryString[0]:                                        
                    s = x.parsedQueryString[0][1]
                    try:
                        string = base64.decodestring(s) #modelo 2: agaleradodownload
                        dicio = {"025":"a",
                        "a56":"b",
                        "bA5":"c",
                        "Bc7":"d",
                        "AdD":"e",            
                        "ec3":"f",
                        "e2d":"g",
                        "h":"h",
                        "ge4":"i",
                        "i6A":"j",
                        "F7e":"k",
                        "kf4":"l",
                        "21F":"m",
                        "f25":"n",
                        "m91":"o",
                        "ij5":"p",
                        "j32":"q",
                        "q56":"r",
                        "f0j":"s",
                        "f0d":"t",
                        "qs0":"u",
                        "r02":"v",
                        "5fg":"w",
                        "ppN":"x",
                        "f0C":"y",
                        "56s":"z",
                        "x5F":":",
                        "x15":"/",
                        "sx0":".",
                        "pxw":"?",
                        "zc0":"="}
                        for a in dicio:
                            string = string.replace(a,dicio[a])
                        
                        if x.checkCorrect(string):                            
                            x.decodeMethod = "custom simple cypher - linkbuy"
                    except Exception, e:
                        logger.error("erro: "+str(e)+" -- "+str(x.url))

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
                try:
                    for l in list:
                        result = result + chr(int(l))
                except Exception, e:
                    logger.error("erro: "+str(e)+" -- "+str(x.url))
                
                if x.checkCorrect(result):                    
                    x.decodeMethod = "custom decode electron_encode crypt"   

        #base64 com frescuras
        if not x.decoded:
            exceptions = [
            "fgprotege.com"            
            ]
            if x.parsedUrl[1] in exceptions:  
                string = x.url
                
                if string.find("aHR0") > 0:            
                    init = string.find("aHR0")
                    string = string[init:]
                

                if string.find("I2h0dH") > 0:            
                    init = string.find("I2h0dH")
                    string = string[init:]
                
                
                if string.find("_") > 0:
                    megaupload = string[string.find("_")+1:]                    
                    try:
                        parameter = base64.decodestring(megaupload)
                        result = "http://www.megaupload.com/?" + parameter
                    except Exception:
                        pass

                else:                    
                    try:
                        result = base64.decodestring(string)
                    except Exception:
                        pass
                
                if result.startswith("#http:/"):
                    result = result[1:]                
                
                if x.checkCorrect(result):                    
                    x.decodeMethod = "custom base64"   


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
                if x.checkCorrect(result):                    
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
                    if x.checkCorrect(string):                        
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
                except Exception, e:
                    logger.error("erro: "+str(e)+" -- "+str(x.url))
                try:
                    if x.checkCorrect(content.strip()):                                            
                        x.decodeMethod = 'custom get url + regex'
                except Exception, e:
                    logger.error("erro: "+str(e)+" -- "+str(x.url))
        
        #linkbucks - dominio eh dinamico, nao pode usar o generico pq a chave eh o dominio
        if not x.decoded:        
            if x.parsedUrl[1].find("linkbucks") > 0:
                x.getUrlAndRunRegex("((?<=TargetUrl = \')http.*?(?=(\';)))")
                x.decodeMethod = 'custom domain + regex'

   


        #desativando todos os link-protegido.com -- usando o desprotetordelink.com (que eh deles mesmo)

        if not x.decoded:
            if x.parsedUrl[1] == "www.link-protegido.com":
                    
                #string = "em.28www//:ptthiva.zib.mumixameht.www.LL3H.pU.piRDVD.ahnitsifruS.anurB.eD.atloV.A.yxxeS/9e59d2b661136a4e819703e23a143f46/selif/moc.oedivag"
                try:
                    parsedQueryString = cgi.parse_qs(x.parsedUrl[4]) 
                    string = parsedQueryString['link'][0]   
                    init = string.find("ptth")
                    init = init+4
                    final = string[init:] + string[0:init]
                    result = final[::-1]
                    
                    if x.checkCorrect(result):                        
                        x.decodeMethod = 'unscramble link-protegido on half'
                except Exception:
                    pass  

                #http://www.link-protegido.com/semprefilmesv2/?link=GF1EV25NG8
                if not x.decoded:
                    #pegando auth da home de desprotetordelink
                    
                    downurl = "http://www.desprotetordelink.com"
                    data = ''
                    headers = { 'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.2.9) Gecko/20100824 Firefox/3.6.9 ( .NET CLR 3.5.30729; .NET CLR 4.0.20506)', 'Referer' : ''}
                    req = urllib2.Request(downurl, data, headers)
                    response = urllib2.urlopen(req)
                    response = response.read()
                    
                    soup = BeautifulSoup(response)            
                    auth = soup.find('form')['action'] #index.php?auth=23cc2e1c8c366a2176d0e40f00e8b539                    
                    #soup.find("b", { "class" : "auth" })
                    #logger.info(soup)
                    #logger.info(auth)
                    

                    #http://www.desprotetordelink.com/index.php?url=http%3A//www.link-protegido.com/semprefilmesv2/%3Flink%3D345XG7AZMO
                    downurl = "http://www.desprotetordelink.com/"+auth+"&link="+x.url.replace("&","@321").replace(":","%3A")
                    data = ""
                    headers = { 'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.2.9) Gecko/20100824 Firefox/3.6.9 ( .NET CLR 3.5.30729; .NET CLR 4.0.20506)', 'Referer' : 'http://www.desprotetordelink.com'}
                    req = urllib2.Request(downurl, data, headers)
                    response = urllib2.urlopen(req)
                    response = response.read()
                    #logger.info(response)
                    
                    try:
                        soup = BeautifulSoup(response)                        
                        ret = soup.find('a')['href']
                    except Exception, e:                        
                        logger.error("erro: "+str(e)+" -- "+str(x.url)+" Soup: "+str(soup))
                    
                    if x.checkCorrect(ret.strip()):
                        x.decodeMethod = 'usando desprotetordelink.com(link-protegido.com)'


        if not x.decoded: #18/07/2011
            if x.parsedUrl[1] == "www.vinxp.com":
                x.url = x.url.replace("?id=","vinxp.php?id=")
                content = x.getUrlContents()
                url = content.replace("<script>location.href='","").replace("';</script>","")                
                if x.checkCorrect(url) and url.find("vinxp") == -1:                    
                    x.decodeMethod = "special (vinxp) get url and parse content"
                


                                
        #na query string com parametros, normalmente
        if not x.decoded:            
            x.deprotectSimpleQueryString()        
        
        #se ainda nao deu certo, tentar achar um base64 (aHR0) 
        if not x.decoded:
            if x.url.find('aHR0') > -1:
                x.decodeBase64(x.url[x.url.find('aHR0'):])
                
        #se ainda nao deu certo, tentar achar um hex (687474)
        if not x.decoded:
            if x.url.find('687474') > -1:
                x.decodeHex(x.url[x.url.find('687474'):])        

        #se nada ainda deu certo, so reverter, caso nao tenha http escrito normal
        if not x.decoded:
            if x.url.find('http') == -1:
                x.decodeReverse(x.url)

        #se nada ainda deu certo, so base64, caso nao tenha http escrito normal
        if not x.decoded:
            if x.url.find('http') == -1:
                x.decodeBase64(x.url)

        #se nada ainda deu certo, so hexa, caso nao tenha http escrito normal
        if not x.decoded:
            if x.url.find('http') == -1:
                x.decodeHex(x.url)

        

#decidir o que fazer quando passou por todo o algoritmo
        if x.decoded:
            success = True

            if x.decodedUrl.endswith("=lru"):
                x.decodedUrl = x.decodedUrl.replace("=lru", "")

            if x.decodedUrl.endswith("=lru?"):
                x.decodedUrl = x.decodedUrl.replace("=lru?", "")

            if x.decodedUrl.endswith("=knil"):
                x.decodedUrl = x.decodedUrl.replace("=knil", "")

            if x.decodedUrl.endswith("!og"):
                x.decodedUrl = x.decodedUrl.replace("!og", "")
            x.decodedUrl = x.decodedUrl.strip()

            #output = output + "arr[0] = 1; arr[1] = '"+x.decoded_url+"';"
            
            outputlist.append({"dep":1,"url":x.decodedUrl})

            #print "<BR><img style='border:0px' src='http://desprotetor.com/static/correto.png'> &nbsp; <a href='" + x.decoded_url + "' target='_blank'>" + x.decoded_url + "</a>"
            try:
                x.insertDbSuccess()
            except Exception, e:
                logger.error("Erro ao inserir sucesso: "+str(e)+" Url desprotegida: "+x.decodedUrl+" url original: "+x.originalurl)
            logger.info("Desprotecao bem sucedida ("+x.extension+") para: "+os.environ["REMOTE_ADDR"]+" - "+x.decodedUrl)
            
            #output = output + "response.push(arr);"

        else: #not decoded
            try:
                response = x.getDbAnswer()
            except Exception, e:
                response = False
                logger.exception("Erro ao pegar respostas padrao: "+str(e))

            if response:
                success = True

                outputlist.append({"dep":2,"url":x.url,"mess":str(response[1])})
                logger.info("Desprotecao nao executada. ("+x.extension+") Blacklist para: "+response[0]+ " - "+x.url)
                if response[2] == 1:
                    try:
                        x.insertDbFailure()                                    
                    except Exception, e:
                        logger.error("Erro ao inserir falha: "+str(e)+" Url: "+x.url)
            else:
                if not x.valid:
                    success = True

                    outputlist.append({"dep":3,"url":x.url,"mess":"nao parece um protetor"})
                else:
                    outputlist.append({"dep":0,"url":x.url})
                    logger.info("Desprotecao falhou ("+x.extension+"): "+x.url)    
                    try:
                        x.insertDbFailure()        
                    except Exception, e:
                        logger.error("Erro ao inserir falha: "+str(e)+" Url: "+x.url)

out = str(outputlist)
print out