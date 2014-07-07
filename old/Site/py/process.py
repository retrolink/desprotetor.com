from __future__ import with_statement #pra rodar no python 2.5 velhao
import MySQLdb, logging, sys, shutil, simplejson, hashlib, datetime, os
import settings


logger = logging.getLogger('dep')
hdlr = logging.FileHandler(settings.application_log)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
fsock = open(settings.application_log, 'a')
sys.stderr = fsock


class process:
    def __init__(self,linelist,dbobj):        
        self.numberOfFailures = 0
        self.numberOfSuccesses = 0
        self.numberOfLinesOnLog = 0
        self.dbobj = dbobj

        for line in iter(linelist.splitlines()):
            self.numberOfLinesOnLog = self.numberOfLinesOnLog + 1

        logger.info("Iniciando processamento. Arquivo de log com "+ str(self.numberOfLinesOnLog) +" linhas.")

        for line in iter(linelist.splitlines()): #passando por todas as linhas do log
            linejson = simplejson.loads(line)
            if linejson["type"] == 1: #desprotecao
                self.processDeprotection(linejson)
            if linejson["type"] == 2: #verify
                self.processVerify(linejson)
        else:
            self.updateDailyStatistics()            
            self.finish()

    def processVerify(self,linejson):
        pass

    def processDeprotection(self,linejson):        
        if linejson["success"] == 1:

            today = datetime.date.today()
            today = today.strftime("%Y-%m-%d")
            hash = linejson["domain"] + linejson["method"] + today
            m = hashlib.md5()
            m.update(hash)
            hash = m.hexdigest()

            hash_extension = linejson["extension"] + today
            m = hashlib.md5()
            m.update(hash_extension)
            hash_extension = m.hexdigest()

            try:
                domain = linejson["domain"].encode("UTF-8")
                method = linejson["method"].encode("UTF-8")
                originalUrl = linejson["originalUrl"].encode("UTF-8")
                decodedUrl = linejson["decoded_url"].encode("UTF-8")
                extension = linejson["extension"]


                query = """INSERT INTO deprotect_py_domain_method (hash,domain,method,num,date) VALUES ('""" + hash + """','""" + domain + """','""" + method + """',1,'""" + today + """') ON DUPLICATE KEY UPDATE num = num +  VALUES(num);"""        
                self.dbobj.query(query)
                query = """INSERT INTO deprotect_py_success_urls (url,result,date) VALUES ('""" + originalUrl + """','""" + decodedUrl + """',DATE_ADD(NOW(),INTERVAL 6 HOUR));"""        
                self.dbobj.query(query)        
                query = """INSERT INTO deprotect_py_extension (hash,date,extension,num) VALUES ('""" + hash_extension + """',DATE_ADD(NOW(),INTERVAL 6 HOUR),'""" + extension + """',1) ON DUPLICATE KEY UPDATE num = num +  VALUES(num);;"""        
                self.dbobj.query(query)
                r = self.dbobj.store_result()
                self.numberOfSuccesses = self.numberOfSuccesses + 1
            except Exception, e:
                logger.exception("Erro ao inserir dados no banco: "+str(e))
                #alarmar
                sys.exit(1)

            
        else:
            self.insertFailure(linejson["domain"],linejson["originalUrl"])
            self.numberOfFailures = self.numberOfFailures + 1


    def insertFailure(self,domain,url):
        query = """INSERT INTO deprotect_py_fail (domain,url) VALUES ('"""+ domain +"""', '""" + url + """');"""
        self.dbobj.query(query)
        r = self.dbobj.store_result()


    def updateDailyStatistics(self):
        logger.info("Atualizando estatisticas diarias: "+str(self.numberOfSuccesses)+" sucessos e "+str(self.numberOfFailures)+" falhas")      
        query = """INSERT INTO deprotect_py_success_fail (date,success,fail) VALUES (date(now()),"""+str(self.numberOfSuccesses)+""","""+str(self.numberOfFailures)+""") ON DUPLICATE KEY UPDATE success = success+ VALUES(success) , fail = fail + VALUES(fail);"""
        self.dbobj.query(query)        
        r = self.dbobj.store_result()

    def finish(self):
        os.remove(settings.temp_data_log)        
        #mover dados muito antigos da tabelona monstro: deprotect_py_success_urls para historico
        logger.info("Finalizando processamento")



class dbCache:
    def __init__(self,dbconnection):
        self.db = dbconnection
        self.dbcursor = self.db.cursor()
        self.answerJsonData = ""

        if self.updateAnswerJson():
            try:
                file = open(settings.answer_json_file, 'w')
                file.writelines(simplejson.dumps(self.answerJsonData))
                file.close()
            except IOError:
                logger.critical('Coulnt save to file')



    def updateAnswerJson(self):
        query = """select domain,answer,log_as_fail from deprotect_py_answer"""
        numRows = self.dbcursor.execute(query)
        if numRows > 0:
            data = self.dbcursor.fetchall()       
            self.answerJsonData = data
            return True
        else:
            return False




logger.info("Processor inicado. Conectando ao DB...")
try:
    dbconnection = MySQLdb.connect(host=settings.dbhost,user=settings.dbuser,passwd=settings.dbpass,db=settings.dbbase)
except Exception, e:
    logger.critical("Erro ao conectar com o banco de dados: "+str(e))
    #alarmar
    sys.exit(1)

logger.info("Atualizando Answer Json")
cache = dbCache(dbconnection)


logger.info("Movendo arquivo de log...")
try:
    shutil.move(settings.data_log, settings.temp_data_log)
except Exception, e:
    logger.critical("Erro ao mover arquivo de log: "+str(e))
    sys.exit(1)

logger.info("Abrindo arquivo temporario.")
try:
    with open(settings.temp_data_log, 'r') as f:
        read_data = f.read()
        processor = process(read_data,dbconnection)
except Exception, e:
    logger.critical("Erro ao processar arquivo de log temporario: "+str(e))
    sys.exit(1)



