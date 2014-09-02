import sys
import urllib2
import socket
import collections
import operator

fname = "/home/ubuntu/sites/desprotetor.com/src/log/user_agent.log"
limit = 30


SMTPserver = 'mail.desprotetor.com'
sender =     'contato_br@desprotetor.com'
destination = ['marcelo.kronberg@gmail.com']

USERNAME = "contato_br@desprotetor.com"
PASSWORD = "nemesistk421"

# typical values for text_subtype are plain, html, xml
text_subtype = 'html'

subject="Avaliacao de IPs suspeitos"






with open(fname) as f:
    content = f.readlines()

results = {}
for line in content:
    elements = line.strip().split(" :: ")    
    ip = elements[0]
    user_agent = elements[1]
    if ip in results:
        results[ip]["count"] = results[ip]["count"] + 1
        results[ip]["ua"] = user_agent
    else:
        results[ip] = {}
        results[ip]["count"] = 1
        results[ip]["ua"] = user_agent

dict_list = []
for result in results:
    dict_list.append({"ip": result, "count": results[result]["count"], "ua": results[result]["ua"]})

newlist = sorted(dict_list, key=lambda k: k['count'], reverse=True) 
del dict_list
del content
del results

count = 0
mail_content = []
for element in newlist:
    if count >= limit:
        break
    try:
        response = urllib2.urlopen('http://' + element["ip"] + '/', timeout=5)
        html = response.read()
        
        try:
            reverse_dns = socket.gethostbyaddr(ip)
            content = "Suspicious"
        except Exception, e:
            reverse_dns = "not found"
            content = "Suspicious"

    except Exception, e:        
        content = e
        reverse_dns = "-"
    count = count + 1
    mail_content.append({"ip": element["ip"], "reps": element["count"], "content": content, "reverse_dns": reverse_dns, "ua": element["ua"]})

content = "<table border=1>"
content += "<tr><th>IP</th><th>Repetitions</th><th>Content</th><th>Reverse DNS</th><th>User Agent</th></tr>"
    
for line in mail_content:
    content += "<tr><td><a href='" + str(line["ip"]) + "'>" + str(line["ip"]) + "</a></td><td>" + str(line["reps"]) + "</td><td>" + str(line["content"]) + "</td><td>" + str(line["reverse_dns"]) + "</td><td>" + str(line["ua"]) + "</td></tr>"

content += "</table>"


import os
import re

#from smtplib import SMTP_SSL as SMTP       # this invokes the secure SMTP protocol (port 465, uses SSL)
from smtplib import SMTP                  # use this for standard SMTP protocol   (port 25, no encryption)
from email.MIMEText import MIMEText

try:
    msg = MIMEText(content, text_subtype)
    msg['Subject']=       subject
    msg['From']   = sender # some SMTP servers will do this automatically, not all

    conn = SMTP(SMTPserver)
    conn.set_debuglevel(False)
    conn.login(USERNAME, PASSWORD)
    try:
        conn.sendmail(sender, destination, msg.as_string())
    finally:
        conn.close()

except Exception, exc:
    sys.exit( "mail failed; %s" % str(exc) ) # give a error message
