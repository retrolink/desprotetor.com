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

        

        '''
        #decode scramble string
        if not x.decoded:
                if x.parsed_url[1] == "www.link-protegido.com":
                        string = x.url
                        dicio = {
                        "00":"0",
                        "01":"1",
                        "02":"2",
                        "03":"3",
                        "04":"m",
                        "05":"r",
                        "06":"6",
                        "07":"w",
                        "08":"8",
                        "09":"9",
                        "10":"z",
                        "11":".",
                        "12":"!",
                        "13":"&",
                        "14":"_",
                        "15":"?",
                        "16":"=",
                        "17":"k",
                        "18":"i",
                        "19":"g",
                        "20":"f",
                        "21":"p",
                        "22":"t",
                        "23":"23",
                        "24":"y",
                        "25":":",
                        "26":"[",
                        "27":"]",
                        "28":"@",
                        "29":"29",
                        "30":"%",
                        "31":"31",
                        "32":"-",
                        "33":"|",
                        "34":"/",
                        "35":"x",
                        "36":"u",
                        "37":"v",
                        "38":"s",
                        "39":"q",
                        "40":"o",
                        "41":"l",
                        "42":"h",
                        "43":"e",
                        "44":"a",
                        "45":"b",
                        "46":"d",
                        "47":"j",
                        "48":"48",
                        "49":"49",
                        "50":"n",
                        "51":"51",
                        "52":"c",
                        "53":"53",
                        "54":"A",
                        "55":"H",
                        "56":"O",
                        "57":"T",
                        "58":"V",
                        "59":"E",
                        "60":"B",
                        "61":"D",
                        "62":"L",
                        "63":"Q",
                        "64":"R",
                        "65":"P",
                        "66":"F",
                        "67":"C",
                        "68":"G",
                        "69":"J",
                        "70":"K",
                        "71":"N",
                        "72":"S",
                        "73":"U",
                        "74":"X",
                        "75":"Y",
                        "76":"Z",
                        "77":"W",
                        "78":"M",
                        "79":"I",
                        "80":"80",
                        "81":"1",
                        "82":"8",
                        "83":"5",
                        "84":"3",
                        "85":"4",
                        "86":"2",
                        "87":"7",
                        "88":"6",
                        "89":"9",
                        "90":"90",
                        "91":"91",
                        "92":"0",
                        "93":"93",
                        "94":"94",
                        "95":"95",
                        "96":"96",
                        "97":"97",
                        "98":"98",
                        "99":"99"}
                        string = string.rpartition("?link=")
                        stri = string[2]
                        stri = stri[:-4]

                        i = 0
                        a = 0
                        result = ""
                        while i < len(stri)/2:     
                            #logger.info("while 1 rodando: "+x.url)   
                            try:
                                result = result + dicio[stri[a:a+2]]
                                a = a+2
                                i = i+1
                            except Exception:
                                break                             

                        string = result

                        init = string.find("thtp")+1
                        num = 0
                        result = ''

                        while len(result) < len(string):
                            #logger.info("while 2 rodando: "+x.url)   
                            if num == 0:
                                result = string[init]
                                num = num+1
                            else:
                                result = result + string[init+num]
                                result = result + string[init+(num*-1)]
                                num = num+1

                        if result.startswith("http:/"):    
                            if result != "http://www.desprotetordelink.com/":                        
                                x.decoded = True
                                x.decoded_url = result
                                x.decode_method = 'link-protegido - unkey'


        
        #decode scramble string
        if not x.decoded:
                if x.parsed_url[1] == "www.link-protegido.com":
                    #string = "/:thtp/wwflsrecmfl/JEqJr76ei/o.veei.w"                    
                    try:
                        parsed_query_string = cgi.parse_qs(x.parsed_url[4])
                        string = parsed_query_string['p2'][0]

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
                            x.decoded_url = result
                            x.decode_method = 'unscramble'
                    except Exception:
                        pass
                    
             
        #link-protegido.com
        if not x.decoded:
            if x.parsed_url[1] == "www.link-protegido.com":
                try:
                    x.parsed_query_string = cgi.parse_qs(x.parsed_url[4])
                    x.url = x.parsed_url[0] + "://" + x.parsed_url[1] + x.parsed_url[2] + 'pag.php?link=' + x.parsed_query_string['link'][0]
                    content = x.get_url_contents()
                    
                    soup = BeautifulSoup(content)            
                    login = soup.find('input', id="login")['value']
                    senha = soup.find('input', id="senha")['value']
                    encoded = soup.find('input', id="pdifr")['value']                
                              
                    login = int(login)-100300000 
                    login = str(login)
                    
                    m = hashlib.md5()
                    m.update(login)
                    senha = m.hexdigest()
                    
                    x.url = x.parsed_url[0] + "://" + x.parsed_url[1] + x.parsed_url[2] + 'trocas.php?link=' + encoded + '&login=' + login + '&senha=' + senha
        
                    content = x.get_url_contents()
                    if content.strip().startswith("http:/"):
                        if not content.strip().startswith("http://www.desprotetordelink.com/"):
                            x.decoded = True
                            x.decoded_url = content
                            x.decode_method = 'custom get url x2 with time lapse + regex'
                except Exception:
                    pass
        '''