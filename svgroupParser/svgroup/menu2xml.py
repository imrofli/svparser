#!/usr/bin/env python
import httplib
import sys
from menuparser import menuparser
from datetime import date, datetime
import re
sys.stderr = sys.stdout

def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

if (len(sys.argv) > 1):
    if re.match('\d+\.\d+\.\d\d\d\d', sys.argv[1]):
        buff = sys.argv[1]
        c = datetime.strptime(buff,"%d.%m.%Y")
        dateset = c.date()
    else:
        dateset = date.today()
    if sys.argv[2].isdigit():
        form = int(sys.argv[2])
    else:
        form = 0
    subdomain=sys.argv[3]
else:
    dateset = date.today()
    form = 0
    subdomain = 'hochschule-rapperswil'
    
today = date.today()
datediff = dateset.isocalendar()[1] - today.isocalendar()[1]
    
h1 = httplib.HTTPConnection(subdomain + '.sv-group.ch')
h1.request('GET', '/de/menuplan.html?addGP[weekday]=' + str(dateset.isoweekday()) + '&addGP[weekmod]=' + str(datediff))
res = h1.getresponse()
if res.status != 200:
    print 'Errr!!!! Address seems to be a troublesome URL. The "Internet" says "', res.reason, '" and the status was', res.status, '. Try again.'
else:
    data = res.read()
    allheaders = res.getheaders()
    parse = menuparser(form, subdomain)
    parse.parse(data)
    parse.writeInDB()
#    print parse.printAll().encode("utf-8")
#    print str(dateset.isoweekday()) + " " + str(datediff)

    
