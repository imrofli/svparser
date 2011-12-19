#!/usr/bin/env python

from BeautifulSoup import BeautifulSoup
from menu import menu
import re
import sqlite3

class menuparser(object):
    def __init__(self, form, subdomain):
        self.data = ''
        self.buffer = ''
        self.result = ''
        self.date = ''
        self.menuList = []
        self.form=form
        self.subdomain=subdomain
    def printAll(self):
        self.save+=self.printHead()
        for item in self.menuList:
            self.save+= item.__str__()
        if self.form==2:
            self.save=self.save[:-1]
        self.save+=self.printFoot()
        return self.save
    def writeInDB(self):
        conn = sqlite3.connect('data.SQLITE3')
        c = conn.cursor()
        c.execute("""select * from mensa2menu where subdomain=? and date=?""", [self.subdomain, self.date])
        if not (self.date == 'Geschlossen') and len(c.fetchall())==0 :
            c.execute("""insert into mensa2menu values (?, ?)""", [self.subdomain, self.date])
            for entry in self.menuList:
                c.execute("""insert into menu values (null, ?,?,?,?,?,?, ?)""", [entry.name , entry.starter,entry.maindish, entry.priceInt, entry.priceExt, self.date, self.subdomain])

            conn.commit()
            c.close()
    def printHead(self):
        if self.form==1:
            return '<?xml version="1.0" encoding="UTF-8" ?>\n<day>\n<date>' + self.date + '</date>'
        elif self.form==2:
            return '{\n\t\"day\":{"date":"'+ self.date +'",\n\t\t\"menu\":[\n\t\t\t'
        else:
            return '<!DOCTYPE html>\n<html>\n   <head>\n     <title>' +self.subdomain+' Mensa Menuplan</title>\n     <link rel="icon" type="image/png" href="./favicon.png">\n    <link rel="apple-touch-icon" href="./ifavicon.png">\n     <link href=\'http://fonts.googleapis.com/css?family=Prociono\' rel=\'stylesheet\' type=\'text/css\'>\n    <link rel=\"stylesheet\" type=\"text/css\" href=\"design.css\" />\n   </head>\n   <body>\n     <div id="main"><h1>' + self.date + '</h1>'
    def printFoot(self):
        if self.form==1:
            return '</day>'
        elif self.form==2:
            return '\n\t\t\t]\n\t\t}\n\t}'
        else:
            return '</div>\n  </body>\n</html>'
    def parse(self, data):
        self.data = data
        self.save=''
        soup = BeautifulSoup(self.data)
        self.result = soup.find('div', { "class" : "date" })
        if self.result == None:
            self.date= 'Geschlossen'
        else:
            self.date = self.result.find(text=True)
            self.date = self.date.split(", ")[1]
        self.result = ''
        self.result = soup.findAll('div', { "class" : "menuitem" })
        for element in self.result:
            cntr = 0
            menubuffer = menu()
            menubuffer.setform(self.form)
            for tmp in element.findAll(text=True):
                if not re.match('.*Take.*away.*', tmp) and re.match('\s*\S+\s*', tmp):
                    tmp = tmp.strip()
                    tmp = ' '.join(tmp.split())
                    if cntr == 0:
                        menubuffer.setname(tmp)
                    elif cntr == 1:
                        menubuffer.setstarter(tmp)
                    elif cntr > 1:
                        maindish = menubuffer.maindish + ' ' + tmp
                        menubuffer.setmaindish(maindish)
                    cntr += 1
            self.menuList.append(menubuffer)
        self.result = soup.findAll('div', { "class" : "price" })
        cntr = 0
        for element in self.result:
            priceNr=0
            price = ''
            for tmp in element.findAll(text=True):
                if re.match('\s*\S+\s*', tmp):
                    tmp=tmp.strip()
                    if priceNr>0:
                        price = tmp
                        self.menuList[cntr].setpriceExt(price)
                    else:
                        price = tmp
                        priceNr+=1
                        self.menuList[cntr].setpriceInt(price)
            cntr+=1