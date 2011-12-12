#!/usr/bin/env python
import json

class menu(object):
    def __init__(self):
        self.name=''
        self.starter=''
        self.maindish=''
        self.priceInt=''
        self.priceExt=''
        self.form=0
    def __str__(self):
        out=''
        if self.form==1:
            out= '<menu>\n<name>' + self.name + '</name>\n<starter>' + self.starter + '</starter>\n<maindish>' + self.maindish + '</maindish>\n<price>\n<Int>' + self.priceInt + '</Int>\n<Ext>' + self.priceExt + '</Ext>\n</price>\n</menu>'
        elif self.form==2:
            out = '\t{\"name\":'+json.dumps(self.name)+',\n\t\t\t\t\"starter\":' + json.dumps(self.starter) + ',\n\t\t\t\t\"maindish\":' + json.dumps(self.maindish) + ',\n\t\t\t\t\"price\":{\n\t\t\t\t\t\"int\":' + json.dumps(self.priceInt) + ',\n\t\t\t\t\t\"ext\":' + json.dumps(self.priceExt) + '\n\t\t\t\t}\n\t\t\t},' 
        else:
            out = '<h2>' + self.name + '</h2>\n' + '<p>' + self.starter + '<br>' + self.maindish + '<br>' + self.priceInt + ' - ' + self.priceExt + '</p>'
        return out  
    def setname(self, name):
        self.name=name
    def setstarter(self, starter):
        self.starter=starter
    def setmaindish(self, maindish):
        self.maindish=maindish
    def setpriceInt(self, price):
        self.priceInt =price
    def setpriceExt(self, price):
        self.priceExt =price
    def setform(self, form):
        self.form =form