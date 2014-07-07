from __future__ import with_statement
import MySQLdb
import logging
import sys
import shutil
import simplejson
import hashlib
import datetime
import os
from settings import settings


logger = logging.getLogger('dep')
hdlr = logging.FileHandler(settings.application_log)
formatter = logging.Formatter('%(asctime)s %(levelname)s %(module)s %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)


class Process:
    def __init__(self, linelist, dbobj):
        self.numberOfFailures = 0
        self.numberOfSuccesses = 0
        self.numberOfLinesOnLog = 0
        self.dbobj = dbobj
        self.numberOfLinesOnLog = len(linelist)
        #for i in iter(linelist.splitlines()):
        #    self.numberOfLinesOnLog += 1

        logger.info("Iniciando processamento. Arquivo de log com %s linhas." % self.numberOfLinesOnLog)

        for line in linelist:  # passando por todas as linhas do log
            try:
                linejson = simplejson.loads(line)
            except Exception as exc:
                logger.critical("Erro ao processar uma linha do arquivo: %s" % exc)
                continue
            if linejson["type"] == 1:  # desprotecao
                try:
                    self.process_deprotection(linejson)
                except Exception as exc2:
                    logger.critical("Erro ao processar uma linha do arquivo: %s " % exc2)
                    continue
            if linejson["type"] == 2:  # verify
                self.process_verify(linejson)
        else:
            self.update_daily_statistics()
            self.finish()

    def process_verify(self, linejson):
        pass

    def process_deprotection(self, linejson):
        if linejson["success"] == 1:

            today = datetime.date.today()
            today = today.strftime("%Y-%m-%d")
            hsh = linejson["domain"] + linejson["method"] + today
            m = hashlib.md5()
            m.update(hsh)
            hsh = m.hexdigest()

            hash_extension = linejson["extension"] + today
            m = hashlib.md5()
            m.update(hash_extension)
            hash_extension = m.hexdigest()

            domain = linejson["domain"].encode("UTF-8")
            method = linejson["method"].encode("UTF-8")
            original_url = linejson["originalUrl"].encode("UTF-8")
            decoded_url = linejson["decoded_url"].encode("UTF-8")
            extension = linejson["extension"]

            query = """INSERT INTO deprotect_py_domain_method (hash,domain,method,num,date) VALUES
            ('""" + hsh + """','""" + domain + """','""" + method + """',1,'""" + today + """')
            ON DUPLICATE KEY UPDATE num = num +  VALUES(num);"""
            self.dbobj.query(query)

            query = """INSERT INTO deprotect_py_success_urls (url,result,date) VALUES
            ('""" + original_url + """','""" + MySQLdb.escape_string(decoded_url) \
                    + """',DATE_ADD(NOW(),INTERVAL 6 HOUR));"""
            self.dbobj.query(query)

            query = """INSERT INTO deprotect_py_extension (hash,date,extension,num) VALUES
            ('""" + hash_extension + """',DATE_ADD(NOW(),INTERVAL 6 HOUR),'""" + extension + """',1)
            ON DUPLICATE KEY UPDATE num = num +  VALUES(num);;"""
            self.dbobj.query(query)
            self.dbobj.store_result()
            self.numberOfSuccesses += 1

        else:
            self.insert_failure(linejson["domain"], linejson["originalUrl"])
            self.numberOfFailures += 1

    def insert_failure(self, domain, url):
        query = """INSERT INTO deprotect_py_fail (domain,url) VALUES ('""" + domain + """', '""" + url + """');"""
        self.dbobj.query(query)
        self.dbobj.store_result()

    def update_daily_statistics(self):
        logger.info("Atualizando estatisticas diarias: %s sucessos e %s falhas. " %
                    (self.numberOfSuccesses, self.numberOfFailures))
        query = """INSERT INTO deprotect_py_success_fail (date,success,fail) VALUES (date(now()),""" + \
                str(self.numberOfSuccesses)+""",""" + str(self.numberOfFailures) + \
                """) ON DUPLICATE KEY UPDATE success = success+ VALUES(success) , fail = fail + VALUES(fail);"""
        self.dbobj.query(query)
        self.dbobj.store_result()

    def finish(self):
        os.remove(settings.temp_data_log)
        logger.info("Finalizando processamento. Arquivo com %s linhas." % self.numberOfLinesOnLog)


class DbCache:
    def __init__(self, connection):
        self.db = connection
        self.dbcursor = self.db.cursor()
        self.answerJsonData = ""

        if self.update_answer_json():
            try:
                file_obj = open(settings.answer_json_file, 'w')
                file_obj.writelines(simplejson.dumps(self.answerJsonData))
                file_obj.close()
            except IOError:
                logger.critical('Couldnt save to file')

    def update_answer_json(self):
        query = """select domain,answer,log_as_fail from deprotect_py_answer"""
        num_rows = self.dbcursor.execute(query)
        if num_rows > 0:
            data = self.dbcursor.fetchall()
            self.answerJsonData = data
            return True
        else:
            return False


if __name__ == "__main__":
    logger.info("Processor inicado. Conectando ao DB...")
    try:
        dbconnection = MySQLdb.connect(host=settings.dbhost,
                                       user=settings.dbuser,
                                       passwd=settings.dbpass,
                                       db=settings.dbbase)
    except Exception, e:
        logger.critical("Erro ao conectar com o banco de dados: %s" % e)
        sys.exit(1)

    logger.info("Atualizando Answer Json")
    cache = DbCache(dbconnection)

    logger.info("Movendo arquivo de log...")
    try:
        #nao posso apenas mover o arquivo ja que o wsgi mantem o socket em memoria.
        #preciso copiar o arquivo, apagar apenas o conteudo do velho
        shutil.copy(settings.data_log, settings.temp_data_log)
        open(settings.data_log, 'w').close()

    except Exception, e:
        logger.critical("Erro ao mover arquivo de log: "+str(e))
        logger.exception(e)
        sys.exit(1)

    logger.info("Abrindo arquivo temporario.")
    try:
        with open(settings.temp_data_log, 'r') as f:
            read_data = f.read()
            line_list = read_data.splitlines()
            processor = Process(line_list, dbconnection)
    except Exception, e:
        logger.critical("Erro ao processar arquivo de log temporario: "+str(e))
        logger.exception(e)
        sys.exit(1)