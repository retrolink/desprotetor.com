import urllib2, re
from random import choice

data = ''
headers = { 'User-Agent' : 'Mozilla/5.0 (Windows; U; Windows NT 6.0; en-GB; rv:1.9.2.9) Gecko/20100824 Firefox/3.6.9 ( .NET CLR 3.5.30729; .NET CLR 4.0.20506)', 'Referer' : 'http://google.com'}                            
req = urllib2.Request("http://www.cool-proxy.net/index.php?action=anonymous-proxy-list&sort=response_time_average&sort-type=asc", data, headers)
response = urllib2.urlopen(req)
content = response.read()

#http://www.proxylists.net/rss.xml

ip = re.findall( r'[0-9]+(?:\.[0-9]+){3}\:[0-9]{2,5}', content )
print ip


try:
	proxy = urllib2.ProxyHandler({'http': choice(ip)})
	opener = urllib2.build_opener(proxy)
	urllib2.install_opener(opener)
	response = urllib2.urlopen('http://www.megaupload.com/?d=3A7DQO6Z')
	print response.read()
except Exception:
	print 'fail!'