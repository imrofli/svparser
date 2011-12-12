#!/usr/bin/env python
import json

class mensa(object):
    def __init__(self):
        self.name=''
        self.owner=''
        self.address=''
        self.plz=''
        self.city=''
        self.telephone=''
        self.opentime=''
        self.website=''
        self.subdomain=''
        self.Glength=''
        self.Gwidth=''
        self.form=0
    def __str__(self):
        out=''
        if self.form==1:
            out= '<mensa>\n<name>' + self.name + '</name>\n<owner>' + self.owner + '</owner>\n<address>' + self.address + '</address>\n<plz>' + self.plz +'</plz>\n<city>' + self.city + '</city>\n<telephone>' + self.telephone + '</telephone>\n<opentime>' + self.opentime + '</opentime>\n<website>' + self.website + '</website>\n<subdomain>' + self.subdomain + '</subdomain>\n<longitude>' + self.Glength + '</longitude>\n<latitude>' + self.Gwidth + '</latitude>\n</mensa>'
        elif self.form==2:
            out = '\t{\"name\":'+self.name+',\n\t\t\t\t\"owner\":' + self.owner + ',\n\t\t\t\t\"address\":' + self.address + ',\n\t\t\t\t\"price\":{\n\t\t\t\t\t\"int\":\"' + self.priceInt + '\",\n\t\t\t\t\t\"ext\":\"' + self.priceExt + '\"\n\t\t\t\t}\n\t\t\t},' 
        else:
            out = '<h2>' + self.name + '</h2>\n' + '<p>' + self.owner + '<br>' + self.address + '<br>' + self.priceInt + ' - ' + self.priceExt + '</p>'
        return out  
    def setname(self, name):
        self.name=name
    def setowner(self, owner):
        self.owner=owner
    def setaddress(self, address):
        self.address=address
    def setplz(self, plz):
        self.plz=plz
    def setcity(self, city):
        self.city=city
    def settel(self, tel):
        self.telephone=tel
    def setopentime(self, opentime):
        self.opentime=opentime
    def setwebsite(self, web):
        self.website=web
    def setsubdomain(self, subdomain):
        self.subdomain=subdomain
    def setGl(self, gl):
        self.Glength=gl
    def setGw(self, gw):
        self.Gwidth=gw
    def setform(self, form):
        self.form =form