#!/usr/bin/python

from flask import Flask
from flask import request

app = Flask(__name__)

from urlparse import parse_qs
from urlparse import parse_qsl
from re import search
from re import escape
from urlparse import urlparse
from base64 import decodestring
from binascii import unhexlify
from urllib2 import Request
from urllib2 import urlopen
from logging import Formatter
from logging import handlers
from logging import getLogger
from logging import DEBUG

from json import dumps

from socket import setdefaulttimeout

from libs.BeautifulSoup import BeautifulSoup
from libs.deprotectclass import UrlDeprotect
from settings import settings


setdefaulttimeout(10)  # setando timeout para gets de url


# logger principal da aplicacao
logger = getLogger('app_logger')
logger.setLevel(DEBUG)

#handler = handlers.RotatingFileHandler(
#    settings.application_log,
#    maxBytes=1024 * 1024 * 100,
#    backupCount=5
#)

handler = handlers.TimedRotatingFileHandler(settings.application_log, 'midnight', 1, backupCount=7)
formatter = Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


# logger de user agent
ua_logger = getLogger('ua_logger')
ua_logger.setLevel(DEBUG)
ua_handler = handlers.TimedRotatingFileHandler(settings.user_agent_log, 'midnight', 1, backupCount=7)
ua_formatter = Formatter('%(message)s')
ua_handler.setFormatter(ua_formatter)
ua_logger.addHandler(ua_handler)


logger.info("Iniciando aplicacao WSGI Desprotetor...")


@app.route('/', methods=['GET', 'POST'])
def dep():
    if request.method == 'GET':
        logger.warn("Tentativa de GET na URL do desprotetor. Ip: %s. UA: %s" %
                    (request.remote_addr, request.user_agent.string))
        ua_logger.info("%s :: %s" % (request.remote_addr, request.user_agent.string))
        return '[]'
    if request.method == 'POST':
        if "Firefox/4.0.1" in request.headers.get('User-Agent'):
            logger.warn("Get com User Agent filtrado: %s - %s" % (request.referrer, request.remote_addr))
            return '[]'

        if not (request.referrer.startswith("http://desprotetor.com/") or
                request.referrer.startswith("http://www.desprotetor.com/")):
            logger.warn("Referer invalido: %s - %s" % (request.referrer, request.remote_addr))
            # return '[]'
        try:
            ua_logger.info("%s :: %s" % (request.remote_addr, request.user_agent.string))
            return deprotect(request)
        except Exception, e:
            logger.error("Erro ao desproteger URL: " + request.form["data"])
            logger.exception(e)
            return '[]'


@app.route('/verify', methods=['GET', 'POST'])
def verify():
    return ' '


