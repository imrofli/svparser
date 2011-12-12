#!/usr/bin/env python
import httplib
import sys
from svparser import svparser
sys.stderr = sys.stdout

def check_int(s):
    if s[0] in ('-', '+'):
        return s[1:].isdigit()
    return s.isdigit()

if (len(sys.argv) > 1):
    if sys.argv[1].isdigit():
        weekday = int(sys.argv[1])
    else:
        weekday = 0
    if sys.argv[2].isdigit():
        form = int(sys.argv[2])
    else:
        form = 0
    if check_int(sys.argv[3]):
        weekDiff = int(sys.argv[3])
    else:
        weekDiff = 0
    subdomain=sys.argv[4]
else:
    weekday = 0
    form = 0
    weekDiff = 0
    subdomain = 'hochschule-rapperswil'
    
if weekday < 8 and weekday > -1:
    h1 = httplib.HTTPConnection(subdomain + '.sv-group.ch')
    h1.request('GET', '/de/menuplan.html?addGP[weekday]=' + str(weekday) + '&addGP[weekmod]=' + str(weekDiff))
    res = h1.getresponse()
    if res.status != 200:
        print 'Errr!!!! Address seems to be a troublesome URL. The "Internet" says "', res.reason, '" and the status was', res.status, '. Try again.'
    else:
        data = res.read()
        allheaders = res.getheaders()
        parse = svparser(form, subdomain)
        parse.parse(data)
        print parse.printAll().encode("utf-8")
else:
    print 'ERROR 001: Fucking idiot. how many workdays does a week have? Right... 5'
