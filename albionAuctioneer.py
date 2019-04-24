# -*- coding: utf-8 -*-
import os
import sys
import json
import urllib3
import requests
import time
from datetime import datetime, timezone
import pytz

from operator import itemgetter, attrgetter
from bs4 import BeautifulSoup

try:
    from PySide2.QtWidgets import *
    from PySide2.QtGui import *
    from PySide2.QtCore import *
except:
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

# - config - #
online = False

# - dataset - #
scriptpath = "C:\\Users\\tobia\\Google Drive\\scripts\\albionAuctioneer\\"
dataset = os.path.join(scriptpath,"dataset")
icons = os.path.join(scriptpath,"icons")

# - styles - #

mainstyle = "font-size:10px; background-color:#292929; border: 2px solid #1C1C1C"
darkstyle = "font-size:10px; color: #858585; font-weight: bold;background-color:#1C1C1C; border: 2px solid #111111; text-align: left; padding-left: 10px; padding-right: 10px; height: 20px;"
lightstyle = "font-size:10px; color: #CCCCCC; background-color:#3B3B3B; border: 1px solid #1C1C1C; height: 20px;"
blackstyle = "font-size:15px; color: #1C1C1C; font-weight: bold; height: 20px; border: 2px solid #292929"
darktextstyle = "font-size:10px; background-color:#292929; border: 2px solid #292929;"

# - styles - #
app = QApplication(sys.argv)

