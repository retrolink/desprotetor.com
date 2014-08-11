#!/usr/bin/python

import os

#dados do DB, para uso no process.py
dbhost = "mysql.mkron.net"
dbuser = "kronapps"
dbpass = "nemesistk421"
dbbase = "mkronnet_apps"

#data_log = "/home/mkron/desprotetor.com/py/log/dep_data.log"
#temp_data_log = "/home/mkron/desprotetor.com/py/log/dep_temp_data.log"
#application_log = "/home/mkron/deprotect.log"
#answer_json_file = "/home/mkron/desprotetor.com/py/data/answer.json"

#tem alguma forma melhor que essa?
parent_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


data_log = parent_dir+"/data/dep_data.log"
temp_data_log = parent_dir+"/data/dep_temp_data.log"
answer_json_file = parent_dir+"/data/answer.json"

application_log = parent_dir+"/log/deprotect.log"
user_agent_log = parent_dir+"/log/user_agent.log"