def deprotect(request_info):
    if "data" in request_info.form:
        text = request_info.form["data"]
    else:
        return "[]"

    outputlist = []

    try:
        lst = text.split("\n")
    except IndexError:
        return "[]"

    for element in lst:
        element = element.strip()
        if not element == '':

            if element.endswith(".url"):
                element = element.replace(".url", "")
            element = element.replace("<", "").replace(">", "").replace("\'", "").replace("\"", "")

            x = UrlDeprotect(element)

            if 'ext' in request_info.form:   # se veio parametro indicando que request veio de extension
                x.extension = request_info.form['ext']

            x.invalid_rls = ["http://www.semprefilmes.com/",
                             "http://www.link-protegido.com",
                             "http://desprotetordelink.com",
                             "http://www.desprotetordelink.com",
                             "http://track.ozonion.com/",
                             "http://www.megaupload.com/?d=R1010212A883"]

            #string apos separador definido
            if not x.decoded:
                exceptions = {
                    "filmeslegendados.info": "/?",
                    "yess.me": "/ir/id/",
                    "www.megafilmesbr.com": "go.php?",
                    "www.downloads-completos.info": "go.php?",
                    "www.celularbr.com": "/?",
                    "www.brasildowns.com.br": "/?Z28h",
                    "www.evolutionsurf.net": "/?",
                    "www.baixebr.org": "/?",
                    "protegerlinks.com": "/?",
                    "clickgratis.org": "ir/id/",
                    "linkprotegido.awardspace.biz": "?url*",
                    "ftp.marciobgf.com": "/?",
                    "www.tudofull.com": "/?",
                    "baixakifilmes.info": "/?",
                    "www.apgfamily.com": "/?",
                    "www.protetordelinksja.net": "?down!",
                    "linkprotegido.biz": "?link",
                    "www.downloadsemcontrole.org": "/?",
                    "www.monitordownloads.net": "cm.php?",
                    "www.baixarfilmesdublados.info": "kbskd",
                    "playcelular.net": "/?",
                    "dualfilmes.com": "/link=",
                    "brfreestylepes.forumeiros.com": "go/",
                    "protelink.info": "id/",
                    "www.planetadownloads.com": "/?",
                    "www.wejte.com": "/?",
                    "www.downsupremo.com": "?url=#",
                    "filmeseseriadosgratis.com": "/?",
                    "protegerlinks.net": "?go%21",
                    "www.baixeaquifilmes.com": "/?",
                    "www.downloadfilmespornos.com": "/?",
                    "www.downloadsgratis.us": "?down!",
                    "www.elitedosfilmes.com": "/?",
                    "www.freefilmeseseries.com": "/?",
                    "www.protetordownloads.info": "/?",
                    "www.liberadosfree.info": "/?",
                    "www.cdscompletos.org": "protetor/",
                    "www.topwebgratis.com": "?down!",
                    "www.loucosporsoftwares.com": "?go%21",
                    "jackao.net": "putaria/",
                    "www.downloadsdegraca.com": "continuar/",
                    "telona.biz": "/?",
                    "telona.org": "/?",
                    "www.baixarfilme.info": "/?",
                    "www.girodiario.com": "/?",
                    "www.musicasdegraca.com": "/?",
                    "www.protetordelink.gospeldownloads.us": "/?",
                    "www.puxandocompleto.com": "/?",
                    "www.redirecionamentodeurl.com": "/?",
                    "redirecionando.me": "/?",
                    "www.romsup.com": "/?",
                    "www.somcristao.com": "/?",
                    "www.emurama.com": "protetor/?",
                    "www.gospelgratis.org": "protetor/",
                    "www.quick-downloads.com": "protetorrr/?",
                    "topcine.net": "ABC123CBA",
                    "protetor.downloadcdsgratis.com": "?url=",
                    "somniu.net": "?url$",
                    "castordownloads.net": "protetor/#/",
                    "www.linkagratis.info": "6hnyh35yd3",
                    "www.baixarjogoscompletos.info": "262565156",
                    "zorrofilmes.com": "aHR0cDovL/",
                    "protetor.zorrofilmes.com": "aHR0cDovL/",
                    "www.baixardownload.org": "ac54a56a4",
                    "redezorro.com": "protcaHR0cDovL/",
                    "protetordelinks.com.br": "/?",
                    "dicasdedicas.com": "/?",
                    "buskaqui.in": "0cDovL/",
                    "br4.us": "/2/",
                    "www.jardimgospel.org": "/?",
                    "www.tecnotech.net": "link=",
                    "novoprotetor.zorrofilmes.com": "protcaHR0cDovL/",
                    "www.baixarjafilmes.com": "php?link=",
                    "www.filmescompletos.info": "/?",
                    "www.alturaepeso.com": "/?",
                    "protetordelink.tv": "1/",
                    "www.buskaqui.in": "protcaHR0cDovL/",
                    "gta.nafaixa.com.br": "cDovL/",
                    "dicasedicas.info": "/?",
                    "www.gospeldownloads.us": "/?",
                    "megagostoso.org": "/?",
                    "dicastech.net": "/?",
                    "amofilmes.net": "/?",
                    "protetor-link-br.blogspot.com.br": "?url=",
                    "vivendosaude.net": "/?",
                    "minhasreceitasfaceis.com": "/?",
                }
                if x.parsed_url[1] in exceptions:
                        x.deprotect_string_after_separator(exceptions[x.parsed_url[1]], "first")

            #string apos separador definido -- caso alguem da lista de cima tenha mais de um metodo
            if not x.decoded:
                exceptions = {
                    "www.brasildowns.com.br": "/?",
                    "www.emurama.com": "protetor2/?"
                }
                if x.parsed_url[1] in exceptions:
                        x.deprotect_string_after_separator(exceptions[x.parsed_url[1]], "first")

            #string apos ultimo separador definido
            if not x.decoded:
                exceptions = {
                    "protetordelink.tv": "/",
                    "www.vamola.in": "&"
                }
                if x.parsed_url[1] in exceptions:
                    x.deprotect_string_after_separator(exceptions[x.parsed_url[1]], "last")

            #string apos separador go! que eh bastante comum
            if not x.decoded:
                if x.url.find("go!") > -1:
                    x.deprotect_string_after_separator("go!", "first")

            #string apos separador | que eh bastante comum
            if not x.decoded:
                if x.url.find("|") > -1:
                    x.deprotect_string_after_separator("|", "first")

            #string apos separador protcaHR0cDovL/ que eh bastante comum
            if not x.decoded:
                if x.url.find("/protcaHR0cDovL/") > -1:
                    x.deprotect_string_after_separator("/protcaHR0cDovL/", "first")

            #string apos separador /download/? que eh bastante comum
            if not x.decoded:
                if x.url.find("/download/?") > -1:
                    x.deprotect_string_after_separator("/download/?", "first")

            #string apos separador ?down! que eh bastante comum
            if not x.decoded:
                if x.url.find("?down!") > -1:
                    x.deprotect_string_after_separator("?down!", "first")

            #remover valor da string, e entao tratar normalmente depois de separador
            if not x.decoded:
                exceptions = {
                    "link.baixedetudo.net": [".url", ".net/"],
                    "superdownsmega.paginadedownload.info": [".url", ".info/"],
                    "protetor.clubedodownload.info": [".url", ".info/"]
                }
                if x.parsed_url[1] in exceptions:
                    x.url = x.url.replace("#", "")
                    x.url = x.url.replace(exceptions[x.parsed_url[1]][0], "")
                    x.deprotect_string_after_separator(exceptions[x.parsed_url[1]][1], "first")

            #string depois de uma certa distancia
