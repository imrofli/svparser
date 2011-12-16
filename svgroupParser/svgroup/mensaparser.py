from BeautifulSoup import BeautifulSoup
from mensa import mensa
import re
import sqlite3

class mensaparser(object):
    def __init__(self, form):
        self.mensalist = []
        self.result=''
        self.data=''
        self.buffer=''
        self.form=form
    def printAll(self):
        out=''
        for entry in self.mensalist:
            out += '\n' + entry.__str__()
        if self.form==2:
            out=out[:-1]
        return self.printHead() + out + self.printFoot()
    def printHead(self):
        if self.form==1:
            return '<?xml version="1.0" encoding="UTF-8" ?>\n<root>'
        elif self.form==2:
            return '{\n\t\"root\":{"mensa\":[\n\t\t\t'
    def printFoot(self):
        if self.form==1:
            return '</root>'
        elif self.form==2:
            return '\n\t\t\t]\n\t\t}\n\t}'
    def writeInDB(self):
        conn = sqlite3.connect('data.SQLITE3')
        c = conn.cursor()
        c.execute('DROP TABLE mensas')
        c.execute("""CREATE TABLE mensas ( ID        INTEGER PRIMARY KEY AUTOINCREMENT,name      TEXT,owner     TEXT,address   TEXT,plz       INT,city      TEXT,telephone TEXT,opentime  TEXT,website   TEXT,subdomain TEXT,longitude TEXT,latitude  TEXT );""")
        # Insert a row of data
        for entry in self.mensalist:
            c.execute("""insert into mensas values (null, ?,?,?,?,?, ?, ?, ?,?, ?, ?)""", [entry.name, entry.owner,entry.address, entry.plz, entry.city, entry.telephone, entry.opentime, entry.website, entry.subdomain, entry.Glength, entry.Gwidth])
        # Save (commit) the changes
        conn.commit()
        
        # We can also close the cursor if we are done with it
        c.close()
    def parse(self, data):
        self.data=data
        soup = BeautifulSoup(self.data)
        self.result = soup.findAll('script' , {'type':'text/javascript'})
        bufferList=[]
        for element in self.result:
            for tmp in element.findAll(text=True):
                bufferList+=tmp.splitlines()
        for item in bufferList:
            cntr=0
            if re.match('createMarker\(new.*\)', item):
                mensaBuffer = mensa(self.form)
                for ext in re.split('<b>|<br>', item):
                    ext=ext.split('</b>')[0]
                    ext=ext.split('\');')[0]
                    ext=ext.split(', \'')[0]
                    if re.match('createMarker\(new.*\)', ext):
                        grades = ext.split('createMarker(new GLatLng(')[-1].split(')')[0]
                        mensaBuffer.setGl(grades.split(',')[0])
                        mensaBuffer.setGw(grades.split(',')[1])
                    elif cntr==1:
                        mensaBuffer.setname(ext.strip())
                    elif cntr==2 and not re.match('.+\s+.*\d+.*', ext.strip()):
                        mensaBuffer.setowner(ext.strip())
                    elif re.match('<a href=\".*\"', ext):
                        link = ext.split('<a href=\"')[-1].split('\"')[0]
                        mensaBuffer.setwebsite(link)
                        mensaBuffer.setsubdomain(link.split('http://')[-1].split('.')[0])
                    elif re.match('\d\d\d\d\s\S+', ext):
                        mensaBuffer.setplz(ext.split(' ')[0])
                        mensaBuffer.setcity(ext.split(' ')[1])
                    elif re.match('.+\+.+', ext) or re.match('.*Telefon.*', ext):
                        mensaBuffer.settel(ext)
                    elif re.match('.+\s.+', ext) and cntr < 4:
                        mensaBuffer.setaddress(ext.strip())
                    else:
                        if len(ext):
                            if len(mensaBuffer.opentime):
                                mensaBuffer.opentime+='\n'
                            mensaBuffer.opentime+=ext.strip() 
                    
                    cntr+=1
                self.mensalist.append(mensaBuffer)