class albionAuctioneer(QWidget):
    def __init__(self):
        super(albionAuctioneer, self).__init__()

        self.showicon = QIcon("/lucas/ilm/dept/dms/sand/tdanbo/dmsTools/dmsScripts/textureBuilder_shown.png")
        self.hideicon = QIcon("/lucas/ilm/dept/dms/sand/tdanbo/dmsTools/dmsScripts/textureBuilder_hidden.png")

        # - layouts - #     
        self.mainLayout = QVBoxLayout()
        self.mainLayout.setContentsMargins(5,5,5,5)
        self.mainLayout.setSpacing(0) 

        self.controllayout = QVBoxLayout()
        self.datalayout = QVBoxLayout()

        # - ui loop - #
        self.catagories = ["control","data"]
        self.layouts = [self.controllayout,self.datalayout]
        for w,c,l in zip(self.catagories,range(len(self.catagories)),self.layouts):
            self.catagorylayout = QGridLayout()

            self.catagorybutton = QPushButton(w.upper())
            self.catagorybutton.clicked.connect(self.showHide)
            self.catagorybutton.setObjectName(w)
            self.catagorybutton.setFocusPolicy(Qt.NoFocus)
            self.catagorybutton.setFixedSize(1015,30)
            self.catagorybutton.setLayoutDirection(Qt.RightToLeft)
            self.catagorybutton.setIcon(self.hideicon)
            self.catagorybutton.setStyleSheet(darkstyle)

            self.catagoryframe = QFrame()
            self.catagoryframe.setFrameShape(QFrame.StyledPanel)
            self.catagoryframe.setObjectName(w+"_frame")
            self.catagoryframe.setHidden(True)

            self.mainLayout.addWidget(self.catagorybutton)
            self.mainLayout.addWidget(self.catagoryframe)

            self.catagoryframe.setLayout(l)

        # - widgets - #
        self.catagoriesui = QComboBox()
        self.catagoriesui.addItems(["accessories","armor","artefacts","cityresources","consumables","farmables","furniture","gatherergear","luxurygoods","magic","materials","melee","mounts","offhand","products","ranged","resources","token","tools","trophies"])
        self.catagoriesui.setFixedSize(499,20)
        self.tierui = QComboBox()
        self.tierui.addItems(["all","T1","T2","T3","T4","T5","T6","T7","T8"])
        self.tierui.setFixedSize(499,20)
        self.generateui = QPushButton("generate")
        self.generateui.clicked.connect(self.generate)
        self.generateui.setFixedSize(430,20)

        self.ccity = QCheckBox("Caerleon")
        self.lcity = QCheckBox("Lymhurst")
        self.mcity = QCheckBox("Martlock")
        self.bcity = QCheckBox("Bridgewatch")
        self.tcity = QCheckBox("Thetford")
        self.fcity = QCheckBox("Fort Sterling")
        self.margincap = QLineEdit("50")
        self.margincap.setAlignment(Qt.AlignCenter)
        self.margincap.setFixedSize(30,20)
        self.hourcap = QLineEdit("1")
        self.hourcap.setAlignment(Qt.AlignCenter)
        self.hourcap.setFixedSize(30,20)

        self.toplayout = QHBoxLayout()
        self.botlayout = QHBoxLayout()

        self.controllayout.addLayout(self.toplayout)
        self.controllayout.addLayout(self.botlayout)

        [self.botlayout.addWidget(w) for w in [self.ccity,self.lcity,self.mcity,self.bcity,self.tcity,self.fcity,self.margincap,self.hourcap,self.generateui]]
        [self.toplayout.addWidget(w) for w in [self.catagoriesui,self.tierui]]


        # - set main layout - #
        self.setLayout(self.mainLayout)
        self.mainLayout.setSizeConstraint(self.mainLayout.SetFixedSize)

        # - set main layout - #
        self.setWindowTitle('albionAuctioneer v1.0')
        self.styles()

    def generate(self):#
        print("generate")
        self.clearLayout()
        self.datagather()

        for self.auction in sorted(self.auctions, key=itemgetter(7), reverse=True):
            h = 40
            print(self.auction[0])
            print(self.auction[7])
            self.auctionlayout = QHBoxLayout()
            self.auctionwidget = QWidget()
            self.auctionwidget.setLayout(self.auctionlayout)

            self.iconlabel = QToolButton()
            self.iconlabel.setFixedSize(h,h)
            print(icons+self.auction[8]+".png")
            icon  = QPixmap(icons+"\\"+self.auction[8]+".png")
            self.iconlabel.setIcon(icon)
            self.iconlabel.setIconSize(QSize(h-2, h-2))

            self.namelabel = QPushButton(str(self.auction[0]))
            self.namelabel.setFixedSize(200,h)
            
            # - button icon - #

            self.fromlabel = QLabel(str(self.auction[2])+"\n"+str(self.auction[9]))
            self.fromlabel.setFixedSize(150,h)
            self.fromlabel.setAlignment(Qt.AlignCenter)

            self.fromvalue = QLabel(str(self.auction[3]))
            self.fromvalue.setFixedSize(50,h)
            self.fromvalue.setAlignment(Qt.AlignCenter)

            self.travelicon = QLabel(">")
            self.travelicon.setAlignment(Qt.AlignCenter)
            self.travelicon.setFixedSize(25,h)

            self.tovalue = QLabel(str(self.auction[5]))
            self.tovalue.setFixedSize(50,h)
            self.tovalue.setAlignment(Qt.AlignCenter)

            self.tolabel = QLabel(str(self.auction[4])+"\n"+str(self.auction[10]))
            self.tolabel.setFixedSize(150,h)
            self.tolabel.setAlignment(Qt.AlignCenter)

            self.marginlabel = QLabel(str(self.auction[6]))
            self.marginlabel.setFixedSize(50,h)
            self.marginlabel.setAlignment(Qt.AlignCenter)

            self.marginplabel = QLabel(str(self.auction[7])+" %")
            self.marginplabel.setFixedSize(50,h)
            self.marginplabel.setAlignment(Qt.AlignCenter)

            widgets = [self.iconlabel,self.namelabel,self.fromlabel,self.fromvalue,self.travelicon,self.tovalue,self.tolabel,self.marginlabel,self.marginplabel]

            [self.auctionlayout.addWidget(w) for w in widgets]
            [w.setStyleSheet(lightstyle) for w in widgets]

            self.travelicon.setStyleSheet(blackstyle)

            self.datalayout.addWidget(self.auctionwidget)


    def datagather(self):
        self.auctions = []

        self.tier = self.tierui.currentText()[1]
        self.category = self.catagoriesui.currentText()

        # - dataset - #
        self.dataset = os.path.join(dataset,self.category+".txt")
        file = open(self.dataset, "r+")
        lines = file.readlines()
        striplines = [line.rstrip('\n') for line in lines]
        self.allauctions = []
        for dataitem in striplines:
            if self.tier == "l":
                print(dataitem)
                self.allauctions.append(dataitem)
            elif self.tier == dataitem.split(":")[2]:
                print(dataitem)
                self.allauctions.append(dataitem)

        # - TABLE MODEL - #

        for item in self.allauctions:
            self.itemname = item.split(":")[0]
            self.itemtier = item.split(":")[2]
            self.itemid = item.split(":")[3]

            http = urllib3.PoolManager()
            page = "https://www.albion-online-data.com/api/v1/stats/prices/%s" % (self.itemid)
            time.sleep(1)
            heroes = http.request('GET', page)
            heroes_dict = json.loads(heroes.data.decode('UTF-8'))
            self.pricedata = []
            for i in heroes_dict:
                if i['city'] in ["Caerleon","Lymhurst","Martlock","Bridgewatch","Thetford","Fort Sterling"]:
                    if i['sell_price_min_date'] != "0001-01-01T00:00:00":
                        currenttime = datetime.now(tz=pytz.utc).replace(microsecond=0)
                        datatime = datetime.strptime(i['sell_price_min_date'], '%Y-%m-%dT%H:%M:%S')
                        currenttime = currenttime.replace(tzinfo=None)
                        difference = currenttime - datatime
                        print(difference)
                        if "day" not in str(difference).split(":")[0]:
                            if int(str(difference).split(":")[0]) < int(self.hourcap.text()):
                                print("good data")
                                self.data = (i['city'], i['sell_price_min'], i['sell_price_min_date'])
                                self.pricedata.append(self.data)
                            else:
                                print("old data")
                        else:
                            pass
                    else:
                        pass
                else:
                    pass

            # - remove 0 data - #

            for pd in self.pricedata:
                if pd[1] == 0:
                    self.pricedata.remove(pd)

            if len(self.pricedata) > 1:

                self.fromdata = sorted(self.pricedata, key=itemgetter(1))[0]
                self.todata = sorted(self.pricedata, key=itemgetter(1))[-1]

                self.fromcity = self.fromdata[0]
                self.fromvalue = self.fromdata[1]
                self.fromvaluedata = self.fromdata[2].replace("T"," ")

                self.tocity = self.todata[0]
                self.tovalue = self.todata[1]
                self.tovaluedata = self.todata[2].replace("T"," ")

                self.margin = self.todata[1]-self.fromdata[1]
                self.marginp = round((self.margin/self.todata[1])*100,2)

                if self.marginp > float(self.margincap.text()):
                    pass
                else:
                    self.auctions.append((self.itemname,self.itemtier,self.fromcity,self.fromvalue,self.tocity,self.tovalue,self.margin,self.marginp,self.itemid,self.tovaluedata,self.fromvaluedata))
            else:
                pass

    # - Function to set UI styles - #
    def styles(self):
        self.setStyleSheet(mainstyle)
        [w.setStyleSheet(lightstyle) for w in [self.catagoriesui,self.tierui,self.margincap,self.hourcap,self.generateui]]
        [w.setStyleSheet(darktextstyle) for w in [self.ccity,self.lcity,self.mcity,self.bcity,self.tcity,self.fcity]]

    # - Function for clearing the browser layout                           - #
    def clearLayout(self):
        layout = self.datalayout
        for i in reversed(range(layout.count())):
            layout.takeAt(i).widget().deleteLater()

    # - UTILITY - Function for showing and hiding parts of the  UI         - #      
    def showHide(self):
        senderobjname = self.sender().objectName()
        items = (self.mainLayout.itemAt(i) for i in range(self.mainLayout.count())) 
        for w in items:
            try:
                if w.widget().objectName() == senderobjname+"_frame":
                    if w.widget().isHidden() == True:
                        self.sender().setIcon(self.showicon)
                        w.widget().setHidden(False)
                    else:
                        self.sender().setIcon(self.hideicon)
                        w.widget().setHidden(True)
            except:
                pass

panel = albionAuctioneer()
panel.show()
sys.exit(app.exec_())