#http://protetordelinks.cont.us/p/9ba0f0f0215e92058fbb2be528c364a9/aHR0cDovL3d3dy5tZWdhdXBsb2FkLmNvbS8/ZD1JUkc0TzA4Ug==
            if not x.decoded:
                exceptions = {
                    "protetordelinks.cont.us": 66
                }
                if x.parsed_url[1] in exceptions:
                    x.deprotect_string_after_distance(exceptions[x.parsed_url[1]])

            #string depois de um numero de ocorrencias de uma outra string
#http://protetordelinks.cont.us/p/9ba0f0f0215e92058fbb2be528c364a9/aHR0cDovL3d3dy5tZWdhdXBsb2FkLmNvbS8/ZD1JUkc0TzA4Ug==
            #depois do 3o. / no path
            if not x.decoded:
                exceptions = {
                    "protetordelinks.cont.us": [3, "/"]
                }
                if x.parsed_url[1] in exceptions:
                    num = exceptions[x.parsed_url[1]][0]
                    sep = exceptions[x.parsed_url[1]][1]
                    a = 1
                    pos = 0
                    while a <= num:
                        pos = x.parsed_url[2].find(sep, pos)
                        pos += 1
                        a += 1
                    x.decode_full(x.parsed_url[2][pos:])

            #apenas um dos parametros GET possui a URL, o resto eh decoy
            if not x.decoded:
                exceptions = {
                    "36.baixevipdown.net": "url"
                }
                if x.parsed_url[1] in exceptions:
                        for q in x.parsed_query_string:
                            if q[0] == exceptions[x.parsed_url[1]]:
                                x.decode_full(q[1])

            #get url and run regex, mas o resultado eh uma url encodada Ex: base64
            if not x.decoded:
                #dominio:regex
                #start = escape(patternstart)
                #end = escape(patternfinish)
                #regexp = "((?<=("+start+")).*?(?=("+end+")))"
                exceptions = {
                    "assistirfilmesonline.biz": "((?<=(" +
                                                escape(""".filmesmegavideo.net/?v=""") +
                                                "))aHR0.*?(?=(" +
                                                escape("""\"""") + ")))",
                    "www.agaleradodownload.com": "((?<=(var\ audhaiud\ \=\ \"))aHR0.*?(?=(\"\;)))",
                    "www.filmesmegavideo.net": "((?<=(" +
                                               escape('''<a href="http://assistir.filmesmegavideo.net/?v=''') +
                                               "))aHR0.*?(?=(" +
                                               escape('''"''') + ")))"
                }
                if x.parsed_url[1] in exceptions:
                    try:
                        x.content = x.get_url_contents()
                        match = search(exceptions[x.parsed_url[1]], x.content)
                        if match is not None:
                            string = match.group(0)
                            x.decode_full(string)
                    except Exception as e:
                        logger.exception(e)

            #informacao nao esta na url - pegar conteudo da pagina e parsear via regex
            if not x.decoded:
                #dominio:regex
                exceptions = {
                    "www.pqueno.com": "((?<=a\ href\=\")http.*?(?=(\" onmouse)))",
                    "osfilmes.com": "((?<=location.href\=\')http.*?(?=(\')))",
                    "www.promocoesdeprodutos.com": "((?<=(\<a href\=\"))http.*?(?=(\" onclick)))",
                    "filmesmegavideo.net": "((?<=(\<a href\=\"))http\:\/\/assistir.*?(?=(\" rel)))",
                    "linkbee.com": "((?<=(linkurl\' href\=\"))http.*?(?=(\")))",
                    "linkbucks.com": "((?<=TargetUrl = \')http.*?(?=(\';)))",
                    "www.lockurl.org": "((?<=(" +
                                       escape("""('newlink').href=\"""") +
                                       "))http.*?(?=(" +
                                       escape("""\";""") + ")))",
                    "topfilmes.com.br": "((?<=(innerHTML\=\'\<a\ href\=\"))http.*?(?=(\")))",
                    "link-protector.com": "((?<=(name\=\"Continue\"\ "
                                          "onClick\=\"window\.location\=\'))http.*?(?=(\'\")))",
                    "linkprotegido.info": "((?<=(url\=\"))http.*?(?=(\"\>)))",
                    "adv.li": "((?<=(" + escape("""_url='""") + "))http.*?(?=(" + escape("""',""") + ")))",
                    "www.centrodedownload.com": "((?<=(" + escape("""href=\"""") + "))http.*?(?=(" +
                                                escape("""\">Download""") + ")))",
                    "www.linkproteger.com": "((?<=(" + escape("""divDLStart\"><a href=\"""") + "))http.*?(?=(" +
                                            escape("""\">""") + ")))"
                }
                if x.parsed_url[1] in exceptions:
                    x.get_url_and_run_regex(exceptions[x.parsed_url[1]])
            
            #informacao nao esta na url - alterar url e pegar conteudo da pagina para parsear via regex
            if not x.decoded:
                #'dominio':['pattern search','pattern replace','regex buscar']
                exceptions = {
                    "www.assistirfilmesonline.net": [".net/pub-", ".net/", "((?<=(value\=\"))http.*?(?=(\")))"],
                    "assistirfilmesonline.net": [".net/pub-", ".net/", "((?<=(value\=\"))http.*?(?=(\")))"]
                }
                if x.parsed_url[1] in exceptions:
                    x.get_changed_url_and_run_regex(exceptions[x.parsed_url[1]][0],
                                                    exceptions[x.parsed_url[1]][1],
                                                    exceptions[x.parsed_url[1]][2])

            #na query string sem parametros
            #desativado para URLs invertidas
            # http://www.celularbr.com/seven/?NP129KKT=d?/moc.daolpuagem.www//:ptth
            if not x.decoded:
                x.deprotect_querystring_without_param_name()

            #-----------------------------
            #metodos completamente customizados para casos estranhos
            #-----------------------------

            #inverter e remover string da URL
            if not x.decoded:
                exceptions = {
                    "www.linkstw.com": "Z@E$",
                    "filmeseserieshd.com": "Z@E$"
                }
                if x.parsed_url[1] in exceptions:
                    x.url = x.url.replace(exceptions[x.parsed_url[1]], "")
                    x.parsed_url = urlparse(x.url.strip())
                    x.parsed_query_string = parse_qsl(x.parsed_url[4])
                    x.deprotect_simple_query_string()
                    x.decode_method = "custom simple param"

            #url com pares e impares
            if not x.decoded:
                exceptions = {
                    "protetor.downloadcdsgratis.com": "?url="
                }
                if x.parsed_url[1] in exceptions:
                    string = x.url
                    string = string.replace("&t=2", "")
                    string = string.partition(exceptions[x.parsed_url[1]])
                    string = string[2]

                    l = len(string)
                    a = 1
                    b = ""
                    while a < l:
                        b = b + string[a]
                        a += 2
                    if l % 2 == 1:
                        l -= 1
                        b = b + string[l]

                    while l > 0:
                        l -= 2
                        b = b + string[l]
                    string = b
                    if x.check_correct(string):
                        x.decode_method = "custom decode even/odd"

            #base 64 que quando decodado fica Nome do Filme|Url
            if not x.decoded:  # 10/12/2012
                try:
                    parsed_query_string = parse_qs(x.parsed_url[4])
                    for key in parsed_query_string:
                        string = parsed_query_string[key][0]

                        #logger.info(string)
                        string = x.base64decodefix(string)

                        string = string.replace("\t", "")
                        string = string.replace(" ", "")

                        #string = decodestring(string)
                        #logger.info(string)
                        string = string.split("|http")
                        #logger.info(string)
                        string = string[1]
                        string = "http" + string
                        #logger.info(string)
                        if string.startswith("http"):
                            x.decoded = True
                            x.decoded_url = string
                            x.decode_method = "special (direcionando.baixetudo) split string b64"
                except IndexError:
                    pass
                except Exception as e:
                    logger.exception(e)
                    pass

            #furiagames.org -- apenas um dos parametros GET possui a URL, o resto eh decoy
            if not x.decoded:
                exceptions = {
                    "furiagames.org": "laospqwsado4512asd1",
                    "baixai.net": "laospqwsado4512asd1",
                    "furiagames360.org": "laospqwsado4512asd1"
                }
                if x.parsed_url[1] in exceptions:
                        for q in x.parsed_query_string:
                            string = q[1]
                            try:
                                string = unhexlify(string)
                                string.replace("?", "")
                                string = decodestring(string)
                                string = unhexlify(string)
                            except TypeError:
                                pass
                            except Exception as e:
                                logger.exception(e)
                            if x.check_correct(string):
                                x.decode_method = "custom decode hex base64 hex"

            # adf.ly - get content, run regex, decode custom
            # 27/03/2013
            if not x.decoded:
                exceptions = [
                    "adf.ly",
                ]
                if x.parsed_url[1] in exceptions:
                    try:
                        contents = x.get_url_contents()
                        match = search("((?<=(" + escape("""ysmm = \'""") + ")).*?(?=(" + escape("""\';""") + ")))",
                                       contents)
                        encrypted_url = match.group(0)

                        first_half = encrypted_url[::2]
                        second_half = encrypted_url[::-1][::2]
                        new = first_half + second_half
                        new = x.base64decodefix(new)
                        new = new[2:]

                        if new.startswith("http"):
                            x.decoded = True
                            x.decoded_url = new
                            x.decode_method = "special (adf.ly) split string b64"

                    except Exception, e:
                        logger.error("erro: " + str(e) + " -- " + str(x.url))

            #pegar casos de hex invertido com 0s intercalados
            if not x.decoded:
                for el in x.parsed_query_string:
                    element = el
                    try:
                        element = str(element[1])
                    except UnicodeEncodeError:
                        element = element[1].encode("ascii", "ignore")
                    if element.find("70074074068") > -1:
                        list1 = []
                        for a in element:
                            list1.append(a)

                        position = 0
                        while position < len(list1):
                            if position % 3 == 0 or position == 0:
                                list1[position] = ""
                            position += 1

                        newurl = "".join(list1)
                        try:
                            element = unhexlify(newurl)
                            element = element[::-1]
                        except Exception as e:
                            logger.exception(e)
                            pass
                        if x.check_correct(element):
                            x.decode_method = "custom decode inverted s with 0s between"

            # www.vinxp.com -- babacas que fazem transformacoes em sequencia e substituicoes bobas, hackeavel
            # agora usam linkbuy
            if not x.decoded:
                exceptions = {
                    "www.vinxp.com": "id"
                }
                if x.parsed_url[1] in exceptions:
                        for qs in x.parsed_query_string:
                            if qs[0] == exceptions[x.parsed_url[1]]:
                                string = qs[1]
                                try:
                                    string = unhexlify(string)
                                    string = string[::-1]
                                    string = decodestring(string)
                                    string = string[::-1]
                                    string = unhexlify(string)
                                    string = string[::-1]
                                except Exception as e:
                                    logger.exception(e)
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
                                if x.check_correct(string):
                                    x.decode_method = "custom decode hex base64 hex"

            # mudou pra um mais simples
            if not x.decoded:    # 18/07/2011
                exceptions = {
                    "www.emurama.com": "id"
                }
                if x.parsed_url[1] in exceptions:
                        for qs in x.parsed_query_string:
                            if qs[0] == exceptions[x.parsed_url[1]]:
                                string = qs[1]
                                try:
                                    string = unhexlify(string)
                                    string = decodestring(string)
                                    string = string[::-1]
                                except Exception as e:
                                    logger.exception(e)
                                    pass

                                if x.check_correct(string):
                                    x.decode_method = "custom decode hex base64 reverse"

            if not x.decoded:   # 23/03/2013
                # http://www.baixandolegal.org/d/index3.php?l=aC9pdi9XdHdsZWZ1dHdlLmllcHdzY2w1Oi5lb2V4L2ZybS9FWA
                exceptions = {
                    "www.baixandolegal.org"
                }
                if x.parsed_url[1] in exceptions:
                        for qs in x.parsed_query_string:
                            qs = qs[1]
                            qs = x.base64decodefix(qs)
                            if "." not in qs:
                                qs = x.base64decodefix(qs)

                            newlist = []
                            init = 0
                            absoluteinit = 0
                            result = ""
                            i = 0   # seguranca
                            index_move = int(len(qs) ** 0.5)
                            rounds = index_move - 1
                            limit = index_move ** 2 - 1

                            while True:
                                i += 1
                                if i >= 350:
                                    break

                                newlist.append(qs[init])
                                init += index_move

                                if init >= limit:
                                    init = absoluteinit + 1
                                    absoluteinit += 1

                                if absoluteinit > rounds:
                                    result = "".join(newlist)
                                    result = result + qs[limit:]
                                    break
                            if x.check_correct(result):
                                x.decode_method = "custom decode even roundabout"

            # even cycle cypher
            if not x.decoded:
                exceptions = {
                    "protetor.download-jogo.com": "url"
                }
                # if x.parsed_url[1] in exceptions:
                if x.parsed_url[1] in exceptions:
                        for qs in x.parsed_query_string:
                            if qs[0] == exceptions[x.parsed_url[1]]:
                                string = qs[1]
                                string = string[3:len(string) - 3]
                                pos = 1
                                a = 0
                                result = ""
                                b = 0
                                try:
                                    while a < len(string):
                                        result = result + string[pos + a]
                                        a += 2
                                except Exception, a:
                                    if str(a) == "string index out of range":
                                        string = string[::-1]
                                        pos = 0
                                        while b < len(string):
                                            result = result + string[pos + b]
                                            b += 2
                                if x.check_correct(result):
                                    x.decode_method = "custom decode even roundabout"

            #simple cypher
            if not x.decoded:
                exceptions = [
                    "www.linkbuy.com.br"
                ]
                if x.parsed_url[1] in exceptions:
                    for i in x.parsed_query_string[0]:
                        element = x.parsed_query_string[0][1]
                        try:
                            string = decodestring(element)  # modelo 2: vinxp (na verdade muda so o 'h')
                            dicio = {
                                "025": "a",
                                "a56": "b",
                                "bA5": "c",
                                "Bc7": "d",
                                "AdD": "e",
                                "ec3": "f",
                                "e2d": "g",
                                "a2d": "h",
                                "ge4": "i",
                                "i6A": "j",
                                "F7e": "k",
                                "kf4": "l",
                                "21F": "m",
                                "f25": "n",
                                "m91": "o",
                                "ij5": "p",
                                "j32": "q",
                                "q56": "r",
                                "f0j": "s",
                                "f0d": "t",
                                "qs0": "u",
                                "r02": "v",
                                "5fg": "w",
                                "ppN": "x",
                                "f0C": "y",
                                "56s": "z",
                                "x5F": ":",
                                "x15": "/",
                                "sx0": ".",
                                "pxw": "?",
                                "zc0": "="
                            }
                            for a in dicio:
                                string = string.replace(a, dicio[a])

                            if x.check_correct(string):
                                x.decode_method = "custom simple cypher - linkbuy"
                        except Exception, e:
                            logger.error("erro: " + str(e) + " -- " + str(x.url))

            #simple cypher
            if not x.decoded:
                exceptions = [
                    "www.linkbuy.com.br"
                ]
                if x.parsed_url[1] in exceptions:
                    for i in x.parsed_query_string[0]:
                        element = x.parsed_query_string[0][1]
                        try:
                            string = decodestring(element)    # modelo 2: agaleradodownload
                            dicio = {
                                "025": "a",
                                "a56": "b",
                                "bA5": "c",
                                "Bc7": "d",
                                "AdD": "e",
                                "ec3": "f",
                                "e2d": "g",
                                "h": "h",
                                "ge4": "i",
                                "i6A": "j",
                                "F7e": "k",
                                "kf4": "l",
                                "21F": "m",
                                "f25": "n",
                                "m91": "o",
                                "ij5": "p",
                                "j32": "q",
                                "q56": "r",
                                "f0j": "s",
                                "f0d": "t",
                                "qs0": "u",
                                "r02": "v",
                                "5fg": "w",
                                "ppN": "x",
                                "f0C": "y",
                                "56s": "z",
                                "x5F": ":",
                                "x15": "/",
                                "sx0": ".",
                                "pxw": "?",
                                "zc0": "="
                            }
                            for a in dicio:
                                string = string.replace(a, dicio[a])

                            if x.check_correct(string):
                                x.decode_method = "custom simple cypher - linkbuy"
                        except Exception, e:
                            logger.error("erro: " + str(e) + " -- " + str(x.url))

            #inverter, base64, pegar o resultado e traduzir o ascii (mesmo resultado de javascript: fromCharCode)
            # outdated
            if not x.decoded:
                exceptions = [
                    "www.nixlove.com"
                ]
                if x.parsed_url[1] in exceptions:
                    string = x.url
                    string = string.rpartition("/")
                    string = string[2]

                    string = string[::-1]
                    try:
                        string = decodestring(string)
                    except Exception as e:
                        logger.exception(e)
                        pass

                    lst = [string[i:i + 3] for i in range(0, len(string), 3)]
                    result = ""
                    try:
                        for l in lst:
                            result += chr(int(l))
                    except Exception, e:
                        logger.error("erro: " + str(e) + " -- " + str(x.url))

                    if x.check_correct(result):
                        x.decode_method = "custom decode electron_encode crypt"

            #base64 com frescuras
            if not x.decoded:
                exceptions = [
                    "fgprotege.com"
                ]
                if x.parsed_url[1] in exceptions:
                    string = x.url

                    if string.find("aHR0") > 0:
                        init = string.find("aHR0")
                        string = string[init:]

                    if string.find("I2h0dH") > 0:
                        init = string.find("I2h0dH")
                        string = string[init:]

                    if string.find("_") > 0:
                        megaupload = string[string.find("_") + 1:]
                        try:
                            parameter = decodestring(megaupload)
                            result = "http://www.megaupload.com/?" + parameter
                        except Exception as e:
                            logger.exception(e)
                            pass

                    else:
                        try:
                            result = decodestring(string)
                        except Exception as e:
                            logger.exception(e)
                            pass

                    if result.startswith("#http:/"):
                        result = result[1:]

                    if x.check_correct(result):
                        x.decode_method = "custom base64"

            #traducao letra a letra
            if not x.decoded:
                exceptions = [
                    "www.protetor.org"
                ]
                if x.parsed_url[1] in exceptions:
                    string = x.url
                    dicio = {
                        "a": "l",
                        "b": "6",
                        "c": "j",
                        "d": "1",
                        "e": "b",
                        "f": "2",
                        "g": ".",
                        "h": "x",
                        "i": "8",
                        "j": "e",
                        "k": "u",
                        "l": "n",
                        "m": "h",
                        "n": "i",
                        "o": "9",
                        "p": "f",
                        "q": "5",
                        "r": "-",
                        "s": "7",
                        "t": "m",
                        "u": "/",
                        "v": "_",
                        "w": "0",
                        "x": "o",
                        "y": "4",
                        "z": "a",
                        "0": "c",
                        "1": "q",
                        "2": "v",
                        "3": "w",
                        "4": "t",
                        "5": "y",
                        "6": "r",
                        "7": "p",
                        "8": "w",
                        "9": ":",
                        ".": "s",
                        "-": "d",
                        ":": "g",
                        "?": "?",
                        "=": "=",
                        "/": "z",
                        "_": "k",
                        "%": "3"
                    }
                    string = string.rpartition("?h=")
                    stri = string[2]
                    lista = [c for c in stri]
                    #lista = list("asd")
                    #print lista
                    result = ""
                    for char in lista:
                        result = result + dicio[char]
                    if x.check_correct(result):
                        x.decode_method = "custom decode rotate char"

            #resolver e adicionar http:// no final
            if not x.decoded:
                exceptions = [
                    "www2.brasildownloads.net",
                    "www.brasildownloads.net"
                ]
                if x.parsed_url[1] in exceptions:
                    original_string = x.url.partition("/?url=")
                    parsed = original_string[2]
                    if not parsed.find(".") == -1:
                        x.decoded_url = "http://" + parsed
                        x.decoded = True
                        x.decode_method = "custom add http://"
                    else:
                        string = x.base64decodefix(parsed)
                        if not original_string == string:
                            x.decoded_url = "http://" + string
                            x.decoded = True
                            x.decode_method = "custom add http://"

            #url possui um codigo, que deve ser passado para outra URL, e essa deve ser parseada via regex
            if not x.decoded:
                exceptions = [
                    "download.vipdownload.com.br",
                    "downloadfilmes.biz"
                ]
                if x.parsed_url[1] in exceptions:
                    content = ""
                    try:
                        content = x.get_url_contents()
                        match = search('((?<=\()\d*?(?=(,)))', content)
                        ids = match.group(0)
                        x.url = "http://" + x.parsed_url[1] + "/linkdiscover.php?cod=" + ids
                        content = x.get_url_contents()
                    except Exception, e:
                        logger.error("erro: " + str(e) + " -- " + str(x.url))
                    try:
                        if x.check_correct(content.strip()):
                            x.decode_method = 'custom get url + regex'
                    except Exception, e:
                        logger.error("erro: " + str(e) + " -- " + str(x.url))

            #linkbucks - dominio eh dinamico, nao pode usar o generico pq a chave eh o dominio
            if not x.decoded:
                if x.parsed_url[1].find("linkbucks") > 0:
                    x.get_url_and_run_regex("((?<=TargetUrl = \')http.*?(?=(\';)))")
                    x.decode_method = 'custom domain + regex'

            #basta trocar URL e ta certo.  -- 30/01/2014
            if not x.decoded:
                exceptions = [
                    "www.hitsmp3.net"
                ]
                if x.parsed_url[1] in exceptions:
                    new_url = ""
                    try:
                        new_url = x.url.replace("download", "liberado")
                    except Exception as e:
                        logger.exception(e)
                        pass                    

                    if x.check_correct(new_url):
                        x.decode_method = 'trocando URL sem mais nada'

            if not x.decoded:
                if x.parsed_url[1] == "www.link-protegido.com":

                    #string = "em.28www//:ptthiva.zib.mumixameht.www.LL3H.pU.piRDVD.ahnitsifruS.anur
                    # B.eD.atloV.A.yxxeS/9e59d2b661136a4e819703e23a143f46/selif/moc.oedivag"
                    try:
                        parsed_query_string = parse_qs(x.parsed_url[4])
                        string = parsed_query_string['link'][0]
                        init = string.find("ptth")
                        init += 4
                        final = string[init:] + string[0:init]
                        result = final[::-1]

                        if x.check_correct(result):
                            x.decode_method = 'unscramble link-protegido on half'
                    except Exception as e:
                        logger.exception(e)
                        pass

                    #http://www.link-protegido.com/semprefilmesv2/?link=GF1EV25NG8
                    # funcionando no dia 04/07/2014
                    if not x.decoded:
                        #pegando auth da home de desprotetordelink

                        downurl = "http://www.desprotetordelink.com"
                        data = ''
                        headers = {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.6',
                                   'Referer': ''}
                        req = Request(downurl, data, headers)
                        response = urlopen(req)                        
                        cookies = response.info()["Set-Cookie"]                        
                        response = response.read()

                        soup = BeautifulSoup(response)
                        auth = soup.find('form')['action']    # index.php?auth=23cc2e1c8c366a2176d0e40f00e8b539
                        downurl = "http://www.desprotetordelink.com/" + auth + \
                                  "&link=" + x.url.replace("&", "@321").replace(":", "%3A")

                        data = ""
                        headers = {'User-Agent': 'Mozilla/5.0 AppleWebKit/537.36 (KHTML, like Gecko) Chrome/35.6',
                                   'Referer': 'http://www.desprotetordelink.com',
                                   "Cookie": cookies}
                        req = Request(downurl, data, headers)
                        response = urlopen(req)
                        response = response.read()                        

                        soup = BeautifulSoup(response)
                        form_action = soup.find('form')['action']
                        k_value = soup.find("input", {"name": "k"})["value"]
                        v_value = soup.find("input", {"name": "v"})["value"]
                        downurl = "http://www.desprotetordelink.com/" + form_action

                        data = {"v": v_value, "k": k_value}
                        import urllib
                        new_data = urllib.urlencode(data)
                        req = Request(url=downurl, data=new_data, headers=headers)
                        response = urlopen(req)
                        response = response.read()

                        try:
                            soup = BeautifulSoup(response)
                            ret = soup.find('a')['href']

                            if x.check_correct(ret.strip()):
                                x.decode_method = 'usando desprotetordelink.com(link-protegido.com)'

                        except Exception, e:
                            logger.error("erro: " + str(e) + " -- " + str(x.url))
                            logger.exception(e)

            #time lapse link-protegido.com -- 24/03/2013
            if not x.decoded:
                exceptions = [
                    "www.link-protegido.com"
                ]
                if x.parsed_url[1] in exceptions:
                    string = x.url  # url original: http://www.link-protegido.com/semprefilmesv2/?link=6HCZL0W01X
                    original_url = string

                    # trocando para a url nova: http://www.link-protegido.com/semprefilmesv2/pag.php?link=6HCZL0W01X
                    x.url = x.url.replace("/?link", "/pag.php?link")
                    content = x.get_url_contents()
                    '''no conteudo, encontrar dados de formulario:
                    <input type='hidden' value='6HCZL0W01X' id='pdifr'>
                    <input type='hidden' value='http://www.promocoeshardbox.com.br/menus/' id='lnk'>
                    <input type='hidden' value='603288105' id='login'>
                    <input type='hidden' value='5d2f8bfad194bf157e45db647bfbf4cc' id='senha'>
                    '''
                    soup = BeautifulSoup(content)
                    #pdifr = soup.find("input", {"id": "pdifr"})
                    #pdifr = pdifr["value"]

                    login = soup.find("input", {"id": "login"})
                    login = login["value"]

                    senha = soup.find("input", {"id": "senha"})
                    senha = senha["value"]
                    logger.info(login)
                    logger.info(senha)

                    # mudar para url que devolve a url desprotegida, adicionando valores capturados na URL anterior
                    x.url = x.url.replace("/pag.php", "/trocas.php")
                    x.url = x.url + "&login=" + login + "&senha=" + senha
                    content = x.get_url_contents()
                    logger.info(content)

                    if x.check_correct(content):
                        x.decode_method = "custom time lapse with double get + BeautifulSoup"
                    else:
                        x.url = original_url

            #na query string com parametros, normalmente
            if not x.decoded:
                x.deprotect_simple_query_string()

            #se ainda nao deu certo, tentar achar um hex (687474)
            if not x.decoded:
                if x.url.find('687474') > -1:
                    x.decode_hex(x.url[x.url.find('687474'):])

            #se ainda nao deu certo, tentar achar um base64 (aHR0)
            if not x.decoded:
                if x.url.find('aHR0') > -1:
                    x.decode_base64(x.url[x.url.find('aHR0'):])

            #base 64 que quando decodado fica Nome do Filme|Url
            if not x.decoded:  # 10/12/2012
                try:
                    string = x.url

                    string = x.base64decodefix(string)

                    string = string.replace("\t", "")
                    string = string.replace(" ", "")

                    string = string.split("|http")
                    string = string[1]
                    string = "http" + string
                    if string.startswith("http"):
                        x.decoded = True
                        x.decoded_url = string
                        x.decode_method = "default base64 with pipe separator, no url"
                except IndexError:
                    pass
                except Exception as e:
                    logger.exception(e)

            #se nada ainda deu certo, so reverter, caso nao tenha http escrito normal
            if not x.decoded:
                if x.url.find('http') == -1:
                    x.decode_reverse(x.url)

            #se nada ainda deu certo, so base64, caso nao tenha http escrito normal
            if not x.decoded:
                if x.url.find('http') == -1:
                    x.decode_base64(x.url)

            #se nada ainda deu certo, so hexa, caso nao tenha http escrito normal
            if not x.decoded:
                if x.url.find('http') == -1:
                    x.decode_hex(x.url)

    #decidir o que fazer quando passou por tudo do algoritmo
            if x.decoded:
                if x.decoded_url.endswith("=lru"):
                    x.decoded_url = x.decoded_url.replace("=lru", "")

                if x.decoded_url.endswith("=lru?"):
                    x.decoded_url = x.decoded_url.replace("=lru?", "")

                if x.decoded_url.endswith("=knil"):
                    x.decoded_url = x.decoded_url.replace("=knil", "")

                if x.decoded_url.endswith("!og"):
                    x.decoded_url = x.decoded_url.replace("!og", "")

                if x.decoded_url.endswith("<---||||||||||||"):
                    x.decoded_url = x.decoded_url.replace("<---||||||||||||", "")

                if x.decoded_url.endswith("---||||||||||||"):
                    x.decoded_url = x.decoded_url.replace("---||||||||||||", "")

                x.decoded_url = x.decoded_url.strip()

                try:
                    x.decoded_url = x.decoded_url.decode("utf-8", "ignore")  # tratando encodings nao ascii

                    outputlist.append({"dep": 1, "url": x.decoded_url})

                    x.insert_db_success()
                except Exception, e:
                    logger.exception(str(e))
                logger.info("Sucesso para: " + request_info.remote_addr + " - " + x.decoded_url)

            else:  # not decoded
                try:
                    response = x.get_db_answer()
                except Exception, e:
                    response = False
                    logger.exception("Erro ao pegar respostas padrao: " + str(e))

                if response is not False:
                    outputlist.append({"dep": 2, "url": x.url, "mess": str(response[1])})
                    logger.info("Blacklist para: " + response[0] + " - " + x.url)
                    if response[2] == 1:
                        try:
                            x.insert_db_failure()
                        except Exception, e:
                            logger.error("Erro ao inserir falha: " + str(e) + " Url: " + x.url)
                else:
                    if not x.valid:

                        outputlist.append({"dep": 3, "url": x.url, "mess": "nao parece um protetor"})
                    else:
                        outputlist.append({"dep": 0, "url": x.url})
                        logger.info("Falha para " + request_info.remote_addr + " - " + x.url)
                        try:
                            x.insert_db_failure()
                        except Exception, e:
                            logger.error("Erro ao inserir falha: " + str(e) + " Url: " + x.url)

    out = outputlist
    return str(dumps(out))


if __name__ == '__main__':
    app.debug = True
    app.run()