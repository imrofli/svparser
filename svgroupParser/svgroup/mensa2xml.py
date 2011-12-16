#!/usr/bin/env python
import httplib
import sys
from mensaparser import mensaparser
sys.stderr = sys.stdout

def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

if (len(sys.argv) > 1):
    if sys.argv[1].isdigit():
        form = int(sys.argv[1])
    else:
        form = 1
else:
    form = 1


h2 = httplib.HTTPConnection('www.sv-group.ch')
h2.request('GET', '/de/privatpersonen/personalrestaurants/personalrestaurantsuche.html')
res2 = h2.getresponse()
data2=res2.read()
allheaders2=res2.getheaders()
parse2=mensaparser(form)
parse2.parse(data2)
if form==2:
    file = open('mensas.json', 'w')
else:
    file = open('mensas.xml', 'w')
file.seek(0)
file.write(parse2.printAll().encode('utf-8'))
parse2.writeInDB()
print 'done!'